from edifice import App, Label, View, component, Window, ScrollView
import playlists as pls

import ui.playlists as pl
import ui.tracks as tk
from playlists.playlist_manager import PlaylistManager
from util.notifier import Notifier


# Start the program as-is
@component
def MyApp(self, pl_manager: PlaylistManager, initial_playlist):
    playlist_notifier = Notifier()
    playlist_notifier.value = initial_playlist

    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            pl.Playlists(pl_manager.playlists, playlist_notifier)
            tk.ShowTracks(playlist_notifier)


def launch(pl_manager: PlaylistManager):
    App(MyApp(pl_manager, pl_manager.playlists[0])).start()
