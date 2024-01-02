from edifice import component, View, Label
from playlists.playlist import Playlist

@component
def ShowPlaylist(self, playlist):
    playlist_label_style = {"width": 170, "margin": 20, "align": "center",
                            "padding": 25, "background-color": "#323f5c"}
    with View(style={"background-color": "#777777"}):
        Label(playlist.name, style=playlist_label_style)
