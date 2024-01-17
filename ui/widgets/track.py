from edifice import component, View, Label, Button, use_state, alert

from player.player_controll import PlayerControl
from playlists.playlist import Playlist
from playlists.playlist_manager import PlaylistManager
from util.notifier import Notifier

# Styles
track_style = {"height": 25, "margin": 10, "padding": 25,
               "border": "1px solid black"}
button_style = {"height": 30, "width": 14, "font-size": 8}


@component
def ShowTrack(self,
              track,
              view_playlist_notifier: Notifier[Playlist],
              play_playlist_notifier: Notifier[Playlist],
              player_control: PlayerControl,
              playlist_manager: PlaylistManager):

    x, x_setter = use_state(0)

    def on_change(val):
        try:
            x_setter(0)
        except Exception as e:
            pass

    player_control.track_notifier.attach(on_change)
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
        # save
        playlist_manager.save_playlists()
        # update
        view_playlist_notifier.value = view_playlist_notifier.value

    def move_down(e):
        playlist = view_playlist_notifier.value
        tmp = playlist.tracks[track.index + 1]
        tmp.index -= 1
        track.index += 1
        playlist.tracks[track.index] = track
        playlist.tracks[track.index - 1] = tmp
        # save
        playlist_manager.save_playlists()
        # update
        view_playlist_notifier.value = view_playlist_notifier.value

    def delete(e):
        # ask user
        answer = alert(message="Are you sure?", choices=["Yes", "No"])
        if answer == 1:
            return
        view_playlist_notifier.value.tracks.remove(track)
        playlist_manager.save_playlists()
        view_playlist_notifier.value = view_playlist_notifier.value

    if track.exist:
        style = track_style
    else:
        style = [track_style, {"background-color": "rgba(10,10,10,100)"}]


    with View(layout="row",
              style=[style,{"border": "2px solid black"} if player_control.track_notifier.value == track else {}],
              on_click=click, cursor="move"):
        # Display for title-artist
        with View(layout="column", style={"align": "left"}):
            Label(track.title)
            if track.artist is not None:
                Label(track.artist)

        View(layout="row")
        View(layout="row")
        View(layout="row")
        View(layout="row")


        # Display for length
        with View(style={"align": "right"}):
            Label(track.duration)

        # Display for buttons (move up or down)
        with View(layout="column", style={"align": "right"}):
            Button('▲', style=button_style, on_click=move_up, enabled=track.index != 0)
            Button('▼', style=button_style, on_click=move_down,
                   enabled=track.index != len(view_playlist_notifier.value.tracks) - 1)
        with View(layout="column", style={"align": "right", "height":"60"}):
            View(layout="column")
            Button('X', style=[button_style, {"align": "right","height": 15}], on_click=delete)
