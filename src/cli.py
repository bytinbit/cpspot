import logging
import sys

import click

from src.core import get_song_data, transform
from src.errors import Error

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


@click.command()
@click.argument("url", metavar="URL")
def main(url):
    try:
        raw = get_song_data(url)
    except Error as e:
        print(e)
        sys.exit(1)

    title, artist = transform(raw)
    print("Here's your title and artist:")
    print(f"{title}")
    print(f"{artist}")
