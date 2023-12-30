import time
from multiprocessing import Queue

from player.player import Player
from player.track import Track


class Message:
    ID: int = 0


class PlayMessage(Message):
    ID: int = 1


class PauseMessage(Message):
    ID: int = 2


class NextMessage(Message):
    ID: int = 3
    track: Track = None

    def __init__(self, track: Track):
        self.track = track


def launch_player(queue: Queue):
    player = Player()
    player.init_player()
    # player.load_from_folder("./music/")
    # player.start_play()

    while True:
        message = queue.get()
        if message.ID == PlayMessage.ID:
            player.play()
        elif message.ID == PauseMessage.ID:
            player.pause()
        elif message.ID == NextMessage.ID:
            player.set_next(message.track)
        time.sleep(0.1)
