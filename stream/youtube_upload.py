import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
#from moviepy import VideoFileClip, AudioFileClip, ImageClip, clips_array
from googleapiclient.http import MediaFileUpload
from googletrans import Translator
#from datetime import datetime, timedelta
#from yt_dlp import YoutubeDL  # YouTubeDL module
import random
import re  # For extracting hashtags
#from pathlib import Path
import var

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Google API credentials and YouTube Data API service configuration
scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]

# Random title and description generator
adjectives = ["Hilarious", "Epic", "Crazy", "Amazing", "Funny", "Incredible"]
verbs = ["Moments", "Challenges", "Pranks", "Skits", "Reactions", "Fails"]
topics = ["Friends", "Daily Life", "Adventures", "Comedy Show", "Vlogs", "Entertainment"]

def generate_title():
    adj = random.choice(adjectives)
    verb = random.choice(verbs)
    topic = random.choice(topics)
    return f"{adj} {verb} with {topic} - Must Watch!"

def generate_description():
    return f"Enjoy these {random.choice(adjectives)} {random.choice(verbs)} from {random.choice(topics)}! Don't forget to like and subscribe for more."

def get_authenticated_service():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "youtube_client_secret.json", scopes)
            credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, video_file, title, description, tags, category_id, privacy_status, publish_at=None, video_language="ru"):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags + ["#shorts"],  # Adding Shorts tag
            "categoryId": category_id,
            "defaultLanguage": "ru",  # Video title and description language
            "defaultAudioLanguage": video_language  # Spoken language of the video
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False  # Not marked for kids
        }
    }

    if publish_at:
        body["status"]["publishAt"] = publish_at

    media_file = MediaFileUpload(video_file, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media_file
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Upload Status: {int(status.progress() * 100)}% completed.")
        except googleapiclient.errors.HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                print("Server error, retrying...")
            elif e.resp.status == 403:
                print("Quota limit exceeded. Please increase your quota or try again later.")
                break
            else:
                raise

    if response:
        print("Video uploaded successfully!")
        print(f"https://www.youtube.com/watch?v={response['id']}")
        return response['id']
    return None

def translate_text(text, dest_lang='tr'):
    """Translates the given text to the specified language (default: Turkish)"""
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest_lang)
        if translated.text:
            return translated.text
        else:
            print(f"Translation returned empty: {text} -> {dest_lang}")
            return text  # Return original text if translation is empty
    except Exception as e:
        print(f"An error occurred: {e}")
        return text  # Return original text if there's an error

def add_multiple_languages_to_video(youtube, video_id, translations):
    """Adds multiple languages to a YouTube video"""
    body = {
        "id": video_id,
        "localizations": translations
    }

    request = youtube.videos().update(
        part="localizations",
        body=body
    )

    response = request.execute()
    print("All languages added successfully!")
    return response

def get_top_30_languages_translations(title, description):
    """Translates the title and description into the top 30 most spoken languages"""
    languages = ['tr', 'fr', 'it', 'es', 'de', 'zh-cn', 'hi', 'ar', 'ru', 'pt', 
                 'ja', 'ko', 'bn', 'vi', 'ur', 'pa', 'fa', 'id', 'th', 'ms', 
                 'pl', 'ro', 'uk', 'nl', 'el', 'sv', 'hu', 'cs', 'da', 'fi']
    
    translations = {}
    for lang in languages:
        translated_title = translate_text(title, dest_lang=lang)
        translated_description = translate_text(description, dest_lang=lang)
        translations[lang] = {
            "title": translated_title,
            "description": translated_description
        }
    return translations

def get_video_hashtags(description):
    # Using a simple regex to identify hashtags
    hashtags = re.findall(r"#\w+", description)
    return hashtags

def get_video_details(youtube, video_id):
    # Get video details including description
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    return response['items']

if __name__ == "__main__":
    youtube = get_authenticated_service()

    # Get hashtags from a popular video using its video_id
    popular_video_id = "TTMZpCcuaZ8"  # Enter the ID of a popular video here
    popular_video_details = get_video_details(youtube, popular_video_id)
    
    # Extract hashtags from the description of the popular video
    popular_video_description = popular_video_details[0]['snippet']['description']
    popular_hashtags = get_video_hashtags(popular_video_description)
    
    # Generate random title and description
    title = generate_title()
    description = generate_description()
    
    # Fixed tags
    manual_tags =   ['stream', 'twitch', 's1rmtrpr', "fyp", "shorts", "viral", "gaming", "Comedy", "Humor", "DailyLife", "Vlog", 
                    "Sketch", "Trending", "FunnyMoments", "FunVideos", "Challenge", "Parody", "Prank", "Viral", "FunnyVideos", "Laugh"]
    
    # Combine manual hashtags with those from the popular video
    combined_tags = manual_tags + popular_hashtags
    
    category_id = "20"  # YouTube category, 20 = Gaming https://gist.github.com/dgp/1b24bf2961521bd75d6c
    privacy_status = "public"  # Privacy status of the video: "public", "private", or "unlisted"

    # Upload the video to YouTube and get the video ID
    video_id = upload_video(youtube, var.uploadfilename, title, description, combined_tags, category_id, privacy_status)
    
    if video_id:
        # Get translations for the top 30 spoken languages
        translations = get_top_30_languages_translations(title, description)
        
        # Add multiple languages to the video
        add_multiple_languages_to_video(youtube, video_id, translations)
