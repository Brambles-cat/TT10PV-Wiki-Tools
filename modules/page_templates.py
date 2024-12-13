from bs4 import BeautifulSoup, PageElement

template_path = "templates/top10er.html"

class TemplateBuilder:
    _populators = {
        "test": lambda archive_row: archive_row[0],
        "top10er_description": lambda archive_row: "miugbmjkgbngfkvcbh"
    }
    _archive_row = None

    def build_top10er_template(self, archive_row: list[str]):
        self._archive_row = archive_row

        with open(template_path, "r") as html_file:
            soup = BeautifulSoup("".join(html_file.readlines()), "html.parser")
            self._populate(soup)
        
        return str(soup)

    def _keep(self, element_id):
        pass

    def _populate(self, element: PageElement | str):
        if isinstance(element, str): return

        children = list(element.children)
        element_id = element.get("id")

        if not element_id:
            for child in children:
                self._populate(child)
            return
        
        element.string = self._keep(element_id) if (
            len(children) and children[0] == "[keep]"
        ) else self._populators[element_id](self._archive_row)