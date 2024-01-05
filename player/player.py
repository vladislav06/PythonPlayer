from pydub import AudioSegment
import numpy as np
#
from enum import Enum
import pyaudio

from player.track import Track


class Player:
    cross_fade_length = 3000
    """ Cross fade length in ms """

    class PlaybackStatus(Enum):
        PLAY = 1
        PAUSE = 2

    current_track: Track | None = None
    next_track: Track | None = None

    playback: pyaudio.PyAudio
    playback_stream: pyaudio.Stream = None
    # Stuff for playback
    playback_current_frame_count: int = 0
    playback_next_frame_count: int = 0

    playback_fade: float = 0
    """0 - current track plays\n
       1 - next track plays"""

    playback_frame_len: int = 96 * 4
    playback_level: float = 0

    playback_status: PlaybackStatus = PlaybackStatus.PAUSE
    playback_pause_frame_count: int = 0

    play_next_track: bool = False

    def _playback_stream_callback(self, in_data, frame_count, time_info, status):
        """ This method is called when output stream requires some data, aka main audio loop """
        try:

            print("playing")
            # play status handling
            match self.playback_status:
                case self.PlaybackStatus.PLAY:
                    if self.playback_level < 1:
                        self.playback_level += 0.005
                    else:
                        self.playback_level = 1
                case self.PlaybackStatus.PAUSE:
                    if self.playback_level > 0:
                        self.playback_level -= 0.01 * self.playback_level ** 0.5
                    else:
                        self.playback_level = 0
            # end stream if nothing to play
            if self.current_track is None:
                print("stopped current_track")
                self.playback_status = self.PlaybackStatus.PAUSE
                return bytes([1]), pyaudio.paComplete

            # stop playback when music is fully paused
            if self.playback_level == 0:
                print("stopped playback_level")
                return bytes([1]), pyaudio.paComplete

            # check if fade is required
            next_data = None
            if (1000 * ((self.current_track.audio.frame_count() - self.playback_current_frame_count)
                        / self.current_track.audio.frame_rate)) <= self.cross_fade_length or self.play_next_track:
                print("must fade:", self.play_next_track)
                if self.next_track is not None:
                    # get next track frame data
                    start_next = self.playback_next_frame_count * self.next_track.audio.frame_width
                    end_next = (self.playback_next_frame_count + frame_count) * self.next_track.audio.frame_width
                    next_data = self.next_track.audio.raw_data[start_next:end_next]
                    self.playback_next_frame_count += frame_count
                else:
                    # or next track is empty aray
                    end_next = frame_count * self.current_track.audio.frame_width
                    next_data = bytes([0] * end_next)
                    self.playback_next_frame_count += frame_count

            # get current track frame data
            start = self.playback_current_frame_count * self.current_track.audio.frame_width
            end = (self.playback_current_frame_count + frame_count) * self.current_track.audio.frame_width
            data = self.current_track.audio.raw_data[start:end]
            self.playback_current_frame_count += frame_count

            # do some fast multiplication
            dtype = "int16"
            data = np.frombuffer(data, dtype=dtype)

            if next_data is not None:
                next_data = np.frombuffer(next_data, dtype=dtype)
                # fade between current and next data frame
                data = (data * (1 - self.playback_fade)) + (next_data * self.playback_fade)
                # calculate fade speed based on fade length, frame rate and frames per call (frame_count)
                self.playback_fade += \
                    1 / (((self.current_track.audio.frame_rate * (self.cross_fade_length / 1000))
                          - frame_count * 2) / frame_count)
                # fade ended,move next track to current
                if self.playback_fade > 1:
                    self.play_next_track = False
                    self.current_track = self.next_track
                    self.next_track = None
                    self.playback_current_frame_count = self.playback_next_frame_count
                    self.playback_fade = 0

            data = data * self.playback_level
            data = bytes(data.astype(dtype))
            self.current_track.status = self.playback_current_frame_count
            return data, pyaudio.paContinue
        except Exception as e:
            print(e)
            return bytes([1]), pyaudio.paComplete

    def init_player(self):
        """ Initializes player, must be called before any other function! """
        self.playback = pyaudio.PyAudio()

    def _start_playback_stream(self):
        def _callback(in_data, frame_count, time_info, status):
            return self._playback_stream_callback(in_data, frame_count, time_info, status)

        self.playback_stream = self.playback.open(
            format=self.playback.get_format_from_width(self.current_track.audio.sample_width),
            channels=self.current_track.audio.channels,
            rate=self.current_track.audio.frame_rate,
            output=True,
            frames_per_buffer=self.playback_frame_len,
            stream_callback=_callback)
        self.playback_stream.start_stream()

    # API

    def play(self):
        """ Will start playing current track """
        print("play")
        if self.playback_status == self.PlaybackStatus.PAUSE:
            self.playback_status = self.PlaybackStatus.PLAY
            self.playback_current_frame_count = self.playback_pause_frame_count

        if self.playback_stream is None:
            self._start_playback_stream()

        if not self.playback_stream.is_active():
            self.playback_stream.close()
            self._start_playback_stream()

    def pause(self):
        """ Will pause current track """
        print("pause")
        self.playback_status = self.PlaybackStatus.PAUSE
        self.playback_pause_frame_count = self.playback_current_frame_count

    def set_next(self, track: Track):
        """" Will set next track to play """
        print("set_next:", track.name)
        # fade music in
        if self.current_track is None:
            self.current_track = track
        else:
            self.next_track = track

    def play_next(self):
        print("play_next")
        self.play_next_track = True
