import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = str(os.environ['MYSPOTIFYLIKEDSONGS_CLIENT_ID'])
client_secret = str(os.environ['MYSPOTIFYLIKEDSONGS_CLIENT_SECRET'])
redirect_uri = str(os.environ['MYSPOTIFYLIKEDSONGS_URL'])

def saveListToJson(tracks, path):
    f = open(path,"w+")
    f.write(json.dumps(tracks, indent=4))
    f.close() 

def saveListToFile(tracks, path):
    f = open(path,"w+")
    header = "name\tartists\talbum\tcover\thref\tadded_at\n"
    f.write(header)
    for track in tracks:
        text = track['name'] + "\t" + track['artists'] + "\t" + track['album'] + "\t" + track['cover'] + "\t" + track['href'] + "\t" + track['added_at'] + "\n"
        f.write(text)
    f.close() 

def main():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-read"
        )
    )

    total_results = sp.current_user_saved_tracks()
    print("Total tracks: " + str(total_results['total']))

    pages = round(total_results['total']/50)
    tracks = []
    for i in range(pages):
        offset=50*i
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        for item in results['items']:
            added_at = item['added_at']
            track = item['track']
            tracks.append({
                'name': track['name'], 
                'artists': track['artists'][0]['name'], 
                'album': track['album']['name'], 
                'cover': track['album']['images'][0]['url'], 
                'href': track['href'], 
                'added_at': added_at
            })

    saveListToJson(tracks, './LikedSongs/LikedSongs.json')
    saveListToFile(tracks, './LikedSongs/LikedSongs.tsv')

if __name__ == '__main__':
    main()