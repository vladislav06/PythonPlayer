from edifice import App, Label, View, component, Window, ScrollView
import playlists as pls

import ui.playlists as pl
import ui.tracks as tk
from playlists.playlist_manager import PlaylistManager
from ui.player import player
from util.notifier import Notifier


# Start the program as-is
@component
def MyApp(self, pl_manager: PlaylistManager, initial_playlist,player_manager):
    playlist_notifier = Notifier()
    playlist_notifier.value = initial_playlist
    track_notifier = Notifier()
    track_notifier.value = None

    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            pl.Playlists(pl_manager.playlists, playlist_notifier)
            player(player_manager,playlist_notifier, track_notifier)
            tk.ShowTracks(playlist_notifier)


def launch(pl_manager: PlaylistManager,player_manager):
    App(MyApp(pl_manager, pl_manager.playlists[0],player_manager)).start()
