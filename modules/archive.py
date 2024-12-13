import requests, csv, io

class ArchiveIndices:
    YEAR = 0
    MONTH = 1
    RANK = 2
    LINK = 3
    TITLE = 4
    CHANNEL = 5
    UPLOAD_DATE = 6
    STATE = 7
    ALT_LINK = 8

def get_archive(archive_url: str):
    response = requests.get(archive_url)
    
    csv_reader = csv.reader(io.StringIO(response.text))
    archive_rows = [row for row in csv_reader]
    del archive_rows[0]

    return archive_rows
