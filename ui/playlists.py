from edifice import component, View, Label, ScrollView
from ui.widgets import playlist as plWidget

#testPlaylists = ["1", "12", "2", "3", "4"]


@component
def Playlists(self, playlists, chosen_playlist):
    playlist_number = 0
    with ScrollView(layout="column"):
        for playlist in playlists:
            #Label(item)
            plWidget.ShowPlaylist(playlist, playlist_number, chosen_playlist)
            playlist_number += 1
