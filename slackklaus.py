import time, re, spotipy, os
import spotipy.util as util
from slackclient import SlackClient

# get all required settings
slack_api_key = os.environ["KLAUS_SLACK_API_KEY"]
spotify_playlist_user = os.environ["KLAUS_SPOTIFY_PLAYLIST_USER"]
spotify_playlist_id = os.environ["KLAUS_SPOTIFY_PLAYLIST_ID"]
spotify_api_client_id = os.environ["KLAUS_SPOTIFY_API_CLIENT_ID"]
spotify_api_secret = os.environ["KLAUS_SPOTIFY_API_CLIENT_SECRET"]
spotify_api_callback_url = os.environ["KLAUS_SPOTIFY_API_CALLBACK_URL"]

sc = SlackClient(slack_api_key)
spre = re.compile(r"(?!spotify\:|http(?!s))\:\/\/[a-z]+\.spotify\.com\/(track|artist|album)(?:\:|\/)([a-zA-Z0-9]+)")

# check if we're connected
if sc.rtm_connect():
    while True:
        # get latest messages
        msg = sc.rtm_read()
        for d in msg:
            # make sure we have an actual message
            if d.get('text') and len(spre.findall(d.get('text'))):
                # extract some required information from the spotify link
                rc = spre.findall(d.get('text'))
                for f in rc:
                    sid = f[1]
                    # make sure we have a track link
                    if f[0] == 'track':
                        # check history if we added this track already
                        f = open('pltracks.txt', 'r+')
                        exists = False
                        for line in f:
                            if(line.rstrip() == sid):
                                # track already exists
                                exists = True

                        if exists == False:
                            # get new spotify api token to work with
                            token = util.prompt_for_user_token(spotify_playlist_user, 'playlist-modify playlist-modify-public playlist-modify-private', spotify_api_client_id, spotify_api_secret, spotify_api_callback_url)
                            sp = spotipy.Spotify(auth=token)
                            try:
                                # add track to playlist
                                sp.user_playlist_add_tracks(spotify_playlist_user, spotify_playlist_id, ["spotify:track:"+sid])
                                # add track to history file
                                f.write(sid+'\n')
                                # react to message to confirm we successfully added the track
                                sc.api_call('reactions.add', channel=d.get('channel'), name="spotify", timestamp=d.get('ts'))
                            except Exception as e:
                                print(e.msg)
                        f.close()
        # have some rest
        time.sleep(3)
else:
    print("Connection failed.")
