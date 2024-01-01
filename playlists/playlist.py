from player.track import Track


class Playlist(object):
    tracks: [Track] = []
    name: str = "ee"

    def __init__(self, name: str, tracks: [Track]):
        self.tracks = tracks
        self.name = name

    def to_json(self):
        return {"name": self.name, "tracks": list(map(lambda x: x.to_json(), self.tracks))}

    def from_json(jsn):
        return Playlist(jsn["name"], list(map(lambda x: Track.from_json(x), jsn['tracks'])))
