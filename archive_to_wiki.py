from modules.archive import get_archive
from modules.wiki import Wiki
import os, dotenv

dotenv.load_dotenv()
archive_url = os.getenv("archive_url")
wiki_api_key = os.getenv("wiki_api_key")

wiki = Wiki(wiki_api_key)

archive_rows = get_archive(archive_url)


for i, row in enumerate(archive_rows[-5:]):
    wiki.create_top10er_page(row)