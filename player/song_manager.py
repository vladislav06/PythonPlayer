import os

from player.track import Track
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence, detect_silence


class SongManager:
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

    def load(self, path: str):
        audio: AudioSegment = AudioSegment.from_file(path, path.split(".")[-1])
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

        track = Track(path.split("/")[-1], path, audio)
        self.tracks.append(track)
