import csv
import os
import re


ROOT = os.path.abspath(os.path.dirname(__file__))
TRANSCRIPT_DIR = os.path.join(ROOT, "raw-data", "inspiration")
CODE_DIR = os.path.join(ROOT, "data-screencasts")
EXISTING_CONTROL_PATH = os.path.join(ROOT, "control_table.csv")
OUTPUT_PATH = os.path.join(ROOT, "control_table_full.csv")

IGNORE_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "with",
    "in",
    "of",
    "for",
    "to",
    "on",
    "us",
    "our",
    "tidy",
    "tuesday",
    "dataset",
    "data",
    "analysis",
    "analyzing",
    "r",
    "rmd",
    "txt",
}

CONTROL_COLUMNS = [
    "transcript_title",
    "transcript_file",
    "code_file",
    "function_name",
    "data_source",
    "analysis_intent",
    "analysis_type",
    "pattern_signature",
    "adaptation_hint",
    "ker_status",
    "notes",
    "normalized_key",
]


def normalize_tokens(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    tokens = [token for token in text.split() if token not in IGNORE_WORDS]
    return " ".join(tokens)


def sanitize_function_name(title):
    function_name = title.lower()
    function_name = re.sub(r"[^a-z0-9]+", " ", function_name)
    function_name = re.sub(
        r"\b(r|rmd|txt|the|a|an|and|with|in|of|for|to|on|us|our|tidy|tuesday|dataset|data|analysis|analyzing)\b",
        " ",
        function_name,
    )
    function_name = re.sub(r"\s+", " ", function_name).strip().replace(" ", "_")
    if re.match(r"^[0-9]", function_name):
        function_name = f"x_{function_name}"
    return function_name


def normalize_path(*parts):
    return "/".join(parts)


def load_existing_rows(path):
    if not os.path.exists(path):
        return {}, {}

    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = csv.DictReader(handle)
        rows = [row for row in rows if row.get("transcript_title", "").strip()]

    by_title = {row["transcript_title"]: row for row in rows}
    by_transcript_file = {
        row["transcript_file"]: row
        for row in rows
        if row.get("transcript_file", "").strip()
    }
    return by_title, by_transcript_file


def main():
    transcript_files = sorted(
        filename for filename in os.listdir(TRANSCRIPT_DIR) if filename.lower().endswith(".txt")
    )
    code_files = sorted(
        filename for filename in os.listdir(CODE_DIR) if filename.lower().endswith(".rmd")
    )

    existing_rows_by_title, existing_rows_by_transcript_file = load_existing_rows(EXISTING_CONTROL_PATH)
    code_map = {}
    for filename in code_files:
        normalized_key = normalize_tokens(os.path.splitext(filename)[0])
        code_map.setdefault(normalized_key, filename)

    rows = []
    for transcript_filename in transcript_files:
        title = os.path.splitext(transcript_filename)[0]
        transcript_file = normalize_path("raw-data", "inspiration", transcript_filename)
        normalized_key = normalize_tokens(title)
        matched_code = code_map.get(normalized_key, "")
        existing = (
            existing_rows_by_title.get(title)
            or existing_rows_by_transcript_file.get(transcript_file, {})
        )

        code_file = existing.get("code_file", "").strip()
        if not code_file and matched_code:
            code_file = normalize_path("data-screencasts", matched_code)

        row = {
            "transcript_title": existing.get("transcript_title", "").strip() or title,
            "transcript_file": existing.get("transcript_file", "").strip() or transcript_file,
            "code_file": code_file,
            "function_name": existing.get("function_name", "").strip() or sanitize_function_name(title),
            "data_source": existing.get("data_source", "").strip(),
            "analysis_intent": existing.get("analysis_intent", "").strip(),
            "analysis_type": existing.get("analysis_type", "").strip(),
            "pattern_signature": existing.get("pattern_signature", "").strip(),
            "adaptation_hint": existing.get("adaptation_hint", "").strip(),
            "ker_status": existing.get("ker_status", "").strip(),
            "notes": existing.get("notes", "").strip(),
            "normalized_key": normalized_key,
        }
        rows.append(row)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONTROL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    matched_count = sum(1 for row in rows if row["code_file"])
    unmatched_count = len(rows) - matched_count

    print("Wrote", OUTPUT_PATH)
    print("Transcripts:", len(rows), "Rmd files:", len(code_files))
    print("Matches:", matched_count)
    print("Unmatched:", unmatched_count)
    for row in rows:
        if not row["code_file"]:
            print("UNMATCHED:", row["transcript_file"], "key=", row["normalized_key"])


if __name__ == "__main__":
    main()
