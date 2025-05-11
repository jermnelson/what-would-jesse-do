"""Static site generator for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"
import argparse
import datetime
import os
import pathlib

import markdown

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("src/templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

all_years = range(1981, 2026)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = pathlib.Path(os.path.dirname(current_dir))

def from_markdown(file_name: str):
    file_path = root_path / f"doc/{file_name}.md"
    if not file_path.exists():
        raise ValueError(f"{file_name} does not exist at {file_path}")
    return markdown.markdown(file_path.read_text(),extensions=['meta'] )
    
env.filters["from_mkdwn"] = from_markdown

def timeline(site_path: pathlib.Path, prefix: str=""):
    years = site_path / "years"
    year_template = env.get_template("year.html")
    for year in all_years:
        year_html = year_template.render(year=year, timeline=all_years, prefix=prefix)
        year_path = years / f"0{year}.html"
        with year_path.open("w+") as fo:
            fo.write(year_html)
        print(f"\t{year} Generated {year_path.absolute()}")    


def website(**kwargs):
    generate_date: datetime.Datetime = kwargs["generation_date"]
    site_path: pathlib.Path = kwargs["site_path"]
    prefix: str = kwargs.get("prefix", "")
    home_template = env.get_template("index.html")
    home_page = home_template.render(
        generated_on=generation_date,
        prefix=prefix,
        timeline=all_years
    )
    
    index_page_path = site_path / "index.html"
    with index_page_path.open("w+") as fo:
        fo.write(home_page)

    print(f"\t{index_page_path.absolute()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix", help="URL prefix for publishing to Github", default="/what-would-jesse-do")
    args = parser.parse_args()
    prefix = args.prefix
    site_path = pathlib.Path(".")
    generation_date = datetime.datetime.now(datetime.UTC)
    print(f"Generating website on {generation_date.isoformat()}")
    website(generation_date=generation_date, site_path=site_path, prefix=prefix)
    timeline(site_path, prefix)
    
