"""One-off bulk fix for super QMDs:
  1. Remove Transcript Preview section
  2. Reformat Episode Snapshot (intent callout first, metadata as table, manifest enrichment)
  3. Add thought_execution_log code chunk after Thought Process Map bullets
"""
import re, json
from pathlib import Path

SUPER_DIR    = Path(__file__).parent / "output" / "super_qmd"
EPISODES_DIR = Path(__file__).parent / "output" / "episodes"

# ── Load manifests ────────────────────────────────────────────────────────────
manifests = {}
for f in EPISODES_DIR.glob("*/episode_manifest.json"):
    try:
        m = json.loads(f.read_text(encoding="utf-8"))
        manifests[m["function_name"]] = m
    except Exception:
        pass
print(f"Manifests loaded: {len(manifests)}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_fn(text):
    m = re.search(r"`function_name`.*?`([^`]+)`", text)
    return m.group(1) if m else None


def reformat_snapshot(text, manifest=None):
    """Replace Episode Snapshot bullet-list with table + intent-first structure.
    Uses string operations (no DOTALL regex) to avoid catastrophic backtracking.
    """
    HEADER  = "## Episode Snapshot\n\n"
    CALLOUT = "::: {.callout-note}\n## Analysis Intent\n"
    END_C   = "\n:::"

    h_idx = text.find(HEADER)
    if h_idx == -1:
        return text

    c_idx = text.find(CALLOUT, h_idx)
    if c_idx == -1:
        return text

    # Collect bullet lines between HEADER and callout
    bullets_raw = text[h_idx + len(HEADER) : c_idx].strip()
    if not bullets_raw.startswith("- `"):
        return text  # already reformatted

    # Find end of callout
    ec_idx = text.find(END_C, c_idx + len(CALLOUT))
    if ec_idx == -1:
        return text
    intent = text[c_idx + len(CALLOUT) : ec_idx].strip()
    end_of_block = ec_idx + len(END_C)

    # Parse bullet fields
    fields = {}
    for line in bullets_raw.splitlines():
        hit = re.match(r"- `(\w+)`: `?([^`\n]+)`?", line)
        if hit:
            fields[hit.group(1)] = hit.group(2)
        else:
            hit2 = re.match(r"- `(\w+)`: (.+)", line)
            if hit2:
                fields[hit2.group(1)] = hit2.group(2).strip()

    pos         = fields.get("queue_position", "—")
    fn          = fields.get("function_name",  "—")
    atype       = fields.get("analysis_type",  "—")
    pattern_sig = fields.get("pattern_signature", "—")
    dsrc        = fields.get("data_source",    "—")
    status      = fields.get("reproduction_status", "—")

    pkg_lines = feature_lines = exec_lines = ""
    if manifest:
        pkgs = manifest.get("required_packages", [])
        if pkgs:
            pkg_list = ", ".join(f"`{p}`" for p in pkgs)
            pkg_lines = f"\n**Packages:** {pkg_list}\n"
        features = manifest.get("features", {})
        active = [k for k, v in features.items() if v]
        if active:
            feature_lines = f"\n**Features:** {', '.join(active)}\n"
        exec_notes = manifest.get("execution_notes", [])
        if exec_notes:
            exec_lines = "\n**Execution notes:**\n" + "".join(f"- {n}\n" for n in exec_notes)

    new_block = (
        f"## Episode Snapshot\n\n"
        f"::: {{.callout-note}}\n## Analysis Intent\n{intent}\n:::\n\n"
        f"| Field | Value |\n|---|---|\n"
        f"| Queue | #{pos} |\n"
        f"| Function | `{fn}` |\n"
        f"| Analysis type | {atype} |\n"
        f"| Data source | {dsrc} |\n"
        f"| Status | `{status}` |\n"
        f"{pkg_lines}"
        f"{feature_lines}"
        f"{exec_lines}"
        f"\n**Analytical pattern:** `{pattern_sig}`\n"
    )
    return text[:h_idx] + new_block + text[end_of_block:]


def add_thought_code(text):
    marker = "### Thought Process Map\n\n"
    idx = text.find(marker)
    if idx == -1:
        return text
    after = idx + len(marker)
    end_m = re.search(r"\n\n### ", text[after:])
    if not end_m:
        return text

    bullet_block = text[after : after + end_m.start()]
    steps = re.findall(r"T(\d+) \| (\w+) \|", bullet_block)
    if not steps:
        return text

    insert_at = after + end_m.start()
    if "thought_execution_log" in text[max(0, insert_at - 400) : insert_at + 10]:
        return text  # already added

    rows = "\n".join(f'  "T{n}", "{move.title()}", "",' for n, move in steps)
    chunk = (
        "\n\n```{r}\n"
        "#| label: thought_execution_log\n"
        "#| eval: false\n\n"
        "# Fill in `finding` after completing each stage.\n"
        "thought_log <- tibble::tribble(\n"
        "  ~step,  ~move,        ~finding,\n"
        f"{rows}\n"
        ")\n"
        "thought_log\n"
        "```\n"
    )
    return text[:insert_at] + chunk + text[insert_at:]


# ── Main loop ─────────────────────────────────────────────────────────────────
changed = skipped = already_done = 0

for i, qmd in enumerate(sorted(SUPER_DIR.glob("*.qmd"))):
    if i % 50 == 0:
        print(f"  [{i}] {qmd.name}", flush=True)
    text     = qmd.read_text(encoding="utf-8")
    original = text

    # 1. Remove Transcript Preview (string-based, no DOTALL backtracking risk)
    tp_start = text.find("\n## Transcript Preview\n\n")
    if tp_start != -1:
        tp_body_start = tp_start + len("\n## Transcript Preview\n\n")
        tp_end = text.find("\n\n## ", tp_body_start)
        if tp_end != -1:
            text = text[:tp_start] + "\n\n" + text[tp_end + 2:]  # keep the \n\n## next section

    # 2. Reformat Episode Snapshot
    fn       = extract_fn(text)
    manifest = manifests.get(fn) if fn else None
    text     = reformat_snapshot(text, manifest)

    # 3. Add thought execution log chunk
    text = add_thought_code(text)

    if "## Transcript Preview" not in original and "thought_execution_log" in original:
        already_done += 1
        continue

    if text != original:
        qmd.write_text(text, encoding="utf-8")
        changed += 1
    else:
        skipped += 1

print(f"Modified: {changed}  |  Unchanged: {skipped}  |  Already done: {already_done}")
