import pathlib

import pytest
import responses

from src.core import get_song_data, transform
from src.errors import FetchDataError, ParseError
from testdata.raw_data import RAW_DATA, RAW_PLAYLIST, EXPECTED_PLAYLIST


TEST_URL = (
    "https://open.spotify.com/track/5lQdYxYl9okxBXtnSN8iJI?si=0e7aa3db079c42c5&nd=1"
)

TESTDATA_ROOT = pathlib.Path(__file__).parent / "testdata"
SPOTIFY_200 = TESTDATA_ROOT / "spotify.html"
SPOTIFY_PLAYLIST = TESTDATA_ROOT / "spotify_playlist.html"
SPOTIFY_404 = TESTDATA_ROOT / "spotify_404.html"
SPOTIFY_NOENTITY = TESTDATA_ROOT / "spotify_noentity.html"


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize(
    "url,path,status,expected",
    [
        ("http://spotify.com/mysong", SPOTIFY_200, 200, RAW_DATA),
        ("http://spotify.com/playlist", SPOTIFY_PLAYLIST, 200, RAW_PLAYLIST),
    ],
)
def test_get_song_data(mocked_responses, url, path, status, expected):
    mocked_responses.add(
        responses.GET, url, body=path.read_text(encoding="utf-8"), status=status
    )
    result = get_song_data(url=url)
    assert result == expected


@pytest.mark.parametrize(
    "url,path,status,expected_exception",
    [
        ("http://spotify.com/404", SPOTIFY_404, 404, FetchDataError),
        ("http://spotify.com/nospotifyentity", SPOTIFY_NOENTITY, 200, ParseError),
    ],
)
def test_get_song_data_fails(mocked_responses, url, path, status, expected_exception):
    mocked_responses.add(
        responses.GET, url, body=path.read_text(encoding="utf-8"), status=status
    )
    with pytest.raises(expected_exception):

        _ = get_song_data(url=url)


def test_transform_single_song():
    result = transform(RAW_DATA)
    assert [("恭喜恭喜", "姚莉, 姚敏")] == result


def test_transform_playlist():
    result = transform(RAW_PLAYLIST, playlist=True)
    assert EXPECTED_PLAYLIST == result


def test_integration_real_url():
    raw = get_song_data(TEST_URL)
    assert [("恭喜恭喜", "姚莉, 姚敏")] == transform(raw)
