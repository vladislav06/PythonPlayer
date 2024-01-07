from playlists.playlist import Playlist
from edifice import component, View, Label, ScrollView, Button, use_state
from ui.widgets import playlist as plWidget


# testPlaylists = ["1", "12", "2", "3", "4"]


@component
def Playlists(self, playlists: [Playlist], playlist_notifier):
    x, x_setter = use_state(0)

    def on_change(val):
        x_setter(0)

    playlist_notifier.attach(on_change)

    with ScrollView(layout="column", style={"min-width": "250px", "max-width": "250px", "align": "top"}):
        for playlist in playlists:
            if playlist == playlist_notifier.value:
                plWidget.selected_playlist(playlist, playlist_notifier)
            else:
                plWidget.playlist(playlist, playlist_notifier)
