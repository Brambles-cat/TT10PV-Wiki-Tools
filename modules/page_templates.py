from bs4 import BeautifulSoup, Tag
from modules.external import fetch_video, VideoData, ArchiveIndices as I
from modules.dtypes import ElementChanges, PageData
from modules.query_templates import get_page
from typing import Callable
import requests


class TemplateBuilder:
    """Class for dynamically populating template html pages for the wiki"""

    _archive_row = None
    _video_cache: VideoData = None
    _page_cache = None

    def __init__(self, wiki_api_key: str, wiki_domain: str):
        self._wiki_api_key = wiki_api_key
        self._wiki_domain = wiki_domain

        # when making templates, element ids should only be from the same group as the page that's being created
        # e.g. don't use t10v_url with t10c_name in the same template
        self._populators: dict[str, Callable[[], ElementChanges]] = {
            "t10v_header": lambda: {
                "content": self._archive_row[I.TITLE]
            },
            "t10v_url": lambda: {
                "content": self._archive_row[I.LINK], "attributes": {
                    "href": self._archive_row[I.LINK]
                }
            },
            "t10v_desc": lambda: {
                "content": self._video_cache["description"]
            },
            "t10v_thumbnail": lambda: {
                "attributes": {
                    "src": self._video_cache["thumbnail"]
                }
            },
            "t10v_details": lambda: {
                "content": BeautifulSoup("<br>".join(self._video_cache["details"]), "html.parser")
            },
            "t10c_name": lambda: {}
        }

    def build_top10v_page(self, archive_row: list[str], template_path: str):
        """Populates the top 10er template with information about the video entry in the archive"""

        self._archive_row = archive_row
        self._video_cache = fetch_video(archive_row[I.LINK])

        with open(template_path, "r") as html_file:
            soup = BeautifulSoup("".join(html_file.readlines()), "html.parser")
            css = self._populate(soup)

        self._video_cache = None
        return str(soup), css

    def build_top10c_page(self):
        pass

    # Helper methods
    def _keep(self, element_id):
        if not self._page_cache:
            response = requests.post(
                f"http://{self._domain}/graphql",
                headers={
                    "Authorization": f"Bearer {self._wiki_api_key}",
                    "Content-Type": "application/json"
                },
                json={"query": get_page(element_id)}
            )
        # todo
        return None


    def _populate(self, element: Tag | str):
        if isinstance(element, str): return
        if element.name == "style":
            css = element.string
            element.decompose()
            return css

        children = list(element.children)
        element_id = element.get("id")

        if not element_id:
            # Assuming that any css used would be in a single style block, which
            # is fine since all templates should have it at the bottom
            for child in children:
                potentially_css = self._populate(child)
            return potentially_css
        
        if (len(children) and children[0]) == "[keep]":
            return element.append(self._keep(element_id))
        
        p = self._populators[element_id]()
        content, attributes = p.get("content"), p.get("attributes")
        
        if attributes:
            for attr, val in attributes.items():
                element[attr] = val

        if content:
            element.append(content)

    def _get_creator_data(self, creator_id):
        pass
