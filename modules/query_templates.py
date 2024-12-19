_create_page = """mutation {{
    pages {{
        create(
            content: "{0}"
            description: "{1}"
            editor: "markdown"
            isPublished: true
            isPrivate: false
            locale: "en"
            path: "{2}"
            scriptCss: "{3}"
            tags: []
            title: "{4}"
        ) {{
            page {{
                id
            }}
        }}
    }}
}}"""

_update_page = """mutation {{
    pages {{
        update(
            id: {0}
            content: "{1}"
            scriptCss: "{2}"
            isPublished: true
        ) {{
            page {{
                id
            }}
        }}
    }}
}}"""

_get_page = """query {{
    pages {{
        single(id: {0}) {{
            content
            scriptCss
        }}
    }}
}}"""

get_page_ids = """query {
    pages {
        list(orderBy: PATH, orderByDirection: DESC) {
            path
            id
        }
    }
}"""


def create_page(content: str, description: str, css: str, path: str, title: str):
    return _create_page.format(content, description, path, css, title)

def update_page(page_id: int, content: str, css: str):
    return _update_page.format(page_id, content, css)

def get_page(page_id):
    return _get_page.format(page_id)
