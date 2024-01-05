from datetime import datetime

from edifice import component, View, Label, ScrollView, use_state, Image, ProgressBar, ButtonView, Icon

from player.player_controll import PlayerControl
from player.track import Track
from playlists.playlist import Playlist
from util.notifier import Notifier

icon_style = {"width": 10, "padding": 10}


@component
def player(self, player_control: PlayerControl, playlist_notifier: Notifier[Playlist], track_notifier: Notifier[Track]):
    progress, progress_setter = use_state(0.0)

    def on_change(val):
        progress_setter(0.5)

    track_notifier.attach(on_change)
    playlist_notifier.attach(on_change)

    progress = 0
    length = 0
    if track_notifier.value is not None and track_notifier.value.is_loaded is True:
        progress = player_control.get_progres()
        print(progress)
        length = len(track_notifier.value.audio)

    def on_play_pause(e):
        player_control.play_pause()

    def on_forward(e):
        player_control.forward()

    def on_backward(e):
        player_control.backward()

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
                    style={"background-color": "#32a852", "border-radius": 25, "max-width": 25},
                    on_click=on_backward):
                Icon(name="backward", style=icon_style)
            with ButtonView(
                    layout="row",
                    style={"background-color": "#32a852", "border-radius": 25, "max-width": 25},
                    on_click=on_play_pause):
                Icon(name="play", style=icon_style)
            with ButtonView(
                    layout="row",
                    style={"background-color": "#32a852", "border-radius": 25, "max-width": 25},
                    on_click=on_forward):
                Icon(name="forward", style=icon_style)
        with View(layout="row"):
            Label("00:00")
            ProgressBar(value=progress,
                        min_value=0,
                        max_value=1)
            Label(f'{int((length % 1000) / 6000):02d}:{int(length / 1000):02d}')
