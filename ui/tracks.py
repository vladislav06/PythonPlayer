from edifice import component, View, Label, ScrollView, use_state

from player.player_controll import PlayerControl
from player.track import Track
from ui.widgets import track as trWidget
from playlists.playlist import Playlist
from util.notifier import Notifier


# testTracks = ["1", "12", "2", "3", "4"]


@component
def ShowTracks(self,
               view_playlist_notifier: Notifier[Playlist],
               play_playlist_notifier: Notifier[Playlist],
               player_control: PlayerControl):
    x, x_setter = use_state(0)

    def on_change(val):
        x_setter(0)

    view_playlist_notifier.attach(on_change)

    with ScrollView(layout="column",
                    style={"background-color": "#cccfdb",
                           "margin": 10,
                           "min-width": "250px",
                           "max-width": "250px",
                           "align": "top"}):
        for track in view_playlist_notifier.value.tracks:
            trWidget.ShowTrack(track, view_playlist_notifier, play_playlist_notifier, player_control)
