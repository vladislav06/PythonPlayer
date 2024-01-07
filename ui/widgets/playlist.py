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

# Styles for playlists

playlist_regular_style = {"align": "left", "height": 25,
                        "padding": 25, "font-size": 20}
playlist_chosen_style = {"align": "left", "font-style": "italic", "height": 25,
                        "padding": 25, "text-decoration": "underline", "font-size": 20}
# Styles for icons
icon_style = {"width": 10, "padding": 10}


@component
def playlist(self, plst, playlist_notifier):
    def on_click(e):
        print("click on playlist:", plst.name)
        playlist_notifier.value = plst

    # Set background
    with View(style={"background-color": "#51EE02", "margin": 10}):
        with ButtonView(
                layout="row",
                style={"background-color": "#32a852", "border-radius": 25},
                on_click=on_click):
            Icon(name="music", style=icon_style)
            Label(text=plst.name, style=playlist_regular_style)


@component
def selected_playlist(self, plst, playlist_notifier):
    def click(e):
        print("click on selected_playlist:", plst.name)
        playlist_notifier.value = plst

    # Set background
    with View(style={"background-color": "#51EE02", "margin": 10}):
        # Set button and mark the chosen playlist
        with ButtonView(
                layout="row",
                style={"background-color": "#32a852", "border-radius": 25,
                       "border": "2px solid black"},
                on_click=click,
        ):
            Icon(name="music", style=icon_style)
            Label(text=plst.name, style=playlist_chosen_style)
