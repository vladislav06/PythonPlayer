from edifice import App, component, View, Label, ButtonView, Icon, Button

'''
from playlists.playlist import Playlist
from playlists.playlist_manager import PlaylistManager
from player.player_interface import *
from ui import ui
'''

# Styles
playlist_regular_style = {"align": "left", "height": 25,
                        "padding": 25, "font-size": 20}
playlist_chosen_style = {"align": "left", "font-style": "italic", "height": 25,
                        "padding": 25, "text-decoration": "underline", "font-size": 20}
icon_style = {"width": 10, "padding": 10}
button_style = {"width": 15, "height": 15, "margin": 10, "align": "right", "font-size": 8}

@component
def playlist(self, plst, playlist_notifier):
    def on_click(e):
        print("click on playlist:", plst.name)
        playlist_notifier.value = plst

    # Set background
    with View(style={"background-color": "#51EE02", "margin": 10}):
        with View(layout="row"):
            with ButtonView(
                    layout="row",
                    style={"background-color": "#32a852", "border-radius": 25},
                    on_click=on_click):
                Icon(name="music", style=icon_style)
                Label(text=plst.name, style=playlist_regular_style)
            Button(title="X", style=button_style)


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
            Button(title="X", style=button_style)
