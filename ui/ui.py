from edifice import App, Label, View, component, Window, ScrollView

import ui.playlists as pl
import ui.tracks as tk



@component
def MyApp(self, playlists):
    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            pl.Playlists(playlists)
            tk.ShowTracks(playlists[0].tracks)




def launch(playlists):
    App(MyApp(playlists)).start()
