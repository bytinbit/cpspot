import pathlib

import pytest

from src.core import retrieve_song_data, transform
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


def test_get_data(mock_successful_response):
    result = retrieve_song_data(url="spotify.html")
    assert result == RAW_DATA


def test_get_data_notfound(mock_404_response):
    with pytest.raises(FetchDataError):
        _ = retrieve_song_data(url="spotify_404.html")


def test_get_data_noentity(mock_noenetity_response):
    with pytest.raises(ParseError):
        _ = retrieve_song_data(url="spotify_noentity.html")


def test_transform():
    title, artist = transform(RAW_DATA)
    assert ("恭喜恭喜", "姚莉, 姚敏") == (title, artist)
