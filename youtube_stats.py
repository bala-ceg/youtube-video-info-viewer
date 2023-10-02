import streamlit as st
import re
import requests

# Set up the  Outerbase YouTube API
YOUTUBE_API_URL = 'https://arbitrary-fuchsia.cmd.outerbase.io/fetchvideoinfo'

st.title('YouTube Video Info Viewer')

# Input field for the YouTube video URL
video_url = st.text_input('Enter YouTube Video URL:')

# Function to extract video ID from URL
def get_video_id(url):
    video_id = None
    video_id_match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
    if video_id_match:
        video_id = video_id_match.group(1)
    return video_id

# Fetch and display video information
if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        params = {
            'videoid': video_id,
        }

        response = requests.get(YOUTUBE_API_URL, params=params)

        if response.status_code == 200:
            video_info = response.json()['items'][0]

            # Display video thumbnail
            st.image(video_info['snippet']['thumbnails']['medium']['url'], caption='Video Thumbnail', use_column_width=True)

            # Display video title and description
            st.header(video_info['snippet']['title'])
            st.write(video_info['snippet']['description'])

            # Display video statistics
            st.subheader('Video Statistics')
            st.write(f'Views: {video_info["statistics"]["viewCount"]}')
            st.write(f'Likes: {video_info["statistics"]["likeCount"]}')
            st.write(f'Comments: {video_info["statistics"]["commentCount"]}')
        else:
            st.warning('Failed to fetch video information. Please check the video URL and API key.')
    else:
        st.warning('Invalid YouTube video URL. Please enter a valid URL.')

