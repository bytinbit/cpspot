import logging
import sys

import click

from src.core import get_data, transform
from src.errors import FetchDataError, ParseError

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


@click.command()
@click.argument("url", metavar="URL")
def main(url):
    try:
        raw = get_data(url)
        if not raw:
            raise ParseError(
                "Cannot extract data: Could not find relevant information!"
            )
    except FetchDataError as e:
        print(e)
        sys.exit(1)
    except ParseError as e:
        print(e)
        sys.exit(1)

    title, artist = transform(raw)
    print("Here's your title and artist:")
    print(f"{title}")
    print(f"{artist}")
