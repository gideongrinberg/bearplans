import os
import json
import polars as pl
from glob import glob
from pathlib import Path
from collections import defaultdict

def load_catalogs():
    catalogs = {}
    for catalog in glob(str(Path(os.path.dirname(__file__)) / "catalogs" / "*.parquet")):
        name = os.path.basename(catalog).split(".")[0]
        name = name.replace("_", " ")
        df = pl.read_parquet(catalog)
        
        courses = {
            row["title"]: row["code"]
            for row in df.select(["title", "code"]).unique().sort(pl.col("title")).iter_rows(named=True)
        }

        catalogs[name] = {
            "courses": courses,
            "sections": get_sections_dict(df)
        }

    return catalogs

def get_sections_dict(df: pl.DataFrame):
    """Takes a catalog and returns a dictionary of courses and their sections"""
    sections = defaultdict(list)
    for code in df["code"].unique().to_list():
        course = df.filter(pl.col("code") == code)
        for section in course.iter_rows(named=True):
            sections[code].append(
                {
                    "id": f"{code}-{section['section']}",
                    "days": section["days"].split("/"),
                    "start": section["start"],
                    "end": section["end"],
                    "instructor": section["instructor"],
                }
            )

    return sections

if __name__ == "__main__":
    with open(Path(os.path.dirname(__file__)) / "../app/src/lib/data/catalogs.json", "w") as f:
        json.dump(load_catalogs(), f)