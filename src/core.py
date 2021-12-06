import json
import logging
from typing import Tuple, Optional, Any, Dict

import requests
from bs4 import BeautifulSoup

from src.errors import FetchDataError

logger = logging.getLogger(__name__)


def transform(data: Dict[str, Any]) -> Tuple[str, str]:
    """Extract title and artists from parsed JSON data.

    :param data: string containing title and artist
    :return: title and artist
    """
    logger.info("Getting title and artist(s)...")
    artists = ", ".join([artist["name"] for artist in data["artists"]])
    title = data["name"]
    return title, artists


def extract(raw_response: str) -> Optional[Dict[str, Any]]:
    """Extract the relevant data from a HTML page that contains information
    about a Spotify song

    :param raw_response: complete content of a html page as a string
    :return: JSON data  that contains title and artist
    """
    logger.info("Parsing raw HTML...")
    tree = BeautifulSoup(raw_response, "html.parser")
    script_tag = tree.find_all("script")
    for tag in script_tag:
        if "Spotify.Entity" in tag.text:
            jsonentity = tag.text.split("Spotify.Entity = ")[1]
            # [:-1] data ends with a semicolon which must be removed for valid JSON
            return json.loads(jsonentity.strip()[:-1])
    return None


def get_data(url: str) -> Dict[str, Any]:
    """
    Retrieve title and artist from the URL that displays information about a song
     on Spotify
    :param url: url to the song
    :return: title and artist
    """
    # requests error handling follows:
    # https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

    try:
        response = requests.get(url=url)
        response.raise_for_status()
        unparsed = response.content.decode("utf-8")
    except requests.exceptions.HTTPError as error:
        raise FetchDataError(
            f"A HTTP error occurred while fetching song data:\n{error}"
        )
    except requests.exceptions.RequestException as error:
        raise FetchDataError(f"An error occurred while fetching song data:\n{error}")

    return extract(unparsed)
