from player.player_manager import PlayerManager
from player.track import Track
from playlists.playlist import Playlist
from playlists.song_manager import SongManager
from util.notifier import Notifier
from util.pereodic import Periodic


class PlayerControl:
    """High abstraction class for controlling player, must be used by ui"""
    playlist_notifier: Notifier[Playlist]
    track_notifier: Notifier[Track]
    song_manager: SongManager
    player: PlayerManager
    periodic: Periodic

    def __init__(self, player, song_manager, playlist_notifier, track_notifier):
        self.player = player
        self.song_manager = song_manager
        self.playlist_notifier = playlist_notifier
        self.track_notifier = track_notifier

        # start getting track info from player
        self.periodic = Periodic(0.1, self._periodic)

    def init(self):
        self.periodic.start()

    def play_pause(self):
        self.player.play()
        pass

    def forward(self):
        if self.track_notifier.value is None:
            next_index = 0
        else:
            next_index = self.track_notifier.value.index + 1
        if next_index >= len(self.playlist_notifier.value.tracks):
            next_index = 0
        self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
        self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
        self.player.play_next()

    def backward(self):
        progress = self.get_progres()
        if progress < 0.2:
            # play prev track
            next_index = self.track_notifier.value.index - 1
            if next_index < 0:
                next_index = len(self.playlist_notifier.value.tracks) - 1
            self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
            self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
            self.player.play_next()
        else:
            # switch to track start
            self.track_notifier.value.status = 0
            self.player.set_next_track(self.track_notifier.value)
            self.track_notifier.value = self.track_notifier.value
            self.track_notifier.notify()
            self.player.play_next()

    def get_progres(self) -> float:
        """Will return current track playback progress, 0 start 1 end"""
        track = self.track_notifier.value
        if track is None:
            return 0
        return track.status / track.max_status

    def _periodic(self):
        """This periodic function will update currently playing track status"""
        self.track_notifier.value = self.player.get_status()
