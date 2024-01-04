from datetime import datetime

from edifice import component, View, Label, ScrollView, use_state, Image, ProgressBar, ButtonView, Icon

from player.player_manager import PlayerManager
from player.track import Track
from playlists.playlist import Playlist
from util.notifier import Notifier

icon_style = {"width": 10, "padding": 10}


@component
def player(self, player: PlayerManager, playlist_notifier: Notifier[Playlist], track_notifier: Notifier[Track]):
    progress = 0
    length = 0
    if track_notifier.value is not None:
        progress = track_notifier.value.status / track_notifier.value.max_status
        length = len(track_notifier.value.audio)

    def on_play_pause(e):
        player.play()

    def on_forward(e):
        next_index = track_notifier.value.index + 1
        if next_index >= len(playlist_notifier.value.tracks):
            next_index = 0
        player.set_next_track(playlist_notifier.value.tracks[next_index])
        player.play_next()

    def on_backward(e):
        if progress < 0.2:
            # play prev track
            next_index = track_notifier.value.index - 1
            if next_index < 0:
                next_index = 0
            player.set_next_track(playlist_notifier.value.tracks[next_index])
            player.play_next()
        else:
            # switch to track start
            track_notifier.value.status = 0
            player.set_next_track(track_notifier.value)
            player.play_next()

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
