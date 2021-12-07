import pathlib

import pytest
import requests

TESTDATA_ROOT = pathlib.Path("testdata")
SPOTIFY_200 = TESTDATA_ROOT / "spotify.html"
SPOTIFY_400 = TESTDATA_ROOT / "spotify_404.html"
SPOTIFY_NOENTITY = TESTDATA_ROOT / "spotify_noentity.html"


class MockResponse(requests.Response):
    def __init__(self, status_code: int = None, path: pathlib.Path = None):
        super().__init__()
        self.status_code = 200 if not status_code else status_code
        self.url = "https://spotify-testurl.com"
        self.path = path

    @property
    def text(self):
        with self.path.open(encoding="utf-8") as fi:
            text = fi.read()
            return text


@pytest.fixture
def mock_successful_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(path=SPOTIFY_200)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(status_code=400, path=SPOTIFY_400)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_noenetity_response(monkeypatch):
    # happens when response does not contain Spotify.Entity that points to song data
    def mock_get(*args, **kwargs):
        return MockResponse(status_code=200, path=SPOTIFY_NOENTITY)

    monkeypatch.setattr(requests, "get", mock_get)
