import os
import sys

import pandas as pd
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-modify-private'))
df = pd.read_csv('tracks.csv.example', sep=';', encoding='utf-16-le')
df = df.sample(frac=1)
acrostic_list = []

if len(sys.argv) <= 1:
    print("Please enter a phrase")
    sys.exit(1)

phrase = sys.argv[1]

for letter in phrase:
    tracks = df.loc[df['track_name'].str.startswith(letter), 'track_id'].tolist()
    track_name = random.choice(tracks)
    df = df[df['track_name'] != track_name]
    tracks.remove(track_name)
    acrostic_list.append(track_name)

sp.playlist_add_items(
    "spotify:playlist:2E0mg7pku7fogLbEo8tuCJ",
    acrostic_list
)
