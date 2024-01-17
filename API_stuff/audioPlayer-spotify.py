#Python project that is meant to be speaking to the API to play music from certain URLs.

import requests
import json
import pyglet

# Your Spotify API credentials
client_id = ""
client_secret = ""

# Get an access token
auth_url = f"https://accounts.spotify.com/api/token"
auth_response = requests.post(auth_url, {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
})

access_token = auth_response.json()["access_token"]

# Spotify Web API endpoint for searching for tracks
search_url = "https://api.spotify.com/v1/search?q={query}&type=track"

# Get the user's search query
query = input("Enter a song title: ")

# Search for tracks matching the user's query
response = requests.get(search_url.format(query=query)).json()

# Check if the response contains any tracks
if 'tracks' in response and response['tracks']['items']:
    # Get the first track from the search results
    track = response['tracks']['items'][0]

    # Get the preview URL for the track
    preview_url = track['preview_url']

    # Download the audio file to a local file
    response = requests.get(preview_url)
    with open("preview.mp3", "wb") as f:
        f.write(response.content)

    # Load the audio file using pyglet
    audio = pyglet.media.load("preview.mp3")
    player = pyglet.media.Player()
    player.queue(audio)
    player.play()

    # Wait for the audio to finish
    pyglet.app.run()
else:
    # No tracks found, print an error message
    print("No tracks found for the query:", query)
