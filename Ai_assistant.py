import datetime
import pyttsx3
import webbrowser
import os
import sys
import random
import requests
from typing import Dict
from urllib.parse import urlparse, parse_qs, urlencode

# Initialize text-to-speech
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice (adjust if needed)
    engine.setProperty('rate', 180)  # Clear speech rate
except Exception as e:
    print(f"Error initializing text-to-speech: {e}")
    sys.exit(1)

# Google Gemini API setup
GEMINI_API_KEY = "REPLACE_YOUR_API_KEY_HERE"  #replace your Api Key (ensure it's valid)
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Fallback knowledge base
FALLBACK_KNOWLEDGE: Dict[str, str] = {
    "python": "Python is a high-level, interpreted programming language known for its readability and versatility. It was created by Guido van Rossum and first released in 1991.",
    "albert einstein": "Albert Einstein was a German-born physicist who developed the theory of relativity. He's famous for the equation E equals M C squared and won the Nobel Prize in Physics in 1921.",
    "sun": "The Sun is a star at the center of our solar system. It's a nearly perfect sphere of hot plasma, primarily made of hydrogen and helium, and provides Earth with light and heat.",
    "ai": "Artificial Intelligence, or AI, is the simulation of human intelligence in machines. It includes tasks like learning, problem-solving, and decision-making.",
    "gravity": "Gravity is a fundamental force that attracts objects toward each other. It keeps planets in orbit around the Sun and is described by Newton's law of universal gravitation.",
    "elon musk": "Elon Musk is a billionaire entrepreneur and inventor, known for founding Tesla, SpaceX, and Neuralink. He's a key figure in technology and space exploration.",
}

def speak(text: str):
    """Speak the given text."""
    try:
        clean_text = text.replace('*', '')  # Remove asterisks
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")

def get_user_input() -> str:
    """Get text input from the user, preserving case for URLs."""
    try:
        query = input("Enter your command or question: ").strip()
        print(f"You entered: {query}")
        return query
    except KeyboardInterrupt:
        speak("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error reading input: {e}")
        return ""

def get_gemini_response(query: str) -> str:
    """Fetch response from Google Gemini API."""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": query.lower()}]}],
            "generationConfig": {
                "maxOutputTokens": 150,
                "temperature": 0.7,
            }
        }
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Gemini API error: {e}")
        for key, value in FALLBACK_KNOWLEDGE.items():
            if key.lower() in query.lower():
                return value
        return f"Sorry, I couldn't fetch information about {query} right now. Try something else!"

def is_valid_url(url: str) -> bool:
    """Check if the input is a valid URL, preserving case."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def normalize_youtube_url(url: str) -> str:
    """Normalize YouTube URLs (e.g., youtu.be to youtube.com/watch), preserving case where possible."""
    if not url:
        return url
    
    # Check if it's a youtu.be short link (case-insensitive domain)
    if 'youtu.be' in url.lower():
        video_id = url.split('/')[-1].split('?')[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    
    # Handle youtube.com links with or without parameters (preserve case where possible)
    if 'youtube.com' in url.lower():
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if 'v' in query:
            video_id = query['v'][0]
            base_url = f"https://www.youtube.com/watch?v={video_id}"
            # Preserve other query parameters like timestamps (case-sensitive)
            query_params = {k: v for k, v in query.items() if k != 'v'}
            if query_params:
                base_url += f"?{urlencode(query_params, quote_via=urlencode)}"
            return base_url
    return url

def check_youtube_availability(url: str) -> bool:
    """Check if a YouTube video is available and accessible, preserving case."""
    try:
        normalized_url = normalize_youtube_url(url)
        import yt_dlp
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(normalized_url, download=False)
            return info.get('id') is not None
    except Exception as e:
        print(f"Error checking YouTube availability: {e}")
        return False

def open_link(url: str):
    """Open a URL in the default web browser, with special handling for YouTube, preserving case."""
    try:
        if not is_valid_url(url):
            speak("Invalid URL. Please provide a valid link.")
            return

        normalized_url = normalize_youtube_url(url)
        if 'youtube.com' in normalized_url.lower() or 'youtu.be' in normalized_url.lower():
            if check_youtube_availability(normalized_url):
                webbrowser.open(normalized_url)
                speak(f"Opening {normalized_url} in your browser.")
            else:
                speak("The YouTube video is not available or restricted. Please check the link.")
        else:
            webbrowser.open(normalized_url)
            speak(f"Opening {normalized_url} in your browser.")
    except Exception as e:
        print(f"Error opening URL: {e}")
        speak("There was an error opening the link. Please try again.")

def download_youtube_video(youtube_url: str, output_path: str = "downloads"):
    """Download a YouTube video to the specified path using yt-dlp, preserving case, with robust error handling."""
    try:
        if not is_valid_url(youtube_url):
            speak("Invalid YouTube URL. Please provide a valid link.")
            return

        normalized_url = normalize_youtube_url(youtube_url)
        if not check_youtube_availability(normalized_url):
            speak("The YouTube video is not available, restricted, or private. Please check the link.")
            return

        # Ensure output directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        import yt_dlp
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(normalized_url, download=True)
            speak(f"Downloaded {info['title']} to the {output_path} folder.")
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error with yt-dlp: {e}")
        if "403" in str(e) or "Forbidden" in str(e):
            speak("YouTube blocked the download due to restrictions or anti-scraping measures. Try logging into YouTube in your browser or using a different link.")
        elif "private" in str(e).lower() or "age-restricted" in str(e).lower():
            speak("This YouTube video is private or age-restricted and cannot be downloaded. Please ensure it's public or use a different link.")
        else:
            speak("There was an error downloading the video. It might be due to network issues or an invalid link. Please try again.")
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        speak("There was an error downloading the video. It might be due to restrictions, network issues, or an invalid link. Please try again.")

def process_command(query: str):
    """Process the user's command or question, preserving case for URLs."""
    if not query:
        speak("Please enter a command or question.")
        return

    # Commands (case-insensitive for keywords, but preserve URLs)
    query_lower = query.lower()
    if "hello" in query_lower or "hi" in query_lower:
        speak("Hello! I'm your assistant. How can I help you?")
    elif "how are you" in query_lower:
        speak("I'm doing great, thanks! How can I assist you today?")
    elif "what can you do" in query_lower:
        speak("I can answer questions, tell the time, open websites, play music, download YouTube videos, and more. Ask me anything!")

    elif "time" in query_lower:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "date" in query_lower or "today" in query_lower:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")

    elif "open website" in query_lower or "open" in query_lower:
        # Extract URL, preserving original case
        url_start = query.find("http")
        url = query[url_start:] if url_start != -1 else query.replace("open website", "").replace("open", "").strip()
        if url:
            open_link(url)
        else:
            speak("Please specify a URL to open, e.g., 'open https://www.YouTube.com'.")

    elif "play music" in query_lower:
        music_dir = "C:/Users/PK/Music"  # Replace with your music directory
        if os.path.exists(music_dir):
            songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                speak(f"Playing {song} from your music directory.")
            else:
                speak("No music files found in the directory.")
        else:
            speak("Music directory not found. Please configure the correct path.")

    elif "calculate" in query_lower or "math" in query_lower:
        try:
            expression = query.replace("calculate", "").replace("math", "").strip()
            result = eval(expression)
            speak(f"The result of {expression} is {result}.")
        except Exception:
            speak("Sorry, I couldn't perform that calculation. Try '2 plus 3'.")

    elif "download" in query_lower:
        # Extract YouTube URL, preserving original case
        url_start = query.find("http")
        youtube_url = query[url_start:] if url_start != -1 else query.replace("download", "").strip()
        if youtube_url:
            download_youtube_video(youtube_url, output_path="downloads")
        else:
            speak("Please specify a YouTube URL to download, e.g., 'download https://www.YouTube.com/watch?v=VIDEO_ID'.")

    elif "exit" in query_lower or "quit" in query_lower or "goodbye" in query_lower:
        speak("Goodbye! Thanks for using me.")
        sys.exit(0)

    else:
        response = get_gemini_response(query)  # Keep query lowercase for Gemini
        speak(response)

def main():
    speak("Greetings! I'm your AI assistant, Ask me anything!") 
    print("Type your command or question below (e.g., 'time', 'Python', 'play music', 'open https://www.YouTube.com', 'download https://www.YouTube.com/watch?v=VIDEO_ID', 'exit')")
    while True:
        user_query = get_user_input()
        process_command(user_query)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("An error occurred. Shutting down.")
        sys.exit(1)
