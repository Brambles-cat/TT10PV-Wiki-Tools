from typing import TypedDict
from bs4 import PageElement

class VideoData(TypedDict):
    description: str
    thumbnail: str
    details: list[str]

class CreatorData:
    pass

class ElementChanges(TypedDict):
    attributes: dict[str, str] | None
    content: PageElement
