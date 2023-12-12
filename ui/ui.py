from edifice import App, Label, View, component, Window, ScrollView

import ui.playlists as pl
import ui.tracks as tk



@component
def MyApp(self):
    with Window():  # Top of every App must be a Window
        with View(layout="row"):  # Top Window must have one static child
            pl.Playlists()
            tk.Tracks()




def launch():
    App(MyApp()).start()
