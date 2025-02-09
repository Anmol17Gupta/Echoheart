import random
from ytmusicapi import YTMusic

# Initialize YouTube Music API without authentication
ytmusic = YTMusic()  # No authentication required

# Function to fetch music recommendations
def get_youtube_music(sentiment):
    query_dict = {
        "happy": ["happy songs", "uplifting music", "feel good songs"],
        "neutral": ["lofi beats", "calm music", "chill music"],
        "sad": ["sad songs", "relaxing sad music", "comforting songs"]
    }

    search_query = random.choice(query_dict[sentiment])
    search_results = ytmusic.search(search_query, filter="songs")

    if search_results:
        song = random.choice(search_results)
        song_title = song["title"]
        artist = song["artists"][0]["name"]
        song_url = f"https://music.youtube.com/watch?v={song['videoId']}"

        return f"I recommend this song: **{song_title}** by **{artist}** 🎵\n{song_url}"
    else:
        return "I couldn't find a song right now. Try again later!"

# Function to analyze sentiment and suggest music
def recommend_music(sentiment):
    return get_youtube_music(sentiment)
