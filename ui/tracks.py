from edifice import component, View, Label, ScrollView, use_state
from player.track import Track
from ui.widgets import track as trWidget
from playlists.playlist import Playlist
from util.notifier import Notifier


# testTracks = ["1", "12", "2", "3", "4"]


@component
def ShowTracks(self, playlist_notifier: Notifier[Playlist]):
    x, x_setter = use_state(0)

    def on_change(val):
        x_setter(0)

    playlist_notifier.attach(on_change)

    with ScrollView(layout="column", style={"background-color": "#cccfdb", "margin": 10}):
        for track in playlist_notifier.value.tracks:
            trWidget.ShowTrack(track)
