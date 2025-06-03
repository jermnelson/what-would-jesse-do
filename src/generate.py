"""Static site generator for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"
import argparse
import datetime
import os
import pathlib

import markdown

from jinja2 import Environment, FileSystemLoader, select_autoescape

from topics import load

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
    converted_to_html = markdown.markdown(file_path.read_text(),extensions=['meta'] )
    return converted_to_html
   

def get_years(file_name: str):
    file_path = root_path / f"doc/{file_name}.md"
    if not file_path.exists():
        raise ValueError(f"{file_name} does not exist at {file_path}")
    md = markdown.Markdown(extensions=['meta'])
    md.convert(file_path.read_text())
    return [year.strip() for year in md.Meta.get("years")[0].split(",")]


env.filters["from_mkdwn"] = from_markdown
env.filters["get_years"] = get_years

def cards(site_path: pathlib.Path, prefix: str=""):
    all_topics = load()
    return all_topics
    
def cards_lookup(topics: list) -> dict:
    lookup = {}
    for topic in topics:
        for year in topic.years:
            year_num = int(year[1:])
            if year_num in lookup:
                lookup[year_num].append(topic)
            else:
                lookup[year_num] = [topic]
    return lookup

def timeline(site_path: pathlib.Path, prefix: str="", all_cards: list=None):
    years = site_path / "years"
    year_template = env.get_template("year.html")
    if all_cards is None:
        all_cards = []
    cards_by_year = cards_lookup(all_cards)
    for year in all_years:
        year_md = site_path / f"doc/years/0{year}.md"
        content = None
        if year_md.exists():
            content = markdown.markdown(year_md.read_text(), extensions=['meta'])
        year_html = year_template.render(
                        year=year,
                        timeline=all_years,
                        content=content, 
                        prefix=prefix, 
                        cards=cards_by_year.get(year, []),
                        image_prefix="../")
        year_path = years / f"0{year}.html"
        with year_path.open("w+") as fo:
            fo.write(year_html)
        print(f"\t{year} Generated {year_path.absolute()}")    


def website(**kwargs):
    generate_date: datetime.Datetime = kwargs["generation_date"]
    site_path: pathlib.Path = kwargs["site_path"]
    prefix: str = kwargs.get("prefix", "")
    home_template = env.get_template("index.html")
    all_cards = cards(site_path=site_path, prefix=prefix)
    home_page = home_template.render(
        generated_on=generation_date,
        prefix=prefix,
        timeline=all_years,
        cards=all_cards
    )
    
    index_page_path = site_path / "index.html"
    with index_page_path.open("w+") as fo:
        fo.write(home_page)

    print(f"\t{index_page_path.absolute()}")
    return all_cards

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix", help="URL prefix for publishing to Github", default="/what-would-jesse-do")
    args = parser.parse_args()
    prefix = args.prefix
    site_path = pathlib.Path(".")
    generation_date = datetime.datetime.now(datetime.UTC)
    print(f"Generating website on {generation_date.isoformat()} {prefix}")
    all_cards = website(generation_date=generation_date, site_path=site_path, prefix=prefix)
    timeline(site_path, prefix, all_cards)
    
