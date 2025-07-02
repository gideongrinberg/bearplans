import os
import re
import json
import polars as pl
from pathlib import Path
from datetime import datetime

catalog_name = input("Catalog name (e.g. Fall 2025): ").replace(" ", "_") + ".parquet"
pages_dir = Path(os.path.dirname(__file__)) / "pages"
catalogs_dir = Path(os.path.dirname(__file__)) / "catalogs"
try:
    os.mkdir(catalogs_dir)
except: # noqa: E722
    pass

title_regex = re.compile(r"^([A-Z\-]+)\s+(\d{4})(?:-([A-Z0-9]+))?\s+-\s+(.*)$")
schedule_regex = re.compile(r"^(?:(?P<location>.+?)\s*\|\s*)?(?P<days>(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:/(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun))*)\s*\|\s*(?P<start_time>\d{1,2}:\d{2}\s*[AP]M)\s*-\s*(?P<end_time>\d{1,2}:\d{2}\s*[AP]M)$")

def parse_time(time_str):
    """Convert HH:MM (AM|PM) to minutes"""
    time_obj = datetime.strptime(time_str.strip(), "%I:%M %p")
    return time_obj.hour * 60 + time_obj.minute

def process_item(item):
    try:
        course_title: str = item["title"]["instances"][0]["text"]
        course_title = course_title.strip()
    except:  # noqa: E722
        return None
    
    match = title_regex.match(course_title)
    try:
        assert match is not None
    except: # noqa: E722
        return None

    dept, code, section, name = match.groups()
    data = {
        "dept": dept,
        "code": f"{dept} {code}",
        "section": str(section) if section is not None else "",
        "name": name,
        "title": f"{dept} {code} - {name}",
    }

    details = {}
    for field in item["detailResultFields"]:
        label = field["label"]
        if "instances" in field and field["instances"]:
            details[label] = field["instances"][0]["text"]
        elif "value" in field:
            details[label] = field["value"]

    if schedule := details.get("Section Details"):
        match = schedule_regex.match(schedule)
        try:
            assert match is not None
        except: # noqa: E722
            return None
        
        data["days"] = match.group("days")
        data["start"] = parse_time(match.group("start_time"))
        data["end"] = parse_time(match.group("end_time"))
        data["instructor"] = details.get("Instructors")
    else:
        return None
    return data


def process_page(filename):
    with open(filename) as f:
        page = json.load(f)

    try:
        items = page["body"]["children"][0]["listItems"]
    except: # noqa: E722
        return
    
    classes = []
    for item in items:
        if (data := process_item(item)) is not None:
            classes.append(data)

    return classes

classes = []
for page in pages_dir.glob("*.json"):
    if (data := process_page(page)) is not None:
        classes.extend(data)

df = pl.from_dicts(classes)
df.write_parquet(catalogs_dir / catalog_name)