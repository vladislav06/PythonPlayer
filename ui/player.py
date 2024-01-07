from datetime import datetime

from PySide6 import QtCore
from edifice import component, View, Label, use_state, Image, Slider, ButtonView, Icon, use_async
from player.player_controll import PlayerControl
from player.track import Track
from playlists.playlist import Playlist
from util.notifier import Notifier

icon_style = {"width": 10, "padding": 10}

use_slider = False
val = 0


@component
def player(self, player_control: PlayerControl, playlist_notifier: Notifier[Playlist], track_notifier: Notifier[Track],
           track_status_notifier: Notifier[Track]):
    x, x_setter = use_state(0)
    global use_slider

    async def asy():
        global use_slider
        if not use_slider:
            await player_control.periodic()
            x_setter(x + 1)

    use_async(asy, x)

    def change(val):
        global use_slider
        if not use_slider:
            x_setter(0)

    track_notifier.attach(change)
    playlist_notifier.attach(change)
    track_status_notifier.attach(change)

    progress = 0
    length = 0
    if track_status_notifier.value is not None and track_status_notifier.value.is_loaded is True:
        progress = player_control.get_progres() * 1000
        # print(progress)
    if track_notifier.value is not None:
        if track_notifier.value.is_loaded:
            length = track_notifier.value.audio.len_ms

    def on_play_pause(e):
        player_control.play_pause()

    def on_forward(e):
        player_control.forward()

    def on_backward(e):
        player_control.backward()

    def on_change(v):
        global val
        val = v

    def on_click(e):
        global use_slider
        global val
        use_slider = False
        player_control.change(val / 1000)
        x_setter(0)

    def on_mouse_down(e):
        global use_slider
        use_slider = True

    with View(layout="column"):
        Image("./images/Daft_Punk-Discovery.png", style={"align": "center"})
        Label(playlist_notifier.value.name, style={"align": "center"})
        if track_notifier.value is not None:
            Label(track_notifier.value.name, style={"align": "center"})
        else:
            Label("None is currently playing", style={"align": "center"})
        with View(layout="row"):
            with ButtonView(
                    layout="row",
                    style= {"border-radius": 25, "max-width": 25},
                    on_click=on_backward):
                Icon(name="backward", style=icon_style)
            with ButtonView(
                    layout="row",
                    style={ "border-radius": 25, "max-width": 25},
                    on_click=on_play_pause):
                Icon(name="pause" if player_control.is_playing else "play", style=icon_style)
            with ButtonView(
                    layout="row",
                    style={ "border-radius": 25, "max-width": 25},
                    on_click=on_forward):
                Icon(name="forward", style=icon_style)
        with View(layout="row"):

            seconds = int(((length*(progress/1000)) / 1000) % 60)
            minutes = int(((length*(progress/1000)) / (1000 * 60)) % 60)

            Label(f'{minutes:02d}:{seconds:02d}')
            Slider(value=progress,
                   min_value=0,
                   max_value=1000,
                   orientation=QtCore.Qt.Orientation.Horizontal,
                   on_change=on_change,
                   on_click=on_click,
                   on_mouse_down=on_mouse_down)

            seconds = int((length / 1000) % 60)
            minutes = int((length / (1000 * 60)) % 60)

            Label(f'{minutes:02d}:{seconds:02d}')
