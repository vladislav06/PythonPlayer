from edifice import App, Label, View, component, Window, ScrollView

import ui.playlists as pl
import ui.tracks as tk


#Start the program as-is
@component
def MyApp(self, playlists, chosen_playlist):
    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            pl.Playlists(playlists, chosen_playlist)
            tk.ShowTracks(playlists[chosen_playlist].tracks)

def launch(playlists):
    App(MyApp(playlists, 0)).start()
