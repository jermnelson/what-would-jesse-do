"""Static site generator for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"
import datetime
import pathlib

import markdown

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("src/templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

all_years = range(1981, 2026)

def timeline(site_path: pathlib.Path):
    years = site_path / "years"
    year_template = env.get_template("year.html")
    for year in all_years:
        year_html = year_template.render(year=year, timeline=all_years)
        year_path = years / f"0{year}.html"
        with year_path.open("w+") as fo:
            fo.write(year_html)
        print(f"\t{year} Generated {year_path.absolute()}")    


def website(**kwargs):
    generate_date: datetime.Datetime = kwargs["generation_date"]
    site_path: pathlib.Path = kwargs["site_path"]
    home_template = env.get_template("index.html")
    home_page = home_template.render(
        generated_on=generation_date,
        timeline=all_years
    )
    
    index_page_path = site_path / "index.html"
    with index_page_path.open("w+") as fo:
        fo.write(home_page)

    print(f"\t{index_page_path.absolute()}")

if __name__ == "__main__":
    site_path = pathlib.Path(".")
    generation_date = datetime.datetime.now(datetime.UTC)
    print(f"Generating website on {generation_date.isoformat()}")
    website(generation_date=generation_date, site_path=site_path)
    timeline(site_path)
    
