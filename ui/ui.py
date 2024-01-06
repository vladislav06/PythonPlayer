import signal

from edifice import App, Label, View, component, Window, ScrollView, Button
import playlists as pls

import ui.playlists as pl
import ui.tracks as tk
from playlists.playlist_manager import PlaylistManager
from ui.player import player
from util.notifier import Notifier



# Start the program as-is
@component
def MyApp(self, pl_manager: PlaylistManager, player_control, playlist_notifier, track_notifier,track_status_notifier):
    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            with View(layout="column", style={"background-color": "#51EE02"}):
                pl.Playlists(pl_manager.playlists, playlist_notifier)
                Button(title='Add',
                       on_click=pl_creation.Dialogue,
                       style={"width": 50, "height": 25, "align": "left", "margin": 5})
            player(player_control, playlist_notifier, track_notifier,track_status_notifier)
            tk.ShowTracks(playlist_notifier)


def launch(pl_manager: PlaylistManager, player_control, playlist_notifier, track_notifier,track_status_notifier):
    app = App(MyApp(pl_manager, player_control, playlist_notifier, track_notifier,track_status_notifier))

    with app.start_loop() as loop:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
        loop.run_forever()


