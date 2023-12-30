from pydub import AudioSegment
import threading
import os
from pydub.playback import play
import simpleaudio
from simpleaudio import PlayObject
from pydub.silence import split_on_silence, detect_silence
from pydub import AudioSegment, effects
import wave
import numpy as np


class Track:
    def __init__(self, name: str, path: str, audio: AudioSegment):
        self.name = name
        self.path = path
        self.audio = audio


class Player:
    pass


class Player:
    tracks: list[Track] = []
    playback: PlayObject

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
            # remove at start
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

    def start_play(self):
        track = self.tracks[0]

        fade_track = self.tracks[0].audio.append(self.tracks[1].audio, crossfade=1500)

        self.playback = simpleaudio.play_buffer(
            fade_track.raw_data,
            num_channels=track.audio.channels,
            bytes_per_sample=track.audio.sample_width,
            sample_rate=track.audio.frame_rate
        )
