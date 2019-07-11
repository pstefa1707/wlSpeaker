#coding: utf-8
import json
# Spotify library.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# URL conversions.
import urllib.request
from bs4 import BeautifulSoup
# Youtube stuff.

#Enter spotify client id and secret for api
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"

def getTracks(playlistURL):
	client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
	spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	results = spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

	trackList = []
	for i in results["tracks"]["items"]:
		if (i["track"]["artists"].__len__() == 1):
			trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])
		else:
			nameString = ""
			for index, b in enumerate(i["track"]["artists"]):
				nameString += (b["name"])
				if (i["track"]["artists"].__len__() - 1 != index):
					nameString += ", "
			trackList.append(i["track"]["name"] + " - " + nameString)

	return trackList

def searchYoutube(url):
	# YouTube will block you if you query too many songs using this search.
	print(url)
	response = urllib.request.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return 'https://www.youtube.com' + soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]['href']

def songToYoutubeQuery(songList):
	urls = []
	for i in songList:
		textToSearch = i
		query = urllib.parse.quote(textToSearch)
		url = "https://www.youtube.com/results?search_query=" + query
		urls.append(url)
	return urls

if (__name__ == "__main__"):
	print("Accessible via player")