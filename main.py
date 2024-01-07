from multiprocessing import set_start_method

from player.player_controll import PlayerControl
from player.player_interface import *
from playlists.playlist import Playlist
from player.player_manager import PlayerManager
from playlists.playlist_manager import PlaylistManager
from playlists.song_manager import TrackManager
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
    song_manager = TrackManager()
    # song_manager.load(playlist_manager.playlists[0].tracks[0])
    # song_manager.load(playlist_manager.playlists[0].tracks[1])

    for track in playlist_manager.playlists[0].tracks:
        song_manager.load(track)

    player_manager = PlayerManager()
    player_manager.launch_player()
    # ui
    play_playlist_notifier = Notifier()
    play_playlist_notifier.value = playlist_manager.playlists[0]
    view_playlist_notifier = Notifier()
    view_playlist_notifier.value = playlist_manager.playlists[0]
    track_notifier = Notifier()
    track_status_notifier = Notifier()
    track_notifier.value = song_manager.tracks[0]

    player_control: PlayerControl = PlayerControl(player_manager, song_manager, play_playlist_notifier, track_notifier,
                                                  track_status_notifier)

    ui.launch(playlist_manager, player_control, view_playlist_notifier, play_playlist_notifier, track_notifier,
              track_status_notifier)


if __name__ == "__main__":
    try:
        set_start_method('spawn')
        main()
    except KeyboardInterrupt as inter:
        pass

