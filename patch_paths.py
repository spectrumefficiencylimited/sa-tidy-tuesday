"""
patch_paths.py — Fix code_file paths to point at data-screencasts-dgrtwo/

All 79 rows in control_table.csv + control_table_full.csv reference
  data-screencasts/<name>.Rmd
but those files live in:
  data-screencasts-dgrtwo/<name>.Rmd

This script:
1. Patches control_table.csv
2. Patches control_table_full.csv
3. Patches source_files.code_file in every output/episodes/*/episode_manifest.json
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DGRTWO = ROOT / "data-screencasts-dgrtwo"
OLD_PREFIX = "data-screencasts/"
NEW_PREFIX = "data-screencasts-dgrtwo/"


def patch_code_file(val: str) -> str:
    if not val or not val.startswith(OLD_PREFIX):
        return val
    fname = Path(val).name
    candidate = DGRTWO / fname
    if candidate.exists():
        return NEW_PREFIX + fname
    return val  # leave unchanged if not found — flag below


def patch_csv(path: Path, code_file_col: str = "code_file"):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            original = row.get(code_file_col, "")
            patched = patch_code_file(original)
            if patched != original:
                print(f"  CSV {path.name}: {original!r} → {patched!r}")
            row[code_file_col] = patched
            rows.append(row)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Patched {path.name} ({len(rows)} rows)")


def patch_manifests():
    episodes_root = ROOT / "output" / "episodes"
    count = 0
    for manifest_path in sorted(episodes_root.rglob("episode_manifest.json")):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        src = data.get("source_files", {})
        original = src.get("code_file", "")
        patched = patch_code_file(original)
        if patched != original:
            src["code_file"] = patched
            data["source_files"] = src
            manifest_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            count += 1
            print(f"  Manifest {manifest_path.parent.name}: {original!r} → {patched!r}")
    print(f"  Patched {count} manifests")


def main():
    print("=== Patching control_table.csv ===")
    patch_csv(ROOT / "control_table.csv")

    print("\n=== Patching control_table_full.csv ===")
    patch_csv(ROOT / "control_table_full.csv")

    print("\n=== Patching episode_manifest.json files ===")
    patch_manifests()

    print("\nDone. Run `python3 build_episode_outputs.py` to rebuild from clean paths.")


if __name__ == "__main__":
    main()
