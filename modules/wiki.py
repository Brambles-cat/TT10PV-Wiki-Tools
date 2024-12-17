from modules.external import ArchiveIndices as I
from modules.page_templates import TemplateBuilder
from modules.query_templates import create_page
import requests, re


class Wiki():
    """API wrapper class for the Top 10 Pony Videos Wikijs instance"""

    _builder = TemplateBuilder()

    def __init__(self, wiki_api_key: str=None, wiki_domain: str=None):
        """Initialize the Wiki API wrapper

        If no arguments are given, the instance will output the page HTML and CSS to a local file"""

        if bool(wiki_domain) != bool(wiki_domain):
            raise ValueError("Expected either both arguments or none, recieved only 1")
        
        self._wiki_api_key = wiki_api_key
        self._domain = wiki_domain

    def create_top10v_page(self, archive_row):
        """Create a new top 10er wiki page from the corresponding archive row"""

        title = archive_row[I.TITLE]
        sanitized_title = self._api_sanitize(title)
        sanitized_path = self._path_sanitize(title)

        page_content, page_css = self._builder.build_top10v_page(archive_row)
        
        if not self._wiki_api_key:
            with open("output.txt", "w", encoding="utf-8") as output:
                output.write(page_content)
                output.write(f"<style>{page_css}</style>")
            return

        page_content = self._api_sanitize(page_content)
        page_css = self._api_sanitize(page_css)

        query = create_page(page_content, "", page_css, sanitized_path, sanitized_title)

        response = requests.post(
            f"http://{self._domain}/graphql",
            headers={
                "Authorization": f"Bearer {self._wiki_api_key}",
                "Content-Type": "application/json"
            },
            json={"query": query}
        )
    
        if response.status_code != 200 or not response.json()["data"]["pages"]["create"]["page"]:
            raise Exception("todo: make proper error message later")
        
    def _api_sanitize(self, string):
        """Sanitize string to prevent broken or invalid graphql queries upon insertion"""
        return string.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")

    def _path_sanitize(self, path):
        """Sanitize path by removing characters that would otherwise make invalid urls"""
        return re.sub("[_ -]+", "_", re.sub("[^a-zA-Z0-9_ -]", "", path))
