import os
import os.path as op
import requests
from datetime import datetime
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip, TextClip, concatenate_videoclips
from gtts import gTTS
from moviepy.config import change_settings
import json
from news_api import get_technology_news

change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# Load the JSON file
with open('docker.json', 'r') as file:
    data = json.load(file)
    
# Load the JSON file
with open('docker-subtitles.json', 'r', encoding='utf-8') as file:
    subtitles = json.load(file)

# Access the title and content
title = data['title']
content = data['content']

# News API
# news_data = get_technology_news()

def download_video(video_url, download_path, filename):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    response = requests.get(video_url)
    if response.status_code == 200:
        filepath = os.path.join(download_path, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Video downloaded successfully as {filename}")
        return filepath
    else:
        print("Failed to download video")
        return None

def get_stock_video(query='drone', download_path='api_data'):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{query}_{timestamp}.mp4"

    url = 'https://api.pexels.com/videos/search'
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': query, 'per_page': 1}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching video: {response.status_code}")
        print(response.text)
        return None

    data = response.json()
    if data['videos']:
        video_url = data['videos'][0]['video_files'][0]['link']
        print(f"Video URL: {video_url}")
        return download_video(video_url, download_path, filename)
    else:
        print("No videos found.")
        return None

def text_to_speech(text, output_path='tts_audio'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio_filename = f"{timestamp}.mp3"
    tts = gTTS(text=text, lang='en-uk', slow=False)
    tts.save(os.path.join(output_path, audio_filename))
    print(f"Speech saved to {audio_filename}")
    return os.path.join(output_path, audio_filename)

def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    """ Writes a text at the bottom of the clip. """
    txtclip = TextClip(txt, fontsize=fontsize, font=font, color=txt_color)
    cvc = CompositeVideoClip([clip, txtclip.set_position(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

def create_movie_with_audio_and_subtitles(video_filename, audio_filename, text, subtitles, output_path='final_videos'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    final_video_name = f"{timestamp}.mp4"

    video_clip = VideoFileClip(video_filename)
    video_clip = concatenate_videoclips([video_clip, video_clip, video_clip, video_clip, video_clip])
    audio_clip = AudioFileClip(audio_filename)
    
    # Calculate text duration based on text length
    text_duration = len(text.split()) * 0.1  # Adjust the multiplier as needed
    
    # Create a list to store subtitle clips
    subtitle_clips = []
    
    # Generate text clips for subtitles
    for subtitle_data in subtitles:
        subtitle_text = subtitle_data['text']
        start_time = subtitle_data['start']
        end_time = subtitle_data['end']
        
        # Calculate duration for each subtitle
        subtitle_duration = end_time - start_time
        
        # Generate text clip for the subtitle
        txt_clip = TextClip(subtitle_text, fontsize=120, color='white', align='center', font='Arial-Bold', size=video_clip.size, stroke_color='black', stroke_width=3)
        txt_clip = txt_clip.set_pos('center').set_duration(subtitle_duration).fadein(0.5).fadeout(0.5).set_start(start_time)
        
        # Add the subtitle clip to the list
        subtitle_clips.append(txt_clip)
    
    # Combine all subtitle clips into a single CompositeVideoClip
    subtitles_clip = CompositeVideoClip(subtitle_clips)
    
    # Composite the video with audio and subtitles
    final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip), subtitles_clip])
    
    # Write the final video file
    final_clip.write_videofile(os.path.join(output_path, final_video_name))

def main():
    print("Fetching stock video...")
    video_filename = get_stock_video(query='night moon stars')
    if video_filename:
        # Load content from docker.json
        with open('docker.json', 'r') as file:
            docker_data = json.load(file)
        docker_content = docker_data['content']
        
        # Load subtitles from docker-subtitles.json
        with open('docker-subtitles.json', 'r') as file:
            subtitles_data = json.load(file)
        subtitles = subtitles_data['subtitles']
        
        # Convert docker content to speech
        audio_filename = text_to_speech(docker_content)
        
        # Create final video with audio and subtitles
        print(f"Creating final video with Docker content audio and subtitles")
        create_movie_with_audio_and_subtitles(video_filename, audio_filename, docker_content, subtitles)

if __name__ == '__main__':
    main()