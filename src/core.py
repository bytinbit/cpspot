import json
import logging
import sys
from typing import Tuple, Optional, Any, Dict

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

URL = "https://open.spotify.com/track/5lQdYxYl9okxBXtnSN8iJI?si=0e7aa3db079c42c5&nd=1"

def extract(raw_response: str) -> Optional[Dict[str, Any]]:
    """Extract the relevant data from a HTML page that contains information
    about a Spotify song

    :param raw_response: complete content of a html page as a string
    :return: JSON data  that contains title and artist
    """
    tree = BeautifulSoup(raw_response, "html.parser")
    script_tag = tree.find_all("script")
    for tag in script_tag:
        if "Spotify.Entity" in tag.text:
            jsonentity = tag.text.split("Spotify.Entity = ")[1]
            return json.loads(jsonentity.strip()[:-1])
    return None


def transform(data: Dict[str, Any]) -> Tuple[str, str]:
    """Extract title and artists from parsed JSON data.

    :param data: string containing title and artist
    :return: title and artist
    """
    artists = ", ".join([artist["name"] for artist in data["artists"]])
    title = data["name"]
    return title, artists


def get_data(url: str) -> Tuple[str, str]:
    """
    Retrieve title and artist from the URL that displays information about a song
     on Spotify
    :param url: url to the song
    :return: title and artist
    """
    # error handling following:
    # https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
    unparsed = ""

    try:
        response = requests.get(url=url)
        response.raise_for_status()
        unparsed = response.content.decode("utf-8")
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    raw = extract(unparsed)
    if not raw:
        # Fixme niceify error-handling
        logger.info("Could not find relevant information on website content")
        sys.exit(1)

    return transform(raw)
