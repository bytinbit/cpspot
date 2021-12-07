import json
import logging
from typing import Tuple, Optional, Any, Dict, List

import requests
from bs4 import BeautifulSoup

from src.errors import FetchDataError, ParseError

logger = logging.getLogger(__name__)


def transform(data: Dict[str, Any], playlist: bool = False) -> List[Tuple[str, str]]:
    """Extract title and artists from parsed JSON data.

    :param data: string containing title and artist
    :param playlist: if True, raw data is a playlist containing several songs
    :return: title and artist
    """
    results = []
    logger.info("Getting title and artist(s) information...")
    if playlist:
        tracks = data["tracks"]["items"]
        for track in tracks:
            title = track["track"]["name"]
            artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )
            results.append((title, artists))
    else:
        artists = ", ".join([artist["name"] for artist in data["artists"]])
        title = data["name"]
        results.append((title, artists))
    return results


def extract_spotify_entity(raw_response: str) -> Optional[Dict[str, Any]]:
    """Find the Spotify.Entity in a HTML page that contains structured information
     about a Spotify song.

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


def get_song_data(url: str) -> Dict[str, Any]:
    """
    Retrieve the relevant data from the URL that displays information about a song
     on Spotify
    :param url: url to the song
    :return: title and artist
    """
    # requests error handling follows:
    # https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

    try:
        response = requests.get(url=url)
        response.raise_for_status()
        unparsed = response.text
    except requests.exceptions.HTTPError as error:
        raise FetchDataError(
            f"A HTTP error occurred while fetching song data:\n{error}"
        )
    except requests.exceptions.RequestException as error:
        raise FetchDataError(f"An error occurred while fetching song data:\n{error}")

    raw = extract_spotify_entity(unparsed)
    if not raw:
        raise ParseError("Cannot extract data: Could not find song information!")
    return raw
