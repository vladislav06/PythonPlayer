import numpy
import numpy as np

from util.serializable import Serializable


class Audio:
    _data: np.ndarray
    _frame_width = 4
    _frame_rate = 0
    _frame_count = 0
    _channels = 2
    _len_ms = 0

    def __init__(self, data, frame_width, frame_rate, frame_count, channels, len_ms):
        self._data = data
        self._frame_width = frame_width
        self._frame_rate = frame_rate
        self._frame_count = frame_count
        self._channels = channels
        self._len_ms = len_ms

    @property
    def raw_data(self) -> numpy.ndarray:
        return self._data

    @property
    def frame_width(self):
        return self._frame_width

    @property
    def frame_rate(self):
        return self._frame_rate

    @property
    def frame_count(self):
        return self._frame_count

    @property
    def channels(self):
        return self._channels

    @property
    def len_ms(self):
        return self._len_ms


class Track(Serializable):
    status: int = 0
    max_status = 1
    is_loaded: bool = False
    name: str = ""
    path: str = ""
    audio: Audio | None = None
    index: int = 0
    exist: bool = False
    # Metadata
    title: str = ""
    artist: str = ""
    duration: str = ""

    def __init__(self, name: str, path: str, audio: Audio | None = None):
        self.name = name
        self.path = path
        self.audio = audio
        self.title =name

    def copy(self):
        """ Will return copy of this track, but without audio data"""
        track = Track(self.name, self.path)
        track.status = self.status
        track.max_status = self.max_status
        track.is_loaded = self.is_loaded
        track.index = self.index

        return track

    def to_json(self):
        return {"name": self.name, "path": self.path}

    def from_json(jsn):
        return Track(jsn['name'], jsn['path'])

    def __str__(self):
        return f'{{{self.name}, {self.path}}}'
