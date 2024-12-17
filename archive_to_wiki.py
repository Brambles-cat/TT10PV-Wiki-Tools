from modules.external import get_archive
from modules.wiki import Wiki
import os, dotenv

dotenv.load_dotenv()
archive_url = os.getenv("archive_url")
wiki_api_key = os.getenv("wiki_api_key")
domain = os.getenv("wiki_domain")

wiki = Wiki(wiki_api_key, domain)

archive_rows = get_archive(archive_url)


for i, row in enumerate(archive_rows[:3]):
    wiki.create_top10v_page(row)
    print(f"wiki page #{i+1} made")
