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

def create_page(content: str, description: str, css: str, path: str, title: str):
    return _create_page.format(content, description, path, css, title)
