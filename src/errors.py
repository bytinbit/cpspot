class Error(Exception):
    """Base class for errors."""


class UsageError(Error):
    """Errors caused by the user."""


class FetchDataError(Error):
    """Errors caused while fetching data."""


class ParseError(Error):
    """Errors caused while parsing and extracting data."""
