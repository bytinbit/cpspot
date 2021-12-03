import logging

import click

from src.core import get_data

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

@click.command()
@click.argument("url", metavar="URL")
def main(url):
    title, artist = get_data(url)
    print(f"Title:\n{title}")
    print(f"Artist:\n{artist}")
