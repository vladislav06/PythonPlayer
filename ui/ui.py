from edifice import App, Label, View, component, Window, ScrollView, Button

import ui.playlists as pl
import ui.tracks as tk
import ui.playlist_creation as pl_creation


#Start the program as-is
@component
def MyApp(self, playlists, chosen_playlist):
    with Window(title='PythonPlayer'):  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            with View(layout="column", style={"background-color": "#51EE02"}):
                pl.Playlists(playlists, chosen_playlist)
                Button(title='Add',
                       on_click=pl_creation.Dialogue,
                       style={"width": 50, "height": 25, "align": "left", "margin": 5})
            tk.ShowTracks(playlists[chosen_playlist].tracks)

def launch(playlists):
    App(MyApp(playlists, 0)).start()
