from multiprocessing import set_start_method, Pipe

from edifice import alert
from pynput.keyboard import Listener, Key

from player.player_controll import PlayerControl
from player.player_interface import *
from playlists.playlist import Playlist
from player.player_manager import PlayerManager
from playlists.playlist_manager import PlaylistManager
from playlists.track_manager import TrackManager
from ui import ui
from util.notifier import Notifier


# Function for handling key presses



player_control = None


def main():
    global player_control

    # load playlists
    playlist_manager: PlaylistManager = PlaylistManager()
    playlists = playlist_manager.load_playlists()

    n = []
    for playlist in playlists:
        m = []
        for track in playlist.tracks:
            m.append(str(track))
        n.append(playlist.name + ":" + str(m))

    if len(n) == 0:
        n = None
    # load songs from 1st playlist
    song_manager = TrackManager()
    # song_manager.load(playlist_manager.playlists[0].tracks[0])
    # song_manager.load(playlist_manager.playlists[0].tracks[1])

    #song_manager.load(playlist_manager.playlists[0].tracks[0])

    player_manager = PlayerManager()
    player_manager.launch_player()

    # ui
    play_playlist_notifier = Notifier()
    play_playlist_notifier.value = Playlist("",[])
    view_playlist_notifier = Notifier()
    view_playlist_notifier.value = Playlist("",[])
    track_notifier = Notifier()
    track_status_notifier = Notifier()
    #track_notifier.value = song_manager.tracks[0]
    pair: (Connection, Connection) = Pipe()

    player_control = PlayerControl(player_manager, song_manager, play_playlist_notifier, track_notifier,
                                   track_status_notifier, pair[1])



    def on_prs(key):
        pair[0].send(key)

    # button listener
    listener_thread = Listener(on_press=on_prs, on_release=None)
    listener_thread.start()

    ui.launch(playlist_manager,
              player_control,
              view_playlist_notifier,
              play_playlist_notifier,
              track_notifier,
              track_status_notifier,
              n)

import logging
logger = logging.getLogger("Edifice")
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        set_start_method('spawn')
        main()
    except KeyboardInterrupt as inter:
        pass
    player_control.stop()
