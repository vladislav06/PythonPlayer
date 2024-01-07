import os

import numpy as np
from tinytag import TinyTag

from player.track import Track, Audio
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence, detect_silence
from pythonlangutil.overload import Overload, signature

# At least on Windows, if a metadata field is empty, tinytag will always yield this string:
tinytag_empty_data_string = ''


class TrackManager:
    tracks: list[Track] = []

    def load_from_folder(self, path: str):
        os.path.isdir(path)
        # iterate over files in
        # that directory
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.load(f)

    def _process_audio(self, audio: AudioSegment) -> AudioSegment:
        effects.normalize(audio)
        # remove silence at start and the end
        silence = detect_silence(
            audio,
            min_silence_len=100,
            silence_thresh=-35,
        )
        if len(silence) > 1:
            # remove at start and end
            audio = audio[silence[0][1]:silence[-1][0]]
            print("from:", silence[0][1], "to:", silence[-1][0])
            print("len:", len(audio))
        if len(silence) == 1:
            # remove at start
            audio = audio[silence[0][1]:]
            print("from:", silence[0][1], "to:", "end")
            print("len:", len(audio))

        return audio

    @Overload
    @signature("str")
    def load(self, path: str):
        audio: AudioSegment = AudioSegment.from_file(path, path.split(".")[-1])
        track: Track = Track(path.split("/")[-1], path, audio)
        self.tracks.append(track)

    @load.overload
    @signature("Track")
    def load(self, track: Track):
        if not track.exist:
            return
        au: AudioSegment = AudioSegment.from_file(os.path.join(track.path, track.name), track.name.split('.')[-1])
        # np = self._read(au)
        track.audio = Audio(au.raw_data, au.frame_width, au.frame_rate, au.frame_count(), au.channels, len(au))
        track.max_status = track.audio.frame_count
        track.is_loaded = True
        self.tracks.append(track)

    @staticmethod
    def check_existence(track: Track) -> bool:
        return os.path.isfile(os.path.join(track.path, track.name))

    def _read(self, a: AudioSegment, normalized=False):
        """MP3 to numpy array"""
        dtype = "uint8"
        y = np.frombuffer(a.raw_data, dtype=dtype)
        return y

    @staticmethod
    def ConvertToMinutes(secs):
        # Convert to int
        seconds = int(secs)
        # Figure out minutes
        minutes = seconds // 60
        # Figure out remaining seconds
        seconds %= 60
        return "%02d:%02d" % (minutes, seconds)

    @staticmethod
    def load_metadata(track):
        # Search for metadata
        track_metadata = TinyTag.get(os.path.join(track.path, track.name))
        # Save track name, display file name if title is empty in metadata
        if track_metadata.title != tinytag_empty_data_string and track_metadata.artist  is not None:
            track.title = track_metadata.title
        else:
            track.title = track.name
        # Show artist name, display - if artist is empty in metadata
        if track_metadata.artist != tinytag_empty_data_string and track_metadata.artist is not None:
            track.artist = track_metadata.artist
        else:
            track.artist = None
        # Get duration, convert to minutes and save as string
        track.duration = TrackManager.ConvertToMinutes(track_metadata.duration)
