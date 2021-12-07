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
@click.option("-p", "--playlist", is_flag=True)
@click.argument("url", metavar="URL")
def main(url, playlist):
    try:
        raw = get_song_data(url)
    except Error as e:
        print(e)
        sys.exit(1)

    results = transform(raw, playlist)
    for song in results:
        print(f"{song[0]} - {song[1]}")
