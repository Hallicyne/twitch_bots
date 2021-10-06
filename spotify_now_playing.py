import spotipy
import spotipy.util as util
import socket

def Main():
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

	irc.send('PASS oauth:{} \r\n'.format(password).encode('utf-8'))
	irc.send('USER {} 0 * : {}}\r\n'.format(bot_owner, username).encode('utf-8'))
	irc.send('NICK {}}\r\n'.format(nickname).encode('utf-8'))
	irc.send('JOIN #{}\r\n'.format(channel).encode('utf-8')) 
	
	song_name = currentsong['item']['name']
	song_artist = currentsong['item']['artists'][0]['name']
	artist_url = currentsong['item']['artists'][0]['external_urls']['spotify']

	r = open("last_played.txt", "r")
	last_played = r.read()

	if song_name != last_played:
		print("Change song: {} by {}".format(song_name, song_artist))
		irc.send('PRIVMSG #ota__ : Now Playing {} by {}, visit the artist page: {}\r\n'.format(song_name, song_artist, artist_url).encode('utf-8'))
		f = open("last_played.txt", "w")
		f.write(song_name)
		f.close()
	else:
		print("Nothing to update, waiting....")

Main()