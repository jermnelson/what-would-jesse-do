__author__ = "Jeremy Nelson"

from datetime import datetime
from pathlib import Path
from typing import Union

import markdown

from bs4 import BeautifulSoup
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    orchid: Union[str, None]


class Topic(BaseModel):
    title: str
    html: str
    card_images: list
    author: Author
    path: Path
    years: list


def parse_author(author: str) -> Author:
    parts = author.split("<")
    orchid = None
    if len(parts) == 2:
        orchid = parts[1].split(">")[0]
    name = parts[0]
    return Author(name=name.strip(), orchid=orchid)
    

def parse_html(raw_html: str) -> tuple:
    soup = BeautifulSoup(raw_html, 'html.parser')
    images = []
    for image in soup.find_all("img"):
        images.append({"alt": image.attrs.get('alt'), "source": image.attrs['src']})
        image.parent.decompose()
    return images, str(soup)

def load(topic_dir=None):
    """Loads all topics"""
    if topic_dir is None:
        current_dir = Path(__file__)
        topic_dir = current_dir.parent.parent / "doc/topics"
    md = markdown.Markdown(extensions=['meta'])
    topics = []
    for mrk_dwn_path in topic_dir.rglob("*.md"):
        topic_markdown = md.convert(mrk_dwn_path.read_text())
        author = parse_author(md.Meta.get("author")[0])
        images, html = parse_html(topic_markdown)
        topic = Topic(
            title=md.Meta.get("title")[0],
            html=html,
            card_images=images,
            path=mrk_dwn_path,
            author=author,
            years=md.Meta.get("years")
        )
        topics.append(topic)
    return topics

if __name__ == "__main__":
    load()
 
