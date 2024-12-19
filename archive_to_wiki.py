from modules.external import get_archive, ArchiveIndices as I
from modules.wiki import Wiki
import os, dotenv

dotenv.load_dotenv()
archive_url = os.getenv("archive_url")
wiki_api_key = os.getenv("wiki_api_key")
domain = os.getenv("wiki_domain")

wiki = Wiki(wiki_api_key, domain)

archive_rows = get_archive(archive_url)

base_template = "templates/t10video_base.html"
updated_template = "templates/t10video_updated.html"


if True:
    for i, row in enumerate(archive_rows[:3]):
        wiki.create_top10v_page(row, base_template)
        print(f"wiki page #{i+1} made")

input(".")

t10v_ids = wiki.get_top10v_ids()

for i, row in enumerate(archive_rows[:3]):
    ids = next(ids for ids in t10v_ids if ids["path"].endswith(wiki._path_sanitize(row[I.TITLE])))

    wiki.update_top10v_page(ids["id"], row, updated_template)
    print(f"wiki page {ids["path"]} updated")