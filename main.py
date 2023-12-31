from multiprocessing import Process, set_start_method, Pipe

from player.player_interface import *
from playlists.playlist import Playlist
from playlists.playlist_manager import PlaylistManager
from playlists.song_manager import SongManager


def playlist_test():
    playlist_manager = PlaylistManager()
    playlist = Playlist("aa", [Track("name", "path", None)])
    playlist2 = Playlist("bb", [Track("name2", "path2", None)])

    playlist_manager.playlists.append(playlist)
    playlist_manager.playlists.append(playlist2)
    playlist_manager.save_playlists()


def main():
    playlist_test()
    # launch player in another thread
    # pipe for bidirectional communication with player
    pair: (Connection, Connection) = Pipe()
    Process(target=launch_player, args=(pair[0],)).start()
    pipe: Connection = pair[1]
    manager = SongManager()
    manager.load_from_folder("./music/")

    pipe.send(NextMessage(manager.tracks[0]))
    pipe.send(PlayMessage())
    pipe.send(NextMessage(manager.tracks[0]))
    while True:
        if pipe.poll():
            trck: TrackMessage = pipe.recv()
            print(trck.track.status)
        2 + 2;


# ui.launch()


if __name__ == "__main__":
    set_start_method('spawn')
    main()
