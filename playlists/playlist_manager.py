import json

import jsonpickle

from player.track import Track
from playlists.playlist import Playlist
from playlists.song_manager import TrackManager


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

        # check if track exist
        playlists: [Playlist] = []
        for playlist in self.playlists:
            pl: [Playlist] = Playlist(playlist.name, [])
            for track in playlist.tracks:
                if not TrackManager.check_existence(track):
                    track.exist = False
                    pl.tracks.append(track)
                else:
                    track.exist = True
            if len(pl.tracks) != 0:
                playlists.append(pl)

        return playlists
