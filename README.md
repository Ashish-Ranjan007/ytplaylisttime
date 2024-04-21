# YouTube Playlist Duration Calculator

## Overview

This Python script allows users to retrieve various details about a YouTube playlist and calculate its total duration. It utilizes the YouTube Data API to fetch playlist information and extract video durations.

## Features

- Extracts details such as title, channel name, description, and number of videos from a YouTube playlist URL.
- Calculates the total duration of all videos in the playlist.
- Provides formatted output displaying the collected information.

## Requirements

- Python 3.x
- Requests library (`pip install requests`)
- isodate library (`pip install isodate`)
- halo library (`pip install halo`)
- dotenv library (`pip install python-dotenv`)

## Usage

1. Clone the repository.
2. Install the required dependencies listed above.
3. Set up a `.env` file in the same directory as the script and provide your YouTube Data API key:

   ```plaintext
   YOUTUBE_API_KEY=YOUR_API_KEY
   ```
4. Run the script from the command line with the following command:

   ```bash
   $ python main.py <playlist_url>
   ```

   Replace `<playlist_url>` with the URL of the YouTube playlist you want to analyze.

## Example

```bash
$ python main.py https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
```

## Shell Script (Linux)

- If you're using Linux or macOS, you can use the provided shell script `ytplaylisttime.sh`.
- Make sure the script has execute permissions (`chmod +x ytplaylisttime.sh`).
- Also make sure to add the path to main.py in ytplaylisttime.sh file.
- Run the script from the terminal with the following command:

   ```bash
   $ ./ytplaylisttime.sh <playlist_url>
   ```

## Example

```bash
$ ./ytplaylisttime.sh https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
```

## Batch Script (Windows)

- For Windows users, there's a batch script `ytplaylisttime.bat`.
- Make sure to add the path to main.py in ytplaylisttime.bat file.
- Run the script from the command prompt:

   ```powershell
   > ytplaylisttime.bat <playlist_url>
   ```

## Example

```powershell
> .\ytplaylisttime.bat https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID
```

## Testing
- This project includes a test file test_main.py for testing various functionalities.
- To run the tests, ensure you have pytest installed (pip install pytest).
- Run the tests by executing pytest from the terminal:
```bash
$ py.test
```

## Note

- Ensure that the provided playlist URL is valid and accessible.
- The script may require a valid YouTube Data API key to access playlist information. Instructions for obtaining an API key can be found in the YouTube Data API documentation.