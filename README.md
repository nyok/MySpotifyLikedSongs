# Getting a List of Liked Songs in Spotify Using the API

## Environment variables in a file .env
```
MYSPOTIFYLIKEDSONGS_CLIENT_ID='CLIENT_ID'
MYSPOTIFYLIKEDSONGS_CLIENT_SECRET='CLIENT_SECRET'
MYSPOTIFYLIKEDSONGS_URL='URL'
```

### Launch:
* Set environment variables from .env file
`export $(xargs < .env)`
* Launch script `python3 main.py`
