from multiprocessing import Process, set_start_method, Queue, Pipe
from multiprocessing.connection import Connection

from player.player_interface import *
from player.song_manager import SongManager


def main():
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
