from modules.archive import ArchiveIndices as I
from modules.page_templates import TemplateBuilder
from modules.query_templates import create_page
import requests, re


class Wiki():
    def __init__(self, wiki_api_key: str):
        self._wiki_api_key = wiki_api_key
        self.builder = TemplateBuilder()

    def create_top10er_page(self, row):
        title = row[I.TITLE]
        sanitized_title = title.replace("\\", "\\\\").replace("\"", "\\\"")
        sanitized_path = re.sub("[_ -]+", "_", re.sub("[^a-zA-Z0-9_ -]", "", title))

        page_content = self.builder.build_top10er_template(row)
        page_content = page_content.replace("\n", "\\n").replace("\"", "\\\"")
        query = create_page(page_content, "", sanitized_path, sanitized_title)

        response = requests.post(
            "http://raspberrypi/graphql",
            headers={
                "Authorization": f"Bearer {self._wiki_api_key}",
                "Content-Type": "application/json"
            },
            json={"query": query}
        )
    
        if not response.json()["data"]["pages"]["create"]["page"]:
            raise Exception()