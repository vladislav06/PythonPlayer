from player.track import Track


class Playlist(object):
    tracks: [Track] = []
    name: str = "ee"

    def __init__(self,  name: str,tracks: [Track]):
        self.tracks = tracks
        self.name = name
