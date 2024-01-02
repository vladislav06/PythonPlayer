from multiprocessing import set_start_method

from player.player_interface import *
from playlists.playlist import Playlist
from player.player_manager import PlayerManager
from playlists.playlist_manager import PlaylistManager
from playlists.song_manager import SongManager
from ui import ui


def main():
    playlist_manager: PlaylistManager = PlaylistManager()
    playlist_manager.playlists.append(
        Playlist("aboba1", [Track("adidas1", "some path"), Track("adidas2", "some path")]))
    playlist_manager.playlists.append(
        Playlist("aboba2", [Track("adidas1", "some path"), Track("adidas2", "some path")]))
    ui.launch(playlist_manager.playlists)
'''
    # load playlists
    playlist_manager: PlaylistManager = PlaylistManager()
    playlists = playlist_manager.load_playlists()

    n = []
    for playlist in playlists:
        m = []
        for track in playlist.tracks:
            m.append(str(track))
        n.append(playlist.name + ":" + str(m))

    print("these tracks dont exist:", n)

    # load songs from 1st playlist
    song_manager = SongManager()
    song_manager.load(playlist_manager.playlists[0].tracks[0])
    song_manager.load(playlist_manager.playlists[0].tracks[1])
    # launch player in another thread
    # pipe for bidirectional communication with player
    player_manager = PlayerManager()
    player_manager.launch_player()

    player_manager.set_next_track(song_manager.tracks[1])
    player_manager.play()
    player_manager.set_next_track(song_manager.tracks[0])
    player_manager.play_next()
    while True:
        track = player_manager.get_status()
        if track is not None:
            print(track.status)
            2 + 2;
            '''





if __name__ == "__main__":
    set_start_method('spawn')
    main()
