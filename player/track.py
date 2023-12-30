from pydub import AudioSegment


class Track:
    def __init__(self, name: str, path: str, audio: AudioSegment):
        self.name = name
        self.path = path
        self.audio = audio
