from pydub import AudioSegment


class Track(object):
    status: int = 0

    def __init__(self, name: str, path: str, audio: AudioSegment):
        self.name = name
        self.path = path
        self.audio = audio

    def copy(self):
        """ Will return copy of this track, but without audio data"""
        track = Track(self.name, self.path, None)
        track.status = self.status
        return track
