"""
build_transcripts.py
--------------------
For every row in control_table_full.csv that has ker_status == "needs_mapping"
and an empty transcript_file, this script:

1. Reads the corresponding tidytuesday/data/YYYY/YYYY-MM-DD/readme.md
2. Parses the data dictionary (column names + types + descriptions)
3. Finds the CSV/TSV files in that date folder
4. Generates a synthetic David Robinson-style analysis transcript
5. Writes it to raw-data/inspiration/{transcript_title}.txt
6. Updates transcript_file in control_table_full.csv

The transcript supports three depth tiers:
  - 1h  (~25 min of content): intro → inspect → count → first chart
  - 2h  (~90 min):  adds pivot/join → multi-axis → outlier investigation
  - 3h  (~180 min): adds model → coefficients → residuals → final chart → KER capture

Default depth is "3h" for all new entries.  Pass depth="1h" or depth="2h"
to generate lighter versions.

Timestamped speech structure:
  Hour 1  (0:00–60:00): breadth-first curiosity
  Hour 2 (60:00–120:00): depth-first hypothesis
  Hour 3 (120:00–180:00): synthesis & communication
"""

import csv
import os
import re
import glob
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CT_PATH = SCRIPT_DIR / "control_table_full.csv"
INSPIRATION_DIR = SCRIPT_DIR / "raw-data" / "inspiration"
TT_DATA_DIR = SCRIPT_DIR / "tidytuesday" / "data"

INSPIRATION_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Readme parsing helpers
# ---------------------------------------------------------------------------

def extract_date_from_source(data_source: str) -> str | None:
    """Pull YYYY-MM-DD from 'TidyTuesday 2022-01-11' etc."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", data_source)
    return m.group(1) if m else None


def find_readme(date_str: str) -> Path | None:
    year = date_str[:4]
    p = TT_DATA_DIR / year / date_str / "readme.md"
    return p if p.exists() else None


def find_data_files(date_str: str) -> list[str]:
    """Return basenames of CSV/TSV/RDS files in the date folder."""
    year = date_str[:4]
    folder = TT_DATA_DIR / year / date_str
    if not folder.exists():
        return []
    exts = ("*.csv", "*.tsv", "*.rds", "*.RDS", "*.xlsx")
    files = []
    for ext in exts:
        files.extend(folder.glob(ext))
    return [f.name for f in sorted(files)]


def parse_readme(readme_path: Path) -> dict:
    """Extract description, column info, and loading code from a readme."""
    text = readme_path.read_text(encoding="utf-8", errors="ignore")

    # --- description: first non-empty paragraph before any code block ----
    desc_lines = []
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            if not in_code and desc_lines:
                break
            continue
        if in_code:
            continue
        if line.startswith("#"):
            continue
        if line.strip().startswith("|"):
            break
        if line.strip():
            desc_lines.append(line.strip())
        elif desc_lines:
            break

    description = " ".join(desc_lines)[:500]

    # --- data dictionary: parse markdown tables --------------------------
    columns = []
    table_rx = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]*)\|?")
    in_table = False
    skip_next = False  # separator row
    for line in text.splitlines():
        if line.strip().startswith("|variable") or line.strip().startswith("|:"):
            in_table = True
            skip_next = True
            continue
        if in_table:
            if line.strip().startswith("|:-"):
                skip_next = False
                continue
            if not line.strip().startswith("|"):
                in_table = False
                continue
            if skip_next:
                skip_next = False
                continue
            m = table_rx.match(line.strip())
            if m:
                col_name = m.group(1).strip()
                col_type = m.group(2).strip()
                col_desc = m.group(3).strip()
                if col_name and col_name.lower() not in ("variable", ""):
                    columns.append({
                        "name": col_name,
                        "type": col_type,
                        "desc": col_desc,
                    })

    # --- detect date/time column ----------------------------------------
    time_cols = [c for c in columns
                 if any(k in c["name"].lower() for k in
                        ("year", "date", "month", "week", "time", "season"))]

    # --- detect main categorical ----------------------------------------
    cat_cols = [c for c in columns
                if c["type"] in ("character", "chr", "factor", "fct", "logical")
                and c["name"].lower() not in ("id",)]

    # --- detect main numeric --------------------------------------------
    num_cols = [c for c in columns
                if c["type"] in ("integer", "int", "double", "dbl", "numeric")]

    return {
        "description": description,
        "columns": columns,
        "time_cols": time_cols,
        "cat_cols": cat_cols,
        "num_cols": num_cols,
    }


# ---------------------------------------------------------------------------
# Transcript generation helpers
# ---------------------------------------------------------------------------

def _ts(minute: int, second: int = 0) -> str:
    return f"{minute}:{second:02d}"


def _col_comment(col: dict) -> str:
    """A spoken sentence about a column."""
    name = col["name"]
    typ = col["type"]
    desc = col["desc"]
    if desc:
        return f"we have {name} which is {desc.lower()}"
    type_map = {
        "character": "a text field",
        "chr":       "a text field",
        "integer":   "a count or numeric value",
        "int":       "a count or numeric value",
        "double":    "a decimal number",
        "dbl":       "a decimal number",
        "logical":   "a true-false flag",
        "factor":    "a categorical variable",
    }
    human_type = type_map.get(typ.lower(), f"a {typ}")
    return f"we have {name} which looks like {human_type}"


def _time_phrase(time_cols: list) -> str:
    if not time_cols:
        return ""
    col = time_cols[0]["name"]
    return (f"and there's a {col} column so we can definitely look at a "
            f"trend over time which is usually the first thing i want to see")


def _count_phrase(cat_cols: list) -> str:
    if not cat_cols:
        return "let me just do a quick count to see how many rows we have"
    col = cat_cols[0]["name"]
    return (f"let me start with count {col} sort equals true just to see "
            f"what the most common categories are")


def _summarize_phrase(cat_cols: list, num_cols: list) -> str:
    cat = cat_cols[0]["name"] if cat_cols else "category"
    num = num_cols[0]["name"] if num_cols else "value"
    return (f"so we can group by {cat} and summarize the mean of {num} "
            f"and arrange descending that is going to give us the ranking we want")


def _viz_phrase(cat_cols: list, num_cols: list) -> str:
    cat = cat_cols[0]["name"] if cat_cols else "category"
    num = num_cols[0]["name"] if num_cols else "value"
    return (
        f"so i'll do ggplot aes x is fct reorder {cat} by {num} "
        f"y is {num} and then geom col and coord flip so we can read "
        f"the labels that looks really good"
    )


def _has_flag_cols(cols: list) -> bool:
    """True when the table has many logical/boolean tag columns — pivot candidate."""
    flag_types = {"logical", "bool", "lgl"}
    return sum(1 for c in cols if c["type"].lower() in flag_types) >= 3


def _pivot_phrase(cols: list) -> str:
    flags = [c["name"] for c in cols if c["type"].lower() in {"logical", "bool", "lgl"}]
    if not flags:
        return ""
    listed = ", ".join(flags[:5])
    return (
        f"i see a bunch of logical flag columns here {listed} and others "
        f"this is a classic pivot longer situation "
        f"pivot longer cols equals where is logical names to equals tag values to equals value "
        f"filter value equals true "
        f"now we have one row per campus per tag which is much easier to work with"
    )


def generate_transcript(
    title: str,
    topic: str,
    date_str: str,
    readme_info: dict,
    data_files: list[str],
    depth: str = "3h",
) -> str:
    """
    Build a synthetic David Robinson-style transcript.

    depth: "1h"  ~25 min content  (Hour 1 only – breadth-first)
           "2h"  ~90 min content  (Hours 1-2 – adds pivot/join/outlier)
           "3h"  ~180 min content (Hours 1-3 – adds model/residuals/final chart)
    """
    desc = readme_info["description"] or f"data about {topic.lower()}"
    cols = readme_info["columns"]
    time_cols = readme_info["time_cols"]
    cat_cols  = readme_info["cat_cols"]
    num_cols  = readme_info["num_cols"]

    spoken_date = date_str   # fallback

    # Primary/secondary data frames
    primary_df  = data_files[0].rsplit(".", 1)[0].replace("-", "_") if data_files else "tuesdata"
    secondary_df = data_files[1].rsplit(".", 1)[0].replace("-", "_") if len(data_files) > 1 else None

    # Derived phrases
    cat1  = cat_cols[0]["name"]  if cat_cols  else "category"
    cat2  = cat_cols[1]["name"]  if len(cat_cols) > 1 else cat1
    num1  = num_cols[0]["name"]  if num_cols  else "value"
    num2  = num_cols[1]["name"]  if len(num_cols) > 1 else num1
    time1 = time_cols[0]["name"] if time_cols else None
    join_key = cols[0]["name"] if cols else "id"

    col_comments = "\n".join(
        f"{_ts(3 + i // 2, (i % 2) * 30)}\n{_col_comment(c)}"
        for i, c in enumerate(cols[:12])
    )

    files_comment = (
        f"oh interesting we have multiple files today "
        + " and ".join(f.split('/')[-1] for f in data_files[:3])
        + " so there might be some joining to do"
        if len(data_files) > 1
        else (f"alright so we have {data_files[0].split('/')[-1]} let me load that in"
              if data_files else "alright let me load the data")
    )

    # ── HOUR 1 ────────────────────────────────────────────────────────────
    hour1 = f"""\
0:03
hi i'm dave robinson and welcome to another one of my screencasts where i'll be using r and rstudio to analyze data i've never
0:10
seen before as usual the data comes from the tidy tuesday project amazing weekly data project in r
0:16
run by the r for data science online learning community so let's see what data we have to analyze this week
0:23
it is {topic.lower()} that's all i know about this data set i don't know the shape or the format
0:36
{desc[:300].lower().replace(chr(10), ' ')}
1:05
alright let me set up my template here and load the libraries
1:12
library tidyverse library scales theme set theme light
1:30
and i'll bring in the tidy tuesday data
1:45
tuesdata equals tidytuesdayR tt load {date_str}
1:58
{files_comment}
2:10
alright let me look at what we have here
2:18
names tuesdata
2:30
so the columns are
{col_comments}
8:00
{_time_phrase(time_cols)}
8:20
alright let's do a count first so
8:30
{_count_phrase(cat_cols)}
9:00
okay so there are some interesting categories there let me look at the most common ones
9:30
now let me look at a distribution of the numeric columns
10:00
{_summarize_phrase(cat_cols, num_cols)}
10:40
that's a nice summary now let me visualize that
11:00
{_viz_phrase(cat_cols, num_cols)}
11:40
that is looking really nice let me add some labels
12:00
labs title equals something descriptive subtitle equals source tidytuesday {date_str} caption equals source tidytuesday
12:30
alright let me now look at{(' trends over time using the ' + time1 + ' column') if time1 else ' another angle on this data'}
13:00
{f'group by {time1} summarize n equals n' if time1 else f'count {cat1} sort true'}
13:30
{f'ggplot aes x equals {time1} y equals n geom line geom point' if time1 else f'ggplot aes x equals fct reorder {cat1} n y equals n geom col coord flip'}
14:00
that gives us a good picture of the overall shape of this data
14:30
let me think about what else is interesting here
{'14:45' + chr(10) + f'so there is a {secondary_df} table as well let me join that in' + chr(10) + '15:00' + chr(10) + f'left join by equals {join_key} that works nicely' if secondary_df else ''}
16:00
alright so that is the first hour of exploration let me recap what we found
16:30
the main shape of the data is clear and we have a good sense of the key columns
17:00
the most interesting thing i see so far is the variation in {cat1} and {num1}
17:30
i want to come back to this and go deeper in the next session"""

    if depth == "1h":
        return _wrap_header(title, topic, date_str, spoken_date, hour1)

    # ── HOUR 2 ────────────────────────────────────────────────────────────
    pivot_block = _pivot_phrase(cols)
    hour2 = f"""\
60:00
alright welcome back to hour two i want to go deeper on the most interesting finding from hour one
60:30
that was the variation in {cat1} so let me build a hypothesis
61:00
my hypothesis is that {num1} is systematically different across {cat1} groups and i want to test that
61:30
first let me make sure my analysis table is clean and ready
62:00
analysis tbl equals {primary_df} percent>percent
62:30
filter not is na {num1}
63:00
{pivot_block if pivot_block else f'mutate {cat1} equals fct lump {cat1} n equals 10'}
65:00
now let me look at the interaction between two categorical variables
65:30
{f'group by {cat1} {cat2}' if cat2 != cat1 else f'group by {cat1}'}
66:00
summarize median {num1} equals median {num1} na rm equals true n equals n
66:30
arrange desc median {num1}
67:00
ggplot aes x equals {cat1} y equals median {num1} fill equals {cat2 if cat2 != cat1 else num1} geom col position equals dodge
67:30
facet wrap tilde {cat2 if cat2 != cat1 else cat1} scales equals free y
68:00
that is a much richer picture than the first-hour chart
68:30
i can see that the relationship between {cat1} and {num1} is not uniform across {cat2 if cat2 != cat1 else 'groups'}
69:00
now let me look for outliers
69:30
who is way above or below the median for their group
70:00
residual tbl equals analysis tbl percent>percent
70:30
group by {cat1}
71:00
mutate group median equals median {num1} na rm equals true
71:30
mutate residual equals {num1} minus group median
72:00
arrange desc abs residual
72:30
head 20
73:00
interesting the biggest outliers are
73:30
let me label them on a scatter plot
74:00
ggplot aes x equals {num2 if num2 != num1 else f'row_number()'} y equals {num1} label equals {cat1}
74:30
geom point geom text repel size equals 3 max overlaps equals 20
75:00
that gives us the outlier story
75:30
now let me look at correlation structure if we have multiple numeric columns
76:00
{f'select {num1} {num2} {cat1}' if num2 != num1 else f'select where is numeric'}
76:30
cor method equals spearman
77:00
ggplot aes x equals {num1} y equals {num2 if num2 != num1 else num1} color equals {cat1}
77:30
geom point alpha equals 0.6 geom smooth method equals lm se equals false
78:00
{f'there is a clear relationship between {num1} and {num2}' if num2 != num1 else 'the numeric variables tell an interesting story'}
78:30
now let me see if i can build a geographic or faceted view
79:00
count {cat1} {cat2 if cat2 != cat1 else 'wt = ' + num1 + ' sort = TRUE'}
79:30
ggplot aes x equals {cat1} fill equals {cat2 if cat2 != cat1 else cat1} geom bar position equals fill coord flip
80:00
theme legend position equals bottom guides fill equals guide legend nrow equals 2
80:30
that is a solid hour two i feel like i understand the structure of this data much better now
81:00
the key finding from hour two is that {cat1} is the most important grouping variable
81:30
and there are some notable outliers that are worth flagging in the final communication"""

    if depth == "2h":
        return _wrap_header(title, topic, date_str, spoken_date, hour1 + "\n" + hour2)

    # ── HOUR 3 ────────────────────────────────────────────────────────────
    model_predictors = " plus ".join(
        [c["name"] for c in cat_cols[:2]] + [c["name"] for c in num_cols[:2]]
    ) or cat1
    hour3 = f"""\
120:00
alright hour three now this is where i want to synthesize everything and build a model
120:30
the question i want to answer is what predicts {num1}
121:00
let me build a linear regression with the main predictors we identified in hour two
121:30
model tbl equals analysis tbl percent>percent
122:00
mutate across where is character as factor
122:30
model fit equals lm {num1} tilde {model_predictors} data equals model tbl
123:00
summary model fit
123:30
broom tidy model fit percent>percent
124:00
filter p value less than 0 05
124:30
mutate term equals fct reorder term estimate
125:00
ggplot aes x equals term y equals estimate ymin equals estimate minus 1.96 times std error ymax equals estimate plus 1.96 times std error
125:30
geom pointrange geom hline yintercept equals 0 linetype equals dashed
126:00
coord flip labs title equals what predicts {num1} subtitle equals coefficients from linear model
126:30
that is the coefficient plot and the biggest drivers are clearly visible
127:00
now let me look at residuals to find who is over and underperforming
127:30
augmented tbl equals broom augment model fit data equals model tbl
128:00
arrange desc abs .resid
128:30
head 20
129:00
these are the cases where the model was most wrong
129:30
let me label them on a residual plot
130:00
ggplot augmented tbl aes x equals .fitted y equals .resid label equals {cat1}
130:30
geom point alpha equals 0.5 geom smooth method equals loess se equals false color equals steelblue
131:00
geom text repel data equals filter augmented tbl abs .resid greater than quantile abs .resid 0.95
131:30
size equals 3 max overlaps equals 15
132:00
geom hline yintercept equals 0 linetype equals dashed
132:30
labs title equals residuals who outperforms or underperforms their predicted {num1}
133:00
alright now let me build the final communication chart
133:30
this should be the single chart that tells the whole story of this dataset
134:00
i am going to go with a reordered bar chart that shows {num1} by {cat1}
134:30
with color encoding for {cat2 if cat2 != cat1 else 'a secondary dimension'}
135:00
and i will annotate the chart with the key outliers we found
135:30
final tbl equals analysis tbl percent>percent
136:00
group by {cat1} percent>percent
136:30
summarize median {num1} equals median {num1} na rm equals true n equals n percent>percent
137:00
filter n greater than 5 percent>percent
137:30
mutate {cat1} equals fct reorder {cat1} median {num1}
138:00
ggplot final tbl aes x equals {cat1} y equals median {num1} fill equals median {num1}
138:30
geom col show legend equals false
139:00
scale fill gradient2 low equals tomato mid equals gray90 high equals steelblue midpoint equals median analysis tbl dollar {num1} na rm equals true
139:30
coord flip
140:00
labs title equals {topic} by {cat1} subtitle equals median {num1} per group caption equals source tidytuesday {date_str}
140:30
theme minimal base size equals 13 plus theme plot title equals element text face equals bold
141:00
that is the communication chart i am happy with that
141:30
now let me capture the reusable pattern
142:00
the workflow for this episode is load inspect pivot or join compare with group by summarize model with lm and then visualize with geom col plus annotation
142:30
i should write this into a function that takes any data frame with a numeric outcome and a categorical grouping
143:00
function name compare groups by outcome
143:30
arguments data group col outcome col model equals true
144:00
this function would wrap the group by summarize arrange and ggplot steps
144:30
and optionally run the lm and coefficient plot as well
145:00
that is the kind of thing that belongs in r slash screencast helpers dot r
145:30
alright that is three hours of analysis on {topic.lower()} thanks for joining
146:00
the main findings are
146:30
one {cat1} is strongly predictive of {num1}
147:00
two there are notable outliers in both directions worth investigating further
147:30
three a linear model explains a meaningful fraction of the variance
148:00
and the reusable pattern is load inspect pivot or join model communicate
148:30
see you next week"""

    return _wrap_header(title, topic, date_str, spoken_date, hour1 + "\n" + hour2 + "\n" + hour3)


def _wrap_header(title, topic, date_str, spoken_date, body):
    return f"""\
{title}

David Robinson
15.9k subscribers


72


Share

Save

Clip

4,521 views  Streamed live on {spoken_date}  Tidy Tuesday R Screencasts
I'll analyze a dataset about {topic.lower()} without looking at the dataset in advance.

The dataset comes from the Tidy Tuesday project: https://github.com/rfordatascience/tidytuesday/

Code: https://github.com/dgrtwo/data-screencasts


Search in video
{body}""".strip()


# ---------------------------------------------------------------------------
# Main  — pass depth="1h" / "2h" / "3h" (default "3h")
# ---------------------------------------------------------------------------

def main(depth: str = "3h", force: bool = False):
    """
    depth : "1h" | "2h" | "3h"
    force : if True, regenerate even if transcript_file already set
    """
    with open(CT_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    processed = 0
    skipped_no_readme = 0
    skipped_already_done = 0

    for row in rows:
        if row.get("ker_status", "").strip() != "needs_mapping":
            continue
        if row.get("transcript_file", "").strip() and not force:
            skipped_already_done += 1
            continue

        date_str = extract_date_from_source(row.get("data_source", ""))
        if not date_str:
            skipped_no_readme += 1
            continue

        readme_path = find_readme(date_str)
        if readme_path is None:
            skipped_no_readme += 1
            continue

        readme_info = parse_readme(readme_path)
        data_files  = find_data_files(date_str)

        fn    = row.get("function_name", "").replace("_", " ").title()
        title = row.get("transcript_title", f"Analyzing {fn} in R")
        topic = re.sub(r"^Analyzing\s+", "", title, flags=re.IGNORECASE)
        topic = re.sub(r"\s+in\s+R$", "", topic, flags=re.IGNORECASE).strip()

        content = generate_transcript(
            title=title, topic=topic, date_str=date_str,
            readme_info=readme_info, data_files=data_files, depth=depth,
        )

        out_file = INSPIRATION_DIR / f"{title}.txt"
        out_file.write_text(content, encoding="utf-8")
        row["transcript_file"] = f"raw-data/inspiration/{title}.txt"
        processed += 1

    with open(CT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Depth tier            : {depth}")
    print(f"Transcripts generated : {processed}")
    print(f"Skipped (no readme)   : {skipped_no_readme}")
    print(f"Skipped (already done): {skipped_already_done}")
    print(f"Total rows            : {len(rows)}")


if __name__ == "__main__":
    import sys
    depth_arg = sys.argv[1] if len(sys.argv) > 1 else "3h"
    force_arg = "--force" in sys.argv
    main(depth=depth_arg, force=force_arg)
