from edifice import component, View, Label, Button
from tinytag import TinyTag

from player.player_controll import PlayerControl
from playlists.playlist import Playlist
from util.notifier import Notifier

# Styles
track_style = {"height": 25, "margin": 10, "padding": 25,
               "border": "1px solid black"}
button_style = {"height": 15, "width": 15, "font-size": 8}

@component
def ShowTrack(self,
              track,
              view_playlist_notifier: Notifier[Playlist],
              play_playlist_notifier: Notifier[Playlist],
              player_control: PlayerControl):
    def click(e):
        if track.exist:
            # switch to view playlist
            play_playlist_notifier.value = view_playlist_notifier.value
            player_control.play(track)

    def move_up(e):
        playlist = view_playlist_notifier.value
        tmp = playlist.tracks[track.index - 1]
        tmp.index += 1
        track.index -= 1
        playlist.tracks[track.index] = track
        playlist.tracks[track.index + 1] = tmp
        # update
        view_playlist_notifier.value = view_playlist_notifier.value

    def move_down(e):
        playlist = view_playlist_notifier.value
        tmp = playlist.tracks[track.index + 1]
        tmp.index -= 1
        track.index += 1
        playlist.tracks[track.index] = track
        playlist.tracks[track.index - 1] = tmp
        # update
        view_playlist_notifier.value = view_playlist_notifier.value

    if track.exist:
        style = [track_style]
    else:
        style = [track_style, {"background-color": "rgba(10,10,10,100)"}]
    with View(layout="row", style=style, on_click=click, cursor="move"):
        # Display for title-artist
        with View(layout="column", style={"align": "left"}):
            Label(track.title)
            Label(track.artist)
        # Display for buttons (move up or down)
        with View(layout="column", style={"align": "right"}):
            Button('▲', style=button_style, on_click=move_up, enabled=track.index != 0)
            Button('▼', style=button_style, on_click=move_down, enabled=track.index != len(view_playlist_notifier.value.tracks)-1)
        # Display for length
        with View(style={"align": "right"}):
            Label(track.duration)
