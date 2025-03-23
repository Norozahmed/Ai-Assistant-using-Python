# AI Assistant

This is a simple AI assistant built with Python that can answer questions, tell the time, open websites, play music, and download YouTube videos. It uses the Google Gemini API for question answering and `yt-dlp` for YouTube downloads.

## Features

*   **Text-to-Speech:** Uses `pyttsx3` to speak responses.
*   **Google Gemini API Integration:** Leverages the Gemini API for answering user queries.
*   **Fallback Knowledge Base:** Includes a local knowledge base for common questions.
*   **Web Browser Integration:** Can open websites in the default web browser using `webbrowser`.
*   **Music Playback:** Plays music files from a specified directory.
*   **YouTube Download:** Downloads YouTube videos using `yt-dlp`.
*   **URL Handling:** Normalizes and validates URLs, especially for YouTube.
*   **Error Handling:** Implements robust error handling for various operations.

## Requirements

*   Python 3.6 or higher
*   `pyttsx3`
*   `webbrowser`
*   `os`
*   `sys`
*   `random`
*   `requests`
*   `yt-dlp`
*   Google Gemini API key

You can install the required packages using pip:


## Setup

1.  **Install Dependencies:**

    ```
    pip install pyttsx3 requests yt-dlp
    ```
2.  **Get a Google Gemini API Key:**

    *   Sign up for the Google Gemini API and obtain an API key.
    *   Replace `"YOUR-API-KEY"` in the script with your actual API key.

    ```
    GEMINI_API_KEY = "YOUR-API-KEY"  # Your key (ensure it's valid)
    ```

    **Important:** For security, it's recommended to use environment variables instead of hardcoding the API key in the script.

    ```
    import os
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
    ```

    Set the environment variable:

    ```
    export GEMINI_API_KEY="your_actual_api_key"
    ```
3.  **Configure Music Directory (Optional):**

    *   Modify the `music_dir` variable in the `process_command` function to point to your music directory.

    ```
    music_dir = "C:/Users/PK/Music"  # Replace with your music directory
    ```

## Usage

1.  **Run the script:**

    ```
    python Ai_assistent.py
    ```
2.  **Interact with the assistant:**

    *   Type your command or question and press Enter.
    *   Examples:
        *   `time`
        *   `What is Python?`
        *   `Open https://www.YouTube.com`
        *   `Play music`
        *   `Download https://www.YouTube.com/watch?v=VIDEO_ID`
        *   `Exit`

## Code Overview

### Initialization

*   Initializes the text-to-speech engine with a female voice and a clear speech rate.
*   Sets up the Google Gemini API URL and includes a fallback knowledge base for quick answers.

### Functions

*   `speak(text: str)`: Speaks the given text using the `pyttsx3` engine.
*   `get_user_input() -> str`: Gets text input from the user.
*   `get_gemini_response(query: str) -> str`: Fetches a response from the Google Gemini API or uses the fallback knowledge base if the API fails.
*   `is_valid_url(url: str) -> bool`: Checks if the input is a valid URL.
*   `normalize_youtube_url(url: str) -> str`: Normalizes YouTube URLs to a standard format.
*   `check_youtube_availability(url: str) -> bool`: Checks if a YouTube video is available using `yt-dlp`.
*   `open_link(url: str)`: Opens a URL in the default web browser, with special handling for YouTube.
*   `download_youtube_video(youtube_url: str, output_path: str = "downloads")`: Downloads a YouTube video to the specified path using `yt-dlp`.
*   `process_command(query: str)`: Processes the user's command or question and calls the appropriate function.
*   `main()`: Main function to start the assistant.

### Main Loop

*   The `main` function continuously gets user input and processes it until the user enters an exit command.
*   Includes error handling to catch unexpected exceptions and shut down gracefully.

## Error Handling

*   The script includes comprehensive error handling for:
    *   Text-to-speech initialization.
    *   Reading user input.
    *   Fetching responses from the Gemini API.
    *   Opening URLs.
    *   Downloading YouTube videos (including checking for private or restricted videos).
    *   General exceptions that may occur during the execution of the script.

## Notes

*   Ensure your Google Gemini API key is valid and properly set up.
*   The music directory path should be correctly configured for the music playback feature to work.
*   The `yt-dlp` library is used for downloading YouTube videos. Ensure it is installed and up-to-date.
*   The script preserves the case of URLs where possible to ensure compatibility.
*   The script checks for YouTube availability before attempting to open or download a video.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues for bug fixes or feature requests.
