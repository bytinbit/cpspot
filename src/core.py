import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def extract(raw_response: str) -> str:
    """Extract the relevant string from a HTML page that displays information
    about a Spotify song

    :param raw_response: complete content of a html page as a string
    :return: unprocessed string that contains title and artist
    """
    tree = BeautifulSoup(raw_response, "html.parser")
    raw_string = tree.head.title.text
    logging.info(f"Found raw song title: {raw_string}")
    return raw_string


def transform(data: str) -> (str, str):
    """Parse a string that contains title and artist to a song

    :param data: string containing title and artist
    :return: title and artist
    """
    # expected format: 恭喜恭喜 - song by 姚莉, 姚敏 | Spotify
    parsed = data.replace("by", "-").replace("|", "-").split(" - ")
    return parsed[0], parsed[2]


def get_data(url: str):
    # error handling following:
    # https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
    unparsed = ""

    try:
        response = requests.get(url=url)
        response.raise_for_status()
        unparsed = response.content.decode("utf-8")
    except requests.exceptions.HTTPError as error:
        SystemExit(error)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    raw = extract(unparsed)
    return transform(raw)
