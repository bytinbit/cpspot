import pathlib

import pytest
import responses

from src.core import get_song_data, transform
from src.errors import FetchDataError, ParseError


RAW_DATA = {
    "album": {
        "album_type": "album",
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/3agVasaCG20vNRxAE8niec"
                },
                "href": "https://api.spotify.com/v1/artists/3agVasaCG20vNRxAE8niec",
                "id": "3agVasaCG20vNRxAE8niec",
                "name": "姚莉",
                "type": "artist",
                "uri": "spotify:artist:3agVasaCG20vNRxAE8niec",
            }
        ],
        "external_urls": {
            "spotify": "https://open.spotify.com/album/640Lj4MlHRY7ZezEsrND2H"
        },
        "href": "https://api.spotify.com/v1/albums/640Lj4MlHRY7ZezEsrND2H",
        "id": "640Lj4MlHRY7ZezEsrND2H",
        "images": [
            {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b273a174ee78ebf4fcdad5b64444",
                "width": 640,
            },
            {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e02a174ee78ebf4fcdad5b64444",
                "width": 300,
            },
            {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d00004851a174ee78ebf4fcdad5b64444",
                "width": 64,
            },
        ],
        "name": "秋的懷念-上海時期歌曲Vol.25/26",
        "release_date": "1992-01-01",
        "release_date_precision": "day",
        "total_tracks": 32,
        "type": "album",
        "uri": "spotify:album:640Lj4MlHRY7ZezEsrND2H",
    },
    "artists": [
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/3agVasaCG20vNRxAE8niec"
            },
            "href": "https://api.spotify.com/v1/artists/3agVasaCG20vNRxAE8niec",
            "id": "3agVasaCG20vNRxAE8niec",
            "name": "姚莉",
            "type": "artist",
            "uri": "spotify:artist:3agVasaCG20vNRxAE8niec",
        },
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/6i1lJfQydjGpVPtKs8snBC"
            },
            "href": "https://api.spotify.com/v1/artists/6i1lJfQydjGpVPtKs8snBC",
            "id": "6i1lJfQydjGpVPtKs8snBC",
            "name": "姚敏",
            "type": "artist",
            "uri": "spotify:artist:6i1lJfQydjGpVPtKs8snBC",
        },
    ],
    "disc_number": 1,
    "duration_ms": 170160,
    "explicit": False,
    "external_ids": {"isrc": "HKB129200015"},
    "external_urls": {
        "spotify": "https://open.spotify.com/track/5lQdYxYl9okxBXtnSN8iJI"
    },
    "href": "https://api.spotify.com/v1/tracks/5lQdYxYl9okxBXtnSN8iJI",
    "id": "5lQdYxYl9okxBXtnSN8iJI",
    "is_local": False,
    "is_playable": True,
    "name": "恭喜恭喜",
    "popularity": 19,
    "preview_url": "https://p.scdn.co/mp3-preview/9c5064dcf97c902db616cef3365b0d76eaa39de7?cid=162b7dc01f3a4a2ca32ed3cec83d1e02",
    "track_number": 12,
    "type": "track",
    "uri": "spotify:track:5lQdYxYl9okxBXtnSN8iJI",
}

TEST_URL = "https://open.spotify.com/track/5lQdYxYl9okxBXtnSN8iJI?si=0e7aa3db079c42c5&nd=1"

TESTDATA_ROOT = pathlib.Path("testdata")
SPOTIFY_200 = TESTDATA_ROOT / "spotify.html"
SPOTIFY_404 = TESTDATA_ROOT / "spotify_404.html"
SPOTIFY_NOENTITY = TESTDATA_ROOT / "spotify_noentity.html"


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize(
    "url,path,status", [("http://spotify.com/mysong", SPOTIFY_200, 200)]
)
def test_get_song_data(mocked_responses, url, path, status):
    mocked_responses.add(
        responses.GET, url, body=path.read_text(encoding="utf-8"), status=status
    )
    result = get_song_data(url=url)
    assert result == RAW_DATA


@pytest.mark.parametrize(
    "url,path,status,expected_exception",
    [
        ("http://spotify.com/404", SPOTIFY_404, 404, FetchDataError),
        ("http://spotify.com/nospotifyentity", SPOTIFY_NOENTITY, 200, ParseError),
    ],
)
def test_get_song_data_fails(
    mocked_responses, url, path, status, expected_exception
):
    mocked_responses.add(
        responses.GET, url, body=path.read_text(encoding="utf-8"), status=status
    )
    with pytest.raises(expected_exception):

        _ = get_song_data(url=url)


def test_transform():
    title, artist = transform(RAW_DATA)
    assert ("恭喜恭喜", "姚莉, 姚敏") == (title, artist)


def test_integration_real_url():
    raw = get_song_data(TEST_URL)
    assert ("恭喜恭喜", "姚莉, 姚敏") == transform(raw)