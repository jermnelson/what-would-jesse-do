"""Common components and data loading for WWJD website"""
__author__ = "Jeremy Nelson"

import datetime
import pathlib
import random

import markdown

from puepy import Component, t
from puepy.core import html


# Years for Jesse's life
ALL_YEARS = list(range(1981, 2026))

# Load topics/cards by scanning doc/topics directory
topics_by_category = {}
all_topics = []

topics_path = pathlib.Path("doc/topics")
for category_dir in topics_path.iterdir():
    if category_dir.is_dir():
        category_topics = []
        for topic_file in category_dir.glob("*.md"):
            category_topics.append(topic_file)
        topics_by_category[category_dir.name] = sorted(category_topics)
        all_topics.extend(category_topics)

# Load general topics
for general_topic in topics_path.glob("*.md"):
    all_topics.append(general_topic)
    if "general" not in topics_by_category:
        topics_by_category["general"] = []
    topics_by_category["general"].append(general_topic)

all_topics = sorted(all_topics)


# Life sections metadata
LIFE_SECTIONS = [
    {
        "id": "jesse-childhood",
        "title": "Childhood",
        "file": "doc/jesse-childhood.md",
        "years": [1981, 1982, 1983, 1984, 1985, 1986, 1987]
    },
    {
        "id": "pre-teen-and-teen",
        "title": "Pre-teen & Teen",
        "file": "doc/jesse-pre_teen-teen.md",
        "years": [1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996]
    },
    {
        "id": "high-school-and-after",
        "title": "High School and After",
        "file": "doc/jesse-high_school-after.md",
        "years": [1997, 1998, 1999, 2000, 2001]
    },
    {
        "id": "early-2000s",
        "title": "The Early 2000s",
        "file": "doc/jesse-early-2000s.md",
        "years": [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
    },
    {
        "id": "2010s-and-teens",
        "title": "The 2010s and Teens",
        "file": "doc/jesse-2010s-teens.md",
        "years": [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    },
    {
        "id": "last-years",
        "title": "The Last Years",
        "file": "doc/jesse-last-years.md",
        "years": [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    }
]

# WWJD items
WWJD_ITEMS = [
    "To make a profit selling pizza, all ingredients matter and should be each be weighed to insure consistency from pie-to-pie.",
    "The second most important piece of a pothead's kit is a lighter. A pipe can be made from anything.",
    "Count your yawns when driving. If you yawn four times in succession, you are too tired to drive. Pull over and rest or have someone else drive.",
    'To win at <a href="https://www.denverbroncos.com">football</a>, start with the Base Defense and a good running back.',
    "Marry the love of your life and be blessed with two sons",
    'Pizza and Pot are <a href="https://en.wikipedia.org/wiki/Complementary_good">complementary goods</a>',
    "Watch less Television",
    'Watch <a href="https://en.wikipedia.org/wiki/Office_Space">Office Space</a>',
    "Be a night owl and early bird but take lots of naps",
    "If all your goats have names; they are pets and not livestock",
    "Cover a Bob Dylan song at your local bar's Open Mic",
    "If you can't stop picking out your eyebrows, just shave them off",
]


@t.component()
class NavBar(Component):
    """Navigation bar component"""

    def populate(self):
        with t.nav(classes=["navbar", "navbar-expand-lg", "bg-body-tertiary"]):
            with t.div(classes=["container-fluid"]):
                t.a("WWJD?", href="#/", classes=["navbar-brand"])
                with t.button(
                    classes=["navbar-toggler"],
                    type="button",
                    data_bs_toggle="collapse",
                    data_bs_target="#navbarSupportedContent",
                    aria_controls="navbarSupportedContent",
                    aria_expanded="false",
                    aria_label="Toggle navigation"
                ):
                    t.span(classes=["navbar-toggler-icon"])

                with t.div(classes=["collapse", "navbar-collapse"], id="navbarSupportedContent"):
                    with t.ul(classes=["navbar-nav", "me-auto", "mb-2", "mb-lg-0"]):
                        with t.li(classes=["nav-item"]):
                            t.a("Home", href="#/", classes=["nav-link", "active"], aria_current="page")

                        with t.li(classes=["nav-item"]):
                            t.a("About", href="#/about", classes=["nav-link"])

                        # Jesse's Life dropdown
                        with t.li(classes=["nav-item", "dropdown"]):
                            t.a(
                                "Jesse's Life",
                                href="#",
                                role="button",
                                classes=["nav-link", "dropdown-toggle"],
                                data_bs_toggle="dropdown",
                                aria_expanded="false"
                            )
                            with t.ul(classes=["dropdown-menu"]):
                                for section in LIFE_SECTIONS:
                                    with t.li():
                                        t.a(section["title"], href=f"#/life/{section['id']}", classes=["dropdown-item"])

                        # Timeline dropdown
                        with t.li(classes=["nav-item", "dropdown"]):
                            t.a(
                                "Timeline",
                                href="#",
                                role="button",
                                classes=["nav-link", "dropdown-toggle"],
                                data_bs_toggle="dropdown",
                                aria_expanded="false"
                            )
                            with t.ul(classes=["dropdown-menu"]):
                                for year in ALL_YEARS:
                                    with t.li():
                                        t.a(str(year), href=f"#/years/{year}", classes=["dropdown-item"])

                        with t.li(classes=["nav-item"]):
                            t.a("Coming soon", href="#", classes=["nav-link", "disabled"], aria_disabled="true")

                    # Search form
                    with t.form(classes=["d-flex"], role="search"):
                        t.input(type="search", placeholder="Search", aria_label="Search", classes=["form-control", "me-2"])
                        t.button("Search", type="submit", classes=["btn", "btn-outline-success"])


@t.component()
class TopicCard(Component):
    """Card component for displaying a memory/topic"""
    props = ["topic_path"]

    def populate(self):
        topic_path = pathlib.Path(self.topic_path)
        if not topic_path.exists():
            return

        # Parse markdown with metadata
        md = markdown.Markdown(extensions=['meta'])
        content = topic_path.read_text()
        html_content = md.convert(content)

        # Extract metadata
        title = md.Meta.get("title", [""])[0] if hasattr(md, "Meta") and md.Meta else topic_path.stem
        author = md.Meta.get("author", ["Unknown"])[0] if hasattr(md, "Meta") and md.Meta else "Unknown"
        years = md.Meta.get("years", [])[0].split(",") if hasattr(md, "Meta") and md.Meta else []

        # Extract author name (remove ORCID if present)
        author_name = author.split("<")[0].strip() if "<" in author else author

        with t.div(classes=["card"], style="width: 18rem;"):
            # Card body
            with t.div(classes=["card-body"]):
                t.h5(title, classes=["card-title"])
                t.h5(author_name, classes=["card-subtitle", "mb-2", "text-body-secondary"])
                t(html(html_content))

            # Card footer with years
            if years:
                with t.div(classes=["card-footer", "text-body-secondary"]):
                    with t.strong():
                        t.text("Year(s): ")
                    for i, year in enumerate(years):
                        year_num = year.strip()[1:]  # Remove leading 0
                        t.a(year_num, href=f"#/years/{year_num}")
                        if i < len(years) - 1:
                            t.text(", ")


@t.component()
class WWJDWidget(Component):
    """WWJD widget with reveal functionality"""

    def initial(self):
        return {"visible_count": 5}

    def populate(self):
        with t.div(classes=["row"]):
            with t.div(classes=["col"]):
                t.img(
                    src="static/imgs/jerms-jesse.jpg",
                    alt="Jeremy and Jesse Nelson",
                    style="width: 420px"
                )

            with t.div(classes=["col"]):
                t.h4("I will leave you with my own list of WWJDs:")
                with t.ul():
                    for i, item in enumerate(WWJD_ITEMS):
                        classes = ["wwjd"]
                        if i >= self.state["visible_count"]:
                            classes.append("d-none")
                        t.li(item, classes=classes, __raw=True)

                if self.state["visible_count"] < len(WWJD_ITEMS):
                    t.button("More", classes=["btn", "btn-success"], on_click=self.reveal_wwjd)
                t.br()

    def reveal_wwjd(self, event):
        """Reveal one more WWJD item"""
        if self.state["visible_count"] < len(WWJD_ITEMS):
            self.state["visible_count"] += 1


@t.component()
class LifeSection(Component):
    """Component for a life section loaded from markdown"""
    props = ["section_id"]

    def populate(self):
        # Find the section metadata
        section_info = None
        for section in LIFE_SECTIONS:
            if section["id"] == self.section_id:
                section_info = section
                break

        if not section_info:
            t.p("Section not found")
            return

        # Load and parse markdown
        section_path = pathlib.Path(section_info["file"])
        if not section_path.exists():
            t.p(f"File not found: {section_info['file']}")
            return

        md = markdown.Markdown(extensions=['meta'])
        content = section_path.read_text()
        html_content = md.convert(content)

        with t.article(classes=["col"], id=self.section_id):
            t(html(html_content))

            # Year links
            if section_info.get("years"):
                with t.div(classes=["alert", "alert-secondary"], role="alert"):
                    with t.ul(classes=["list-inline"]):
                        for year in section_info["years"]:
                            with t.li(classes=["list-inline-item"]):
                                t.a(str(year), href=f"#/years/{year}")


@t.component()
class Footer(Component):
    """Footer component"""

    def populate(self):
        with t.footer(classes=["mt-5", "text-center", "text-muted"]):
            t.p("© 2025 Jeremy Nelson")
