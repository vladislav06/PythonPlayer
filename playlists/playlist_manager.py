from tinytag import TinyTag

import json
import jsonpickle
import os

from player.track import Track
from playlists.playlist import Playlist
from playlists.song_manager import TrackManager

# At least on Windows, if a metadata field is empty, tinytag will always yield this string:
tinytag_empty_data_string = '                              '
# It's used here to check whether certain metadata exists or not.

# Function to convert data from track_metadata.duration to minutes for display:
def ConvertToMinutes(seconds):
    # Convert to int
    seconds = int(seconds)
    # Figure out minutes
    minutes = seconds // 60
    # Figure out remaining seconds
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

class PlaylistManager:
    playlists: [Playlist] = []

    FILE_NAME: str = "playlists.json"

    def save_playlists(self):
        """ Will save playlists to a file"""
        f = open(self.FILE_NAME, "w")
        jsn = map(lambda x: x.to_json(), self.playlists)
        json.dump(list(jsn), f)
        f.flush()
        f.close()

    def load_playlists(self) -> [Playlist]:
        """ Will load playlists from a file and will check if tracks exist.
        Will return list of Playlists with tracks that don't exist"""
        f = open(self.FILE_NAME, "r")
        jsn = json.load(f)
        self.playlists = list(map(lambda x: Playlist.from_json(x), jsn))
        n = 0
        for playlist in self.playlists:
            playlist.index = n
            n += 1
        f.close()

        # check if track exists
        playlists: [Playlist] = []
        for playlist in self.playlists:
            pl: [Playlist] = Playlist(playlist.name, [])
            for track in playlist.tracks:
                if not TrackManager.check_existence(track):
                    track.exist = False
                    pl.tracks.append(track)
                else:
                    track.exist = True
                    # Search for metadata
                    track_metadata = TinyTag.get(os.path.join(track.path, track.name))
                    # Save track name, display file name if title is empty in metadata
                    if track_metadata.title != tinytag_empty_data_string:
                        track.title = track_metadata.title
                    else:
                        track.title = track.name
                    # Show artist name, display - if artist is empty in metadata
                    if track_metadata.artist != tinytag_empty_data_string:
                        track.title = track_metadata.artist
                    else:
                        track.artist = '-'
                    # Get duration, convert to minutes and save as string
                    track.duration = ConvertToMinutes(track_metadata.duration)

        if len(pl.tracks) != 0:
                playlists.append(pl)

        return playlists
