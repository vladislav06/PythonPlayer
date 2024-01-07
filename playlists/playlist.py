from player.track import Track


class Playlist(object):
    tracks: [Track] = []
    name: str = "ee"
    index: int = 0

    def __init__(self, name: str, tracks: [Track]):
        self.tracks = tracks
        self.name = name
        # number track in order
        n = 0
        for track in self.tracks:
            track.index = n
            n += 1

    def add(self, track: Track):
        track.index = len(self.tracks)
        self.tracks.append(track)

    def to_json(self):
        return {"name": self.name, "tracks": list(map(lambda x: x.to_json(), self.tracks))}

    def from_json(jsn):
        return Playlist(jsn["name"], list(map(lambda x: Track.from_json(x), jsn['tracks'])))
