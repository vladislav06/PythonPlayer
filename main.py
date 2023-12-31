from multiprocessing import Process, set_start_method, Queue

from player.player_interface import *
from player.song_manager import SongManager


def main():
    # launch player in another thread
    # queue for communication with player
    queue: Queue[Message] = Queue()
    Process(target=launch_player, args=(queue,)).start()

    manager = SongManager()
    manager.load_from_folder("./music/")

    queue.put(NextMessage(manager.tracks[0]))
    queue.put(PlayMessage())
    queue.put(NextMessage(manager.tracks[0]))
    while True:
        2 + 2;


# ui.launch()


if __name__ == "__main__":
    set_start_method('spawn')
    main()
