from pydub import AudioSegment

from util.serializable import Serializable


class Track(Serializable):
    status: int = 0
    name: str = ""
    path: str = ""
    audio: AudioSegment | None = None

    def __init__(self, name: str, path: str, audio: AudioSegment | None = None):
        self.name = name
        self.path = path
        self.audio = audio

    def copy(self):
        """ Will return copy of this track, but without audio data"""
        track = Track(self.name, self.path)
        track.status = self.status
        return track

    def to_json(self):
        return {"name": self.name, "path": self.path}

    def from_json(jsn):
        return Track(jsn['name'], jsn['path'])

    def __str__(self):
        return f'{{{self.name}, {self.path}}}'
