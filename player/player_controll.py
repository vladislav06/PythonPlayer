import asyncio

from player.player_interface import TrackMessage
from player.player_manager import PlayerManager
from player.track import Track
from playlists.playlist import Playlist
from playlists.track_manager import TrackManager
from util.notifier import Notifier
from util.pereodic import Periodic


class PlayerControl:
    """High abstraction class for controlling player, must be used by ui"""
    playlist_notifier: Notifier[Playlist]
    track_notifier: Notifier[Track]
    track_manager: TrackManager
    player: PlayerManager
    # Very convoluted mess of flags and ifs to cover all edge cases
    track_status_notifier: Notifier[Track]
    track_full_status: TrackMessage
    next_track: Track
    is_playing: bool = False

    def __init__(self, player, song_manager, playlist_notifier, track_notifier, track_status_notifier):
        self.player = player
        self.track_manager = song_manager
        self.playlist_notifier = playlist_notifier
        self.track_notifier = track_notifier
        self.track_status_notifier = track_status_notifier

    def stop(self):
        self.player.proc.kill()

    def play_pause(self):
        """Play/pause"""
        if self.is_playing:
            self.player.pause()
        else:
            self.player.play()
        self.is_playing = not self.is_playing

    def play(self, track: Track):
        """Will play specified track, assuming that playlist that this track belongs to is already selected"""
        self.track_notifier.value = track

        if not track.is_loaded:
            self.track_manager.load(track)

        status = self.player.get_full_status()
        if status.current_track_exist:
            if not self.is_playing:
                self.player.set_current_track(track)
            else:
                self.player.set_next_track(track)
                self.player.play_next()
        else:
            self.player.set_current_track(track)
        self.next_track = track

        if not self.is_playing:
            self.player.play()
            self.is_playing = True

    def forward(self, force=True):
        """Forwards to the next track in current playlist, if current track is last,
        will loop to playlist beginning"""
        # search for next available track
        if self.track_notifier.value is None:
            next_index = 0
        else:
            next_index = self.track_notifier.value.index + 1
        if next_index >= len(self.playlist_notifier.value.tracks):
            next_index = 0
        while not self.playlist_notifier.value.tracks[next_index].exist:
            next_index += 1
            if next_index >= len(self.playlist_notifier.value.tracks):
                next_index = 0

        # play music from start
        self.playlist_notifier.value.tracks[next_index].status = 0
        # load
        if not self.playlist_notifier.value.tracks[next_index].is_loaded:
            self.track_manager.load(self.playlist_notifier.value.tracks[next_index])

        status = self.player.get_full_status()

        # play
        if status.current_track_exist:
            # print("current_track_exist")
            # if not self.is_playing:
            #    self.player.set_current_track(self.playlist_notifier.value.tracks[next_index])
            # else:
            #    self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
            self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
            self.next_track = self.playlist_notifier.value.tracks[next_index]
            if force:
                self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
                self.player.play_next()
        else:
            # print("current_track_exist False")
            self.player.set_current_track(self.playlist_notifier.value.tracks[next_index])
            self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
            # self.player.play_next()

    def backward(self):
        """Backs to previous track in current playlist, if current track is last,
        will loop to playlists first track """
        progress = self.get_progres()
        status = self.player.get_full_status()

        if progress < 0.05:
            # play prev track
            # search for next available track
            next_index = self.track_notifier.value.index - 1
            if next_index < 0:
                next_index = len(self.playlist_notifier.value.tracks) - 1
            while not self.playlist_notifier.value.tracks[next_index].exist:
                next_index -= 1
                if next_index < 0:
                    next_index = len(self.playlist_notifier.value.tracks) - 1

            # play from start
            self.playlist_notifier.value.tracks[next_index].status = 0
            # load
            if not self.playlist_notifier.value.tracks[next_index].is_loaded:
                self.track_manager.load(self.playlist_notifier.value.tracks[next_index])
            # play
            if status.current_track_exist:
                # if not self.is_playing:
                #    self.player.set_current_track(self.playlist_notifier.value.tracks[next_index])
                # else:
                #    self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
                self.player.set_next_track(self.playlist_notifier.value.tracks[next_index])
                self.next_track = self.playlist_notifier.value.tracks[next_index]
                self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
                self.player.play_next()
            else:
                self.player.set_current_track(self.playlist_notifier.value.tracks[next_index])
                self.track_notifier.value = self.playlist_notifier.value.tracks[next_index]
        else:
            # switch to track start
            self.track_notifier.value.status = 0

            if status.current_track_exist:
                self.player.set_next_track(self.track_notifier.value)
                self.next_track = self.track_notifier.value
                self.track_notifier.value = self.track_notifier.value
                self.player.play_next()
            else:
                self.player.set_current_track(self.track_notifier.value)
                self.track_notifier.value = self.track_notifier.value

    def change(self, new_status):
        # calculate new status from percentage
        self.track_notifier.value.status = int(new_status * self.track_notifier.value.max_status)
        self.player.set_next_track(self.track_notifier.value)
        self.next_track = self.track_notifier.value
        self.track_notifier.value = self.track_notifier.value
        self.track_notifier.notify()
        self.player.play_next()

    def get_progres(self) -> float:
        """Will return current track playback progress, 0 start 1 end"""
        track = self.track_full_status.current_track
        if track is None:
            return 0
        current_status = self.track_full_status.current_track.status / self.track_full_status.current_track.max_status

        if self.track_full_status.next_track is None:
            next_stat = 0
        else:
            next_stat = self.track_full_status.next_track.status / self.track_full_status.next_track.max_status

        return current_status

    async def periodic(self):
        """This periodic function will update currently playing track status"""
        self.track_full_status = await self.player.get_status()
        self.track_status_notifier.value = self.track_full_status.current_track

        if self.track_full_status.in_transition:
            self.track_notifier.value = self.next_track
        # add next track
        if not self.track_full_status.next_track_exist:
            self.forward(force=False)

        await asyncio.sleep(0.5)
