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
Parsing raw HTML...
Getting title and artist(s) information...
恭喜恭喜 - 姚莉, 姚敏
```

Extract all song data from a playlist:
```bash
cpspot "https://open.spotify.com/playlist/4VD06iQuXulKarrsIHia40?si=4ae3a105593e4919" -p
Parsing raw HTML...
Getting title and artist(s) information...
Original Bedroom Rockers - Kruder & Dorfmeister
Cowgirl - Remastered - Underworld
# -- snip --
```

## Escaping URLs in zsh
Zsh auto-escapes certain characters in the URL - a solution can be found in [[Tip] Better URL pasting in ZSH](https://forum.endeavouros.com/t/tip-better-url-pasting-in-zsh/6962).
