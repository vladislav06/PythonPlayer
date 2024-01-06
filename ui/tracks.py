from edifice import component, View, Label, ScrollView
from player.track import Track
from ui.widgets import track as trWidget
from playlists.playlist import Playlist

#testTracks = ["1", "12", "2", "3", "4"]


@component
def ShowTracks(self, playlistTracks):
    with ScrollView(layout="column", style={"background-color": "#cccfdb", "margin": 10,
                                            "min-width": "250px", "max-width": "250px"}):
        for track in playlistTracks:
            trWidget.ShowTrack(track)
