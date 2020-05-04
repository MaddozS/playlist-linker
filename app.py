import spotipy
import spotipy.util as util
import os
import sys
from config import Config
from spotipy.oauth2 import SpotifyClientCredentials

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

class PlaylistLinker:
    
    def __init__(self):
        # Load the all the configurations of different streaming services
        self.config = Config('config.cfg')
        # For now, this is only used in the spotify API
        self.username = os.environ.get('USERNAME')
        # Since youtube is our base, we need to authenticate it
        self.start_youtube()

    def start_youtube(self):
        # Youtube API Credentials
        CLIENT_SECRETS_FILE = "client_secrets.json"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

        %s

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        CLIENT_SECRETS_FILE))

        # This OAuth 2.0 access scope allows for full read/write access to the
        # authenticated user's account.
        YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
            message=MISSING_CLIENT_SECRETS_MESSAGE,
            scope=YOUTUBE_SCOPE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = argparser.parse_args()
            credentials = run_flow(flow, storage, flags)

        # Saving the youtube information
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http())
        )

    def start_spotify(self):
        self.spotify_token = util.prompt_for_user_token(
            self.username,
            scope="playlist-read-private playlist-read-collaborative",
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            redirect_uri=self.config.redirect_uri
        )

    def get_spotify_playlists(self):
        if self.spotify_token:
            sp = spotipy.Spotify(auth=self.spotify_token)
            playlists = sp.current_user_playlists()['items']
      
            for playlist in self.playlists:
                print(playlist['name'] + ' - ' + playlist['owner']['id'] + "- id: " + playlist['id'])
        else:
            print("Can't get token for", username)
    
    def get_playlist_youtube(self):
        youtube_playlist = self.youtube.playlists()
        print(youtube_playlist)

    def get_spotify_uri(self):
        pass

    def add_song(self):
        pass

if __name__ == "__main__":
    pl = PlaylistLinker()
    pl.start_spotify()
    pl.get_spotify_playlists()

