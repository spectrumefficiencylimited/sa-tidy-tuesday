"""
build_site.py
-------------
Render ready super QMDs to self-contained HTML and push to
TheDataShrink.github.io.

Usage:
  py -3 build_site.py                   # render + push
  py -3 build_site.py --render-only     # render, don't push
  py -3 build_site.py --push-only       # skip render, just push
  py -3 build_site.py --episode global_health_spending  # single episode

What gets rendered:
  Super QMDs for episodes with reproduction_status = ready_local
  or ready_with_external_steps (i.e. have actual local data and an Rmd).

What is excluded:
  - data-screencasts/  (original screencast code — not ours)
  - tidytuesday/       (upstream data repo)
  - raw-data/          (transcripts)
  - episode guides     (internal reproduction artifacts)
"""

import argparse
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT       = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "output" / "reproduction_index.csv"
SUPER_DIR  = ROOT / "output" / "super_qmd"
CSS_SRC    = ROOT / "site" / "thedatashrink.css"

# Repo that serves TheDataShrink.github.io — sibling folder by default.
# Override with --site-repo if your clone is elsewhere.
DEFAULT_SITE_REPO = ROOT.parent / "TheDataShrink.github.io"
SITE_SUBDIR       = "tidy-tuesday"   # subfolder inside the Pages repo

READY_STATUSES = {"ready_local", "ready_with_external_steps"}


# ---------------------------------------------------------------------------
# Find Quarto
# ---------------------------------------------------------------------------

QUARTO_CANDIDATES = [
    r"C:\PROGRA~1\RStudio\RESOUR~1\app\bin\quarto\bin\quarto.cmd",  # short path avoids spaces
    r"C:\Program Files\Quarto\bin\quarto.cmd",
    r"C:\Users\mstoian\AppData\Local\Programs\Quarto\bin\quarto.cmd",
    r"C:\Program Files\RStudio\bin\quarto\bin\quarto.cmd",
    "quarto",
    "quarto.cmd",
]


def find_quarto() -> str:
    for candidate in QUARTO_CANDIDATES:
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                return candidate
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    raise RuntimeError(
        "Quarto not found. Install from https://quarto.org or add to PATH."
    )


# ---------------------------------------------------------------------------
# Load index
# ---------------------------------------------------------------------------

def load_ready_episodes(episode_filter: str | None = None) -> list[dict]:
    with INDEX_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    ready = [
        r for r in rows
        if r.get("reproduction_status", "") in READY_STATUSES
        and r.get("ker_status", "") == "extracted"
    ]

    if episode_filter:
        ready = [r for r in ready if episode_filter in r.get("function_name", "")]

    return ready


def find_super_qmd(function_name: str) -> Path | None:
    hits = sorted(SUPER_DIR.glob(f"*_{function_name}_super.qmd"))
    return hits[0] if hits else None


# ---------------------------------------------------------------------------
# Render one episode
# ---------------------------------------------------------------------------

def render_episode(quarto: str, row: dict, out_dir: Path) -> Path | None:
    fn  = row["function_name"]
    qmd = find_super_qmd(fn)
    if not qmd:
        print(f"  SKIP {fn}: no super QMD found")
        return None

    slug     = re.sub(r"_", "-", fn)
    html_out = out_dir / f"{slug}.html"

    # Render into the same folder as the QMD (avoids cross-dir --output issues),
    # then move the result to out_dir.
    rendered_beside = qmd.with_suffix(".html")

    print(f"  Rendering {qmd.name} → {html_out.name}")

    result = subprocess.run(
        [
            quarto, "render", qmd.name,
            "--to", "html",
            "--no-cache",
            "-M", "embed-resources:true",
        ],
        cwd=qmd.parent,       # run from the QMD's own directory
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        print(f"    ERROR:\n{result.stderr[-800:]}")
        return None

    if not rendered_beside.exists():
        print(f"    ERROR: expected {rendered_beside} but not found")
        return None

    import shutil
    shutil.move(str(rendered_beside), str(html_out))
    return html_out


# ---------------------------------------------------------------------------
# Build index page
# ---------------------------------------------------------------------------

def build_index(rows: list[dict], out_dir: Path):
    cards = []
    for row in rows:
        fn    = row["function_name"]
        title = row.get("transcript_title", fn).replace("Analyzing ", "").replace(" in R", "")
        slug  = re.sub(r"_", "-", fn)
        html  = out_dir / f"{slug}.html"
        if not html.exists():
            continue
        ds    = row.get("data_source", "")
        atype = row.get("analysis_type", "EDA")
        pat   = row.get("pattern_signature", "")
        cards.append(
            f'<div class="tt-card">'
            f'<h4><a href="{slug}.html">{title}</a></h4>'
            f'<div class="meta">'
            f'{ds} &nbsp;·&nbsp; {atype}'
            f'{"&nbsp;·&nbsp;<code>" + pat + "</code>" if pat else ""}'
            f'</div></div>'
        )

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TidyTuesday — TheDataShrink</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="../thedatashrink.css">
  <style>
    body {{ max-width: 860px; margin: 2rem auto; padding: 0 1rem; }}
    .hero {{ background: #0f2b46; color: white; border-radius: 10px;
             padding: 2rem 2.5rem; margin-bottom: 2rem; }}
    .hero h1 {{ color: #f4a300; border: none; font-size: 2.2rem; }}
    .hero p  {{ color: #c8dde6; margin: 0; }}
  </style>
</head>
<body>
  <div class="hero">
    <h1>TidyTuesday</h1>
    <p>Analysis companions for each episode &nbsp;·&nbsp; <span class="yt-companion">YouTube</span></p>
  </div>
  <p><strong>{len(cards)}</strong> episodes ready. Each page maps Hour&nbsp;1&nbsp;/&nbsp;Hour&nbsp;2&nbsp;/&nbsp;Hour&nbsp;3.</p>
  {"".join(cards)}
  <footer class="page-footer">
    Built with <a href="https://github.com/TheDataShrink">TheDataShrink</a> ·
    Data from <a href="https://github.com/rfordatascience/tidytuesday">TidyTuesday</a>
  </footer>
</body>
</html>
"""
    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"  Wrote index: {index_path}")


# ---------------------------------------------------------------------------
# Push to GitHub Pages repo
# ---------------------------------------------------------------------------

def push_site(site_repo: Path, out_dir: Path):
    if not site_repo.exists():
        print(f"  Site repo not found at {site_repo}")
        print("  Clone it first or pass --site-repo <path>")
        return

    dest = site_repo / SITE_SUBDIR
    dest.mkdir(parents=True, exist_ok=True)

    # Copy CSS to repo root
    shutil.copy(CSS_SRC, site_repo / "thedatashrink.css")

    # Copy all rendered HTMLs
    copied = 0
    for html in out_dir.glob("*.html"):
        shutil.copy(html, dest / html.name)
        copied += 1

    print(f"  Copied {copied} HTML files to {dest}")

    # Git commit + push
    msg = f"Update TidyTuesday site: {copied} episodes"
    cmds = [
        ["git", "add", SITE_SUBDIR, "thedatashrink.css"],
        ["git", "commit", "-m", msg],
        ["git", "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=site_repo, capture_output=True, text=True)
        out = (result.stdout + result.stderr).strip()
        if out:
            print(f"  {out}")
        if result.returncode != 0 and "nothing to commit" not in out:
            print(f"  git error: {out}")
            break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-only", action="store_true")
    parser.add_argument("--push-only",   action="store_true")
    parser.add_argument("--episode",     help="Filter to one function_name")
    parser.add_argument("--site-repo",   default=str(DEFAULT_SITE_REPO))
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    print()
    print("=" * 62)
    print("  TheDataShrink -- site build")
    print("=" * 62)
    print()

    site_repo = Path(args.site_repo)
    out_dir   = site_repo / SITE_SUBDIR if site_repo.exists() else ROOT / "site" / "html"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not site_repo.exists():
        print(f"  Site repo not found at {site_repo}")
        print(f"  Rendering to {out_dir} instead (run with --site-repo to set path)")
        print()

    episodes = load_ready_episodes(args.episode)
    print(f"Episodes to render: {len(episodes)}")
    print()

    if not args.push_only:
        quarto = find_quarto()
        print(f"Quarto: {quarto}")
        print()

        print("── Rendering ────────────────────────────────────────────────")
        for row in episodes:
            render_episode(quarto, row, out_dir)
        print()

        print("── Index ────────────────────────────────────────────────────")
        build_index(episodes, out_dir)
        print()

    if not args.render_only:
        print("── Push ─────────────────────────────────────────────────────")
        push_site(site_repo, out_dir)
        print()

    print("Done.")
    print(f"  HTML files in: {out_dir}")
    if site_repo.exists():
        print(f"  Site repo:     {site_repo}")
    print()


if __name__ == "__main__":
    main()
