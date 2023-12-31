import json

import jsonpickle

from playlists.playlist import Playlist


class PlaylistManager:
    playlists: [Playlist] = []

    def save_playlists(self):
        f = open("playlists.json", "w")
        f.write(jsonpickle.encode(self.playlists, unpicklable=False))
        f.flush()
        f.close()
