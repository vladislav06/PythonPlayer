from edifice import App, component, View, Label, ButtonView, Icon

'''
from playlists.playlist import Playlist
from playlists.playlist_manager import PlaylistManager
from player.player_interface import *
from ui import ui

# Kostil' - playlists in here are declared so that the widget can use them
# SLOMANO NAHUI, ESLI VVESTI - POJAVLAYUTSA DVA (2) LISHNIH PLAYLISTA

playlist_manager: PlaylistManager = PlaylistManager()
playlist_manager.playlists.append(
    Playlist("NEGRI1", [Track("adidas1", "some path"), Track("adidas2", "some path")]))
playlist_manager.playlists.append(
    Playlist("NEGRI2", [Track("nike1", "some path"), Track("nike2", "some path")]))
playlistsTest = playlist_manager.playlists
'''

# Fix - read them from the .JSON file, code copy-pasted below from main.py
# Don't forget to uncomment PlaylistManager inclusions from above
#playlist_manager: PlaylistManager = PlaylistManager()
#playlists = playlist_manager.load_playlists()

# Styles for playlists
playlist_regular_style = {"align": "left", "height": 25,
                        "padding": 25, "font-size": 20}
playlist_chosen_style = {"align": "left", "font-style": "italic", "height": 25,
                        "padding": 25, "text-decoration": "underline", "font-size": 20}
# Styles for icons
icon_style = {"width": 10, "padding": 10}

@component
def ShowPlaylist(self, playlist, playlist_number, chosen_playlist):
    # Set background
    with View(style={"background-color": "#51EE02", "margin": 10}):
        # Set button and mark the chosen playlist
        if (playlist_number == chosen_playlist):
            with ButtonView(
                    layout="row",
                    style={"background-color": "#32a852", "border-radius": 25,
                           "border": "2px solid black"},
            ):
                Icon(name="music", style=icon_style)
                Label(text=playlist.name, style=playlist_chosen_style)
        # For other playlists
        else:
            with ButtonView(
                    layout="row",
                    style={"background-color": "#32a852", "border-radius": 25},
                    #on_click=ChangePlaylist(playlists, playlist_number),
            ):
                Icon(name="music", style=icon_style)
                Label(text=playlist.name, style=playlist_regular_style)

# NE RABOTAET ja daun
#def ChangePlaylist(self, playlists, playlist_number):
#    ui.MyApp(playlists, playlist_number)

