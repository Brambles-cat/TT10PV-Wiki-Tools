from urllib.parse import urlparse, parse_qs, ParseResult
from googleapiclient.discovery import build
from modules.dtypes import VideoData
import requests, csv, io, os, re

_yt_api_key = os.getenv("yt_api_key")
_yt_service = build("youtube", "v3", developerKey=_yt_api_key)

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


def fetch_video(url) -> VideoData:
    url_components = urlparse(url)
    
    return _fetch_yt(url_components) if url_components.netloc in [
        "m.youtube.com", "www.youtube.com", "youtube.com", "youtu.be"
    ] else _fetch_ytdlp(url)

def get_archive(archive_url: str):
    response = requests.get(archive_url)
    
    csv_reader = csv.reader(io.StringIO(response.text))
    archive_rows = [row for row in csv_reader]
    del archive_rows[0]

    return archive_rows


def _fetch_yt(url_components: ParseResult) -> str:
    video_id = None
    path = url_components.path
    query_params = parse_qs(url_components.query)

    # Regular YouTube URL: eg. https://www.youtube.com/watch?v=9RT4lfvVFhA
    if path == "/watch":
        video_id = query_params["v"][0]
    else:
        livestream_match = re.match("^/live/([a-zA-Z0-9_-]+)", path)
        shortened_match = re.match("^/([a-zA-Z0-9_-]+)", path)

        if livestream_match:
            # Livestream URL: eg. https://www.youtube.com/live/Q8k4UTf8jiI
            video_id = livestream_match.group(1)
        elif shortened_match:
            # Shortened YouTube URL: eg. https://youtu.be/9RT4lfvVFhA
            video_id = shortened_match.group(1)
        else:
            raise Exception("Url missing video id")
    
    request = _yt_service.videos().list(
        part="status,snippet,contentDetails", id=video_id
    )

    response = request.execute()

    if not response or not response["items"]:
        raise Exception(
            f"Couldn't request URL {url_components.geturl()} or response from YouTube Data API did not contain any items"
        )

    response_item = response["items"][0]
    snippet = response_item["snippet"]

    return VideoData(
        description=snippet["description"],
        thumbnail=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        details=[
            f"Creator: {snippet["channelTitle"]}",
            f"Publish Date: {snippet["publishedAt"]}",
            f"Captions: {response_item["contentDetails"]["caption"]}"
        ]
    )

def _fetch_ytdlp(url):
    pass
