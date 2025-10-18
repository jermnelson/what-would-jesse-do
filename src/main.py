"""Main application for What Would Jesse Do?"""
__author__ = "Jeremy Nelson"

import pathlib

import markdown

from puepy import Application, Page, t
from puepy.router import Router
from puepy.core import html
from puepy.exceptions import NotFound

from common import (
    NavBar, TopicCard, WWJDWidget, LifeSection, Footer,
    all_topics, LIFE_SECTIONS, ALL_YEARS
)


app = Application()
app.install_router(Router, link_mode=Router.LINK_MODE_HASH)


@app.page("/years/<year>")
class YearPage(Page):
    """Page showing all content for a specific year"""
    props = ["year"]

    def populate(self):
        year_num = int(self.year)
        if year_num not in ALL_YEARS:
            raise NotFound()

        t.navbar()

        with t.div(classes=["container"]):
            t.h1(f"Year {year_num}", classes=["text-center", "my-4"])

            # Find life section for this year
            relevant_section = None
            for section in LIFE_SECTIONS:
                if year_num in section["years"]:
                    relevant_section = section
                    break

            if relevant_section:
                t.life_section(section_id=relevant_section["id"])

            # Find and display relevant topic cards
            relevant_topics = []
            for topic_path in all_topics:
                md = markdown.Markdown(extensions=['meta'])
                content = topic_path.read_text()
                md.convert(content)
                if hasattr(md, "Meta") and md.Meta:
                    years = md.Meta.get("years", [])
                    if years:
                        year_list = years[0].split(",")
                        # Check if this year matches
                        for y in year_list:
                            if y.strip()[1:] == str(year_num) or y.strip() == f"0{year_num}":
                                relevant_topics.append(topic_path)
                                break

            if relevant_topics:
                t.h2("Memories from this year", classes=["mt-5"])
                with t.div(classes=["row", "mb-3"]):
                    for topic_path in relevant_topics:
                        with t.div(classes=["col-md-4", "mb-3"]):
                            t.topic_card(topic_path=str(topic_path))

        t.footer()


@app.page("/life/<section_id>")
class LifeSectionPage(Page):
    """Page for a specific life section"""
    props = ["section_id"]

    def populate(self):
        # Verify section exists
        section_info = None
        for section in LIFE_SECTIONS:
            if section["id"] == self.section_id:
                section_info = section
                break

        if not section_info:
            raise NotFound()

        t.navbar()

        with t.div(classes=["container"]):
            t.h1(section_info["title"], classes=["text-center", "my-4"])
            t.life_section(section_id=self.section_id)

        t.footer()


@app.page()
class HomePage(Page):
    """Main home page"""

    def populate(self):
        t.navbar()

        with t.div(classes=["container"]):
            # Main heading
            t.h1("What Would Jesse Do?", classes=["text-center", "mt-4"])
            t.h2("An Oldest Brother Eulogy for Jesse Robert Nelson (1981-2025)", classes=["text-center"])
            t.h3("By Jeremy Nelson", classes=["text-center", "mb-4"])

            # Introduction
            intro_path = pathlib.Path("doc/jesse-eulogy-intro.md")
            if intro_path.exists():
                md = markdown.Markdown(extensions=['meta'])
                intro_content = md.convert(intro_path.read_text())

                with t.div(classes=["row"], id="intro"):
                    with t.div(classes=["col-md-6"]):
                        t(html(intro_content))

                    with t.div(classes=["col-md-6"]):
                        with t.figure(classes=["figure"]):
                            t.img(
                                src="static/imgs/family-jesse-funeral.jpg",
                                classes=["figure-img", "img-fluid", "rounded"],
                                alt="Family Portrait at Jesse Nelson's Kief 29 March 02025 Funeral"
                            )
                            with t.figcaption(classes=["figure-caption"]):
                                t.text("""(left-to-right) Judd Nelson, Jarrett Nelson (holding Jesse's ashes), Jake Nelson (back row), Carolyn Nelson, Jill Case, Jeremy Nelson (back row),
       Angie Belknap, Paul Nelson""")

                        t.img(
                            src="static/imgs/WWJD_QR.png",
                            style="width: 300px",
                            classes=["rounded"],
                            alt="QR Code for Eulogy"
                        )

            t.hr()

            # Warning alert
            with t.div(classes=["alert", "alert-light"], role="alert"):
                t.text("An important disclosure - there are times when you certainly should ")
                t.strong("NOT")
                t.text(" do what Jesse would do! Like smoking cigarettes")
                t.p("🚭", style="font-size: 3em;", classes=["text-center"])

            t.hr()

            # Life sections
            with t.div(classes=["row"]):
                t.life_section(section_id="jesse-childhood")
                t.life_section(section_id="pre-teen-and-teen")

            t.hr()

            with t.div(classes=["row"]):
                t.life_section(section_id="high-school-and-after")
                t.life_section(section_id="early-2000s")

            t.hr()

            with t.div(classes=["row"]):
                t.life_section(section_id="2010s-and-teens")
                t.life_section(section_id="last-years")

            t.hr()

            # Final thoughts
            final_path = pathlib.Path("doc/jesse-eulogy-final-thoughts.md")
            if final_path.exists():
                md = markdown.Markdown()
                final_content = md.convert(final_path.read_text())
                t(html(final_content))

            t.hr()

            # WWJD Widget
            t.wwjd_widget()

            t.hr()

            # Cards section
            with t.div(classes=["row"]):
                with t.div(classes=["col"]):
                    t.p("""Please email me at <a href="mailto:jermnelson@gmail.com">jermnelson@gmail.com</a> or submit a
Github <a href="https://github.com/jermnelson/what-would-jesse-do/issues">WWJD? Card Ticket</a>. I'll add your memories, photos,
and your own WWJD?s to this website. You can also clone the
<a href="https://github.com/jermnelson/what-would-jesse-do/">repository</a> and do a pull-request (I'll help ☺)""", __raw=True)

            # Display all topic cards in groups of 3
            for i in range(0, len(all_topics), 3):
                batch = all_topics[i:i+3]
                with t.div(classes=["row", "mb-3"]):
                    for topic_path in batch:
                        with t.div(classes=["col-md-4"]):
                            t.topic_card(topic_path=str(topic_path))

        t.footer()


app.mount("#app")
