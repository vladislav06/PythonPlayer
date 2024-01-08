import os
import pathlib

from edifice import component, View, Label, ScrollView, use_state, Button, file_dialog

from player.player_controll import PlayerControl
from player.track import Track
from playlists.playlist_manager import PlaylistManager
from playlists.track_manager import TrackManager
from ui.widgets import track as trWidget
from playlists.playlist import Playlist
from util.notifier import Notifier


@component
def ShowTracks(self,
               playlist_manager: PlaylistManager,
               view_playlist_notifier: Notifier[Playlist],
               play_playlist_notifier: Notifier[Playlist],
               player_control: PlayerControl):
    x, x_setter = use_state(0)

    def on_change(val):
        x_setter(0)

    def add_track(e):
        if view_playlist_notifier.value is None:
            return
        path = file_dialog(
            caption="Select track",
            file_filter="*.mp3 *.wav *.flac")
        if path is None:
            return

        track = Track(path.split(os.sep)[-1], str(pathlib.Path(path).parent.resolve()))
        track.exist = True
        TrackManager.load_metadata(track)

        view_playlist_notifier.value.add(track)
        view_playlist_notifier.value = view_playlist_notifier.value
        playlist_manager.save_playlists()
        x_setter(0)

    view_playlist_notifier.attach(on_change)
    with View(style={
        "min-width": "250px",
        "max-width": "250px",
        "align": "top"}):
        with ScrollView(layout="column", style={"margin": 10}):
            if view_playlist_notifier.value is not None:
                for track in view_playlist_notifier.value.tracks:
                    trWidget.ShowTrack(track, view_playlist_notifier, play_playlist_notifier, player_control,
                                       playlist_manager)
        Button(title='Add',
               on_click=add_track,
               style={"width": 50, "height": 25, "align": "left", "margin": 5})
