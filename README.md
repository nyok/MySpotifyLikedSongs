# Getting a List of Liked Songs in Spotify Using the API

**Environment variables in a file .env**
```
MYSPOTIFYLIKEDSONGS_CLIENT_ID='CLIENT_ID'
MYSPOTIFYLIKEDSONGS_CLIENT_SECRET='CLIENT_SECRET'
MYSPOTIFYLIKEDSONGS_URL='URL'
```

**Launch**:
`python3 main.py`


# Make auto commit & push to GitHub (if there are new liked songs)

**Environment variables in a file .env**
```
GITHUB_USERNAME='USERNAME'
GITHUB_REPO='REPONAME'
GITHUB_TOKEN='CLIENT_TOKEN'
```
**Launch**:
`python3 autocommit.py`


Previously it was necessary to load the variable manually `export $(xargs < .env)`
now this is done automatically using the "dotenv" library
