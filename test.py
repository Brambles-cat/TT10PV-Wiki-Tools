from modules.archive import get_archive
from modules.archive import ArchiveIndices as I
import os, dotenv, re

dotenv.load_dotenv()
archive_url = os.getenv("archive_url")

archive_rows = get_archive(archive_url)

paths = {}

for i, row in enumerate(archive_rows):    
    title = row[I.TITLE]
    sanitized_title = title.replace("\\", "\\\\").replace("\"", "\\\"")
    sanitized_path = re.sub("[_ -]+", "_", re.sub("[^a-zA-Z0-9_ -]", "", title))

    if len(sanitized_path) < 2: # debug
        pass

    if sanitized_path in paths:
        paths[sanitized_path] += 1
    else:
        paths[sanitized_path] = 1
    

paths = {path: count for path, count in paths.items() if count > 1}
for path, count in paths.items():
    print(f"{count} : {path}")