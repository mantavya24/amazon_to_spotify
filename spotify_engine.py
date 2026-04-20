import os
import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from thefuzz import fuzz

# Load credentials from .env
load_dotenv()

# Setup Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="playlist-modify-public"
    ),
    requests_timeout=20,
    retries=5,
    status_retries=5,
    backoff_factor=0.5
)

def create_spotify_playlist(name, tracks):
    user_id = sp.current_user()['id']
    print(f"Authenticated as: {sp.current_user()['display_name']}")
    
    # 1. Create the new playlist
    playlist = sp.user_playlist_create(user_id, name, public=True)
    playlist_id = playlist['id']
    
    track_uris = []
    
    # 2. Search for each track from our JSON
    for track in tracks:
        query = f"{track['title']} {track['artist']}"
        results = sp.search(q=query, limit=5, type='track')
        
        found = False
        for item in results['tracks']['items']:
            # Use Fuzzy Matching to ensure it's actually the right song
            # (Matches title similarity > 80%)
            ratio = fuzz.partial_ratio(track['title'].lower(), item['name'].lower())
            
            if ratio > 80:
                track_uris.append(item['uri'])
                print(f"🔗 Linked: {track['title']} -> {item['name']} ({ratio}%)")
                found = True
                break
        
        if not found:
            print(f"❌ Could not find: {track['title']} by {track['artist']}")
            
        time.sleep(0.3)  # Small delay to prevent API timeout bursts

    # 3. Add tracks in batches (Spotify limit is 100 per call)
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        print(f"\n🎉 Done! Added {len(track_uris)} songs to '{name}' on Spotify.")

if __name__ == "__main__":
    with open("amazon_tracks.json", "r") as f:
        data = json.load(f)
    
    if isinstance(data, list) and len(data) > 0 and 'playlist_name' in data[0]:
        # New format: list of playlists
        print(f"Found {len(data)} distinct playlists in amazon_tracks.json. Creating them...")
        for idx, playlist in enumerate(data):
            name = playlist.get('playlist_name', f"Amazon Playlist {idx+1}")
            tracks = playlist.get('tracks', [])
            print(f"\n--- Importing Playlist: {name} ---")
            create_spotify_playlist(name, tracks)
    else:
        # Legacy format: flat list of tracks
        playlist_name = input("Enter the name for your new Spotify playlist: ")
        create_spotify_playlist(playlist_name, data)