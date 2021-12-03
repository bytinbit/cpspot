# cpspot

Spotify makes it impossible to simply copy-paste the title and author of a song, 
neither from the desktop nor the browser version. Various related questions on 
Spotify's community forums confirm this (such as [this](https://community.spotify.com/t5/Desktop-Windows/How-do-I-copy-song-names-when-using-the-desktop-or-web-app/td-p/4715780))
with no useful tips.

Enter cpspot:
```bash
# clone repository
$ cd cpspot
# create, activate venv
$ pip install .
# Copy song url from a song's share button
cpspot "https://open.spotify.com/track/5lQdYxYl9okxBXtnSN8iJI?si=0e7aa3db079c42c5&nd=1"    
Received raw song title: 恭喜恭喜 - song by 姚莉, 姚敏 | Spotify
Title:
恭喜恭喜
Artist:
姚莉, 姚敏
```