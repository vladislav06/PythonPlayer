import time
from multiprocessing.connection import Connection

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


class PlayNextMessage(Message):
    ID: int = 4


class TrackMessage(Message):
    ID: int = 5
    track: Track = None

    def __init__(self, track: Track = None):
        self.track = track


def launch_player(pipe: Connection):
    player = Player()
    player.init_player()

    while True:
        try:
            if pipe.poll():
                message = pipe.recv()
                if message.ID == PlayMessage.ID:
                    player.play()
                elif message.ID == PauseMessage.ID:
                    player.pause()
                elif message.ID == NextMessage.ID:
                    player.set_next(message.track)
                elif message.ID == PlayNextMessage.ID:
                    player.play_next()
                elif message.ID == TrackMessage.ID:
                    if player.current_track is not None:
                        pipe.send(TrackMessage(player.current_track.copy()))
                    else:
                        pipe.send(TrackMessage())

            time.sleep(0.1)
        except Exception as e:
            print(e)
