import asyncio
from multiprocessing import set_start_method

from player.player_controll import PlayerControl
from player.player_interface import *
from playlists.playlist import Playlist
from player.player_manager import PlayerManager
from playlists.playlist_manager import PlaylistManager
from playlists.song_manager import SongManager
from ui import ui
from util.notifier import Notifier


def main():
    # load playlists
    playlist_manager: PlaylistManager = PlaylistManager()
    playlists = playlist_manager.load_playlists()

    # TODO: show notification to user about lost tracks
    n = []
    for playlist in playlists:
        m = []
        for track in playlist.tracks:
            m.append(str(track))
        n.append(playlist.name + ":" + str(m))

    print("these tracks dont exist:", n)
    ###
    # load songs from 1st playlist
    song_manager = SongManager()
    song_manager.load(playlist_manager.playlists[0].tracks[0])
    song_manager.load(playlist_manager.playlists[0].tracks[1])

    player_manager = PlayerManager()
    player_manager.launch_player()

    playlist_notifier = Notifier()
    playlist_notifier.value = playlist_manager.playlists[0]
    track_notifier = Notifier()

    player_control: PlayerControl = PlayerControl(player_manager, song_manager, playlist_notifier, track_notifier)
    player_control.init()

    ui.launch(playlist_manager, player_control, playlist_notifier, track_notifier)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    set_start_method('spawn')
    main()
