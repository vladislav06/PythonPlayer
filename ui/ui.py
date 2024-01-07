from edifice import App,  View, component, Window,  Button, use_async, use_state, alert


import ui.playlists as pl
import ui.tracks as tk
from playlists.playlist import Playlist
from playlists.playlist_manager import PlaylistManager
from ui.player import player
from ui.playlist_creation import dialogue
create_playlist = False

n = None
# Start the program as-is
@component
def MyApp(self, pl_manager: PlaylistManager, player_control, view_playlist_notifier, play_playlist_notifier,
          track_notifier, track_status_notifier):
    x, x_state = use_state(0)
    global create_playlist
    global n
    # show warning about lost tracks
    if n is not None:
        alert(message="These tracks do not exist" + str(n))
        n = None

    async def fetcher():
        print("3")
        name = await dialogue()
        pl_manager.add(Playlist(name, []))
        pl_manager.save_playlists()
        view_playlist_notifier.value = view_playlist_notifier.value
        x_state(x+1)

    def new_playlist(e):
        print("1")
        global create_playlist
        create_playlist = True
        x_state(x+1)

    if create_playlist:
        print("2")
        use_async(fetcher, x)
        print("2.1")
        create_playlist = False

    with Window(title='PythonPlayer'):  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            with View(layout="column", style={"min-width": "270px", "max-width": "270px"}):
                pl.Playlists(pl_manager.playlists, view_playlist_notifier, pl_manager)
                Button(title='Add',
                       on_click=new_playlist,
                       style={"width": 50, "height": 25, "align": "left", "margin": 5})
            player(player_control, play_playlist_notifier, track_notifier, track_status_notifier)
            tk.ShowTracks(pl_manager, view_playlist_notifier, play_playlist_notifier, player_control)


def launch(pl_manager: PlaylistManager, player_control, view_playlist_notifier, play_playlist_notifier, track_notifier,
           track_status_notifier, nn):
    global n
    n=nn
    app = App(MyApp(pl_manager, player_control, view_playlist_notifier, play_playlist_notifier, track_notifier,
                    track_status_notifier))
    with app.start_loop() as loop:
        #loop.add_signal_handler(signal.SIGINT, loop.stop)
        loop.run_forever()
