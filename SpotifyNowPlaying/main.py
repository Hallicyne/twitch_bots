import spotipy
import spotipy.util as util
import socket

def main():
	scope = "user-read-currently-playing"
	client_id = ''								# client ID from https://developer.spotify.com/dashboard/applications 
	client_secret = ''							# client secret from https://developer.spotify.com/dashboard/applications
												# Log into your account and create a new App, a client ID & Client Secret
	username = ''								# your spotify username
	redirect_uri = "http://localhost/"

	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

	sp = spotipy.Spotify(auth=token)

	currentsong = sp.currently_playing()

	bot_owner = '' 								# your twitch user
	nickname = ''								# your twitch user / bot user
	channel = '#'								# your twitch channel
	server = "irc.chat.twitch.tv"
	password = ''								# oauth token, got to https://twitchapps.com/tmi/ and connect account then copy the oauth token in here

	irc = socket.socket()
	irc.connect((server, 6667))

	irc.send(f'PASS oauth:{password} \r\n'.encode('utf-8'))
	irc.send(f'USER {bot_owner} 0 * : {username}}\r\n'.encode('utf-8'))
	irc.send(f'NICK {nickname}}\r\n'.encode('utf-8'))
	irc.send(f'JOIN #{channel}\r\n'.encode('utf-8')) 
	
	song_name = currentsong['item']['name']
	song_artist = currentsong['item']['artists'][0]['name']
	artist_url = currentsong['item']['artists'][0]['external_urls']['spotify']

	r = open("last_played.txt", "r")
	last_played = r.read()
	while 0:
		if song_name != last_played:
			print(f"Change song: {song_name} by {song_artist}")
			irc.send(f'PRIVMSG #{channel} : Now Playing {song_name} by {song_artist}, visit the artist page: {artist_url}\r\n'.encode('utf-8'))
			f = open("last_played.txt", "w")
			f.write(song_name)
			f.close()
		else:
			print("Nothing to update, waiting....")

main()
