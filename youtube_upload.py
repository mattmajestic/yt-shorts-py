import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Authenticate using OAuth 2.0 credentials
credentials = Credentials.from_authorized_user_file('credentials.json', scopes=['https://www.googleapis.com/auth/youtube.upload'])
youtube = build('youtube', 'v3', credentials=credentials)

# Define video metadata
request_body = {
    'snippet': {
        'title': 'Docker with Python & AI',
        'description': 'This video was completely automated with AI using Python to inform those about Docker',
        'tags': ['tag1', 'tag2', 'tag3'],
        'categoryId': '22'  # Category ID for Tech, you can find other category IDs in the YouTube API documentation.
    },
    'status': {
        'privacyStatus': 'public'  # Set to 'private' if you want the video to be private
    }
}

# Specify the video file to upload
media = MediaFileUpload('final_videos/video.mp4')

# Upload the video
upload_response = youtube.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=media
).execute()

print('Video uploaded successfully!')
