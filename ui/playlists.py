from playlists.playlist import Playlist
from edifice import component, View, Label, ScrollView, Button, use_state

from playlists.playlist_manager import PlaylistManager
from ui.widgets import playlist as plWidget

@component
def Playlists(self, playlists: [Playlist], playlist_notifier,playlist_manager:PlaylistManager):
    x, x_setter = use_state(0)

    def on_change(val):
        x_setter(0)

    playlist_notifier.attach(on_change)

    with ScrollView(layout="column", style={"min-width": "270px", "max-width": "270px", "align": "top"}):
        for playlist in playlists:
            plWidget.playlist(playlist, playlist_notifier, playlist_manager)

