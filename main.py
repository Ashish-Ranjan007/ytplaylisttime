import os 
import sys
import json 
import isodate
import requests
from halo import Halo
from dotenv import load_dotenv
from datetime import timedelta


# Load environment variables
load_dotenv()

def get_playlist_id(playlist_url):
	"""Extracts the playlist ID from a YouTube playlist URL.

	Args:
	  playlist_url (str): The URL of the YouTube playlist.

	Returns:
	  str: The playlist ID, or None if the URL is not a valid YouTube playlist URL.
	"""

	# Check if the URL is a valid YouTube playlist URL
	if not playlist_url.startswith("https://youtube.com/playlist"):
		print("Invalid URL provided.")
		return None

	# Extract the part after "list="
	parts = playlist_url.split("list=")
	if len(parts) != 2:
		print("Invalid URL provided.")
		return None

	playlist_id = parts[1].split("&")[0]
	return playlist_id

def format_duration(duration):
	"""
	Converts a duration string in "Days:Hours:Minutes:Seconds" format to "w days x hours y minutes z seconds" format.

	Args:
	    duration_str (str): The duration string in "Days:Hours:Minutes:Seconds" format.

	Returns:
	    str: The formatted duration string in "w days x hours y minutes z seconds" format.
	"""
	if duration == "":
		return "0 Seconds"

	format_arr = duration.split(":")
	length = len(format_arr)

	if length == 4:
		return format_arr[0] + " Days, " + format_arr[1] + " Hours, " + format_arr[2] + " Minutes, " + format_arr[3] + " Seconds"
	elif length == 3:
		return format_arr[0] + " Hours, " + format_arr[1] + " Minutes, " + format_arr[2] + " Seconds"
	elif length == 2:
		return format_arr[0] + " Minutes, " + format_arr[1] + " Seconds"
	return format_arr[0] + " Seconds"

def get_playlist_details(playlist_url):
	"""
	Returns a dictionary containing various playlist description
	
	Args:
		playlist_url (str): The URL of the YouTube playlists.

	Returns:
		dict: {
			channel_name (str): Name of the youtube channel,
			itemCount (int): Number of videos in the playlist,
			title (str): Title of the playlist,
			description (str): Description of the playlist
		}
	"""
	result = {
		"channel_name": "",
		"itemCount": 0,
		"title": "",
		"description": ""
	}
	playlist_id = get_playlist_id(playlist_url)
	api_key = os.environ.get("YOUTUBE_API_KEY")
	url = "https://www.googleapis.com/youtube/v3/playlists/?key=" + api_key + "&id=" + playlist_id + "&part=snippet,contentDetails"

	try:
		response = requests.get(url)
		if response.status_code == 200:
			data = response.json()
			items = data.get("items")
			snippet = items[0].get("snippet")
			content_details = items[0].get("contentDetails")

			result["channel_name"] = snippet.get("channelTitle")
			result["title"] = snippet.get("title")
			result["description"] = snippet.get("description") or "No description yet."
			result["itemCount"] = content_details.get("itemCount")
		else:
			print("No details found for provided playlist URL.")
	except requests.exception.RequestException as err:
		print("Error:", err)

	return result

def get_playlist_length(playlist_url):
	"""
	Returns the length of a YouTube playlist.

	Args:
	  playlist_url (str): The URL of the YouTube playlist.

	Returns:
	  timedelta: The length of the playlist in timedelta
	"""

	result = timedelta(0)
	nextPageToken = ""
	api_key = os.environ.get("YOUTUBE_API_KEY")
	playlist_id = get_playlist_id(playlist_url)

	while True:
		video_ids = [] # stores an array of IDs of videos in a playlist
		playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems/?key=" + api_key + "&playlistId=" + playlist_id + "&part=snippet" + "&maxResults=50" + "&pageToken=" + nextPageToken

		# Construct an array of video IDs that are the part of playlist
		try:
			playlist_response = requests.get(playlist_url)
			if playlist_response.status_code != 200:
				print("Error retrieving playlist data.")
				break

			playlist_data = playlist_response.json()
			if not playlist_data:
				print("Error retrieving playlist data.")
				break

			playlist_items = playlist_data.get("items")
			if not playlist_items:
				print("No items found in playlist response.")
				break 

			for item in playlist_items:
				snippet = item.get("snippet")
				if not snippet:
					print("No snippet found in playlist item")

				resource_id = snippet.get("resourceId")
				if not resource_id:
					print("No resourceId found in playlist item's snippet")

				video_id = resource_id.get("videoId")
				if not video_id:
					print("No video_id found in playlist item's resourceId")

				video_ids.append(video_id)
		except requests.exception.RequestException as err:
			print("Enter:", err)
			break

		# Make the video_ids array into a single string of comma separated values to be passed into url as a parameter
		video_ids_string = ','.join(video_ids)

		video_url = "https://www.googleapis.com/youtube/v3/videos/?key=" + api_key + "&id=" + video_ids_string + "&part=contentDetails" + "&maxResults=50"

		# Go through each video and add its duration to result
		try:
			video_response = requests.get(video_url)
			if video_response.status_code != 200:
				print("Error retrieving playlist data.")
				break

			video_data = video_response.json()
			if not video_data:
				print("Error retrieving playlist data.")
				break

			video_items = video_data.get("items")
			if not video_items:
				print("No items found in video response.")
				break;	

			for item in video_items:
				content_details = item.get("contentDetails")
				if not content_details:
					print("No contentDetails found in video item")

				duration = content_details.get("duration")
				if not duration:
					print("No duration found in video item's content_details")

				result += isodate.parse_duration(duration)

		except requests.exception.RequestException as err:
			print("Error:", err)
			break

		if playlist_data.get("nextPageToken"):
			nextPageToken = playlist_data.get("nextPageToken")
		else:
			break

	return result

def main():
	if len(sys.argv) != 2:
		print("Usage: ytplaylisttime <playlist_url>")
		return None

	spinner = Halo(text="Fetching...", spinner="pipe")
	spinner.start()
	playlist_url = sys.argv[1]
	playlist_details = get_playlist_details(playlist_url)
	playlist_length = get_playlist_length(playlist_url)
	spinner.stop()
	
	print("Title:", playlist_details["title"])
	print("Channel:", playlist_details["channel_name"])
	print("Description:", playlist_details["description"])
	print("Number of videos:", playlist_details["itemCount"])
	print("Playlist length:", format_duration(str(playlist_length)))

if __name__ == "__main__":
	main()