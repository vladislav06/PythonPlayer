import time
import traceback
from multiprocessing.connection import Connection
from threading import Thread

from player.player import Player
from player.track import Track


class Message:
    ID: int = 0


class PlayMessage(Message):
    ID: int = 1


class PauseMessage(Message):
    ID: int = 2


class SetCurrentMessage(Message):
    ID: int = 6
    track: Track = None

    def __init__(self, track: Track):
        self.track = track


class SetNextMessage(Message):
    ID: int = 3
    track: Track = None

    def __init__(self, track: Track):
        self.track = track


class PlayNextMessage(Message):
    ID: int = 4


class TrackMessage(Message):
    ID: int = 5
    current_track: Track = None
    next_track: Track = None
    current_status: int = 0
    next_status: int = 0
    current_track_exist: bool = False
    next_track_exist: bool = False
    in_transition: bool = False

    def __init__(self, current_status,
                 next_status,
                 current_track_exist,
                 next_track_exist,
                 in_transition,
                 current_track: Track = None,
                 next_track: Track = None):
        self.current_track = current_track
        self.next_track = next_track
        self.current_status = current_status
        self.next_status = next_status
        self.current_track_exist = current_track_exist
        self.next_track_exist = next_track_exist
        self.in_transition = in_transition


def loop(pipe: Connection, player):
    while True:
        try:
            # print("check")
            if pipe.poll():
                msg = pipe.recv()
                # print("got:", type(msg))
                if msg.ID == PlayMessage.ID:
                    player.play()
                elif msg.ID == PauseMessage.ID:
                    player.pause()
                elif msg.ID == SetCurrentMessage.ID:
                    player.set_current(msg.track)
                elif msg.ID == SetNextMessage.ID:
                    player.set_next(msg.track)
                elif msg.ID == PlayNextMessage.ID:
                    player.play_next()
                elif msg.ID == TrackMessage.ID:
                    pipe.send(TrackMessage(player.current_track.status if player.current_track is not None else 0,
                                           player.next_track.status if player.next_track is not None else 0,
                                           player.current_track is not None,
                                           player.next_track is not None,
                                           player.in_transition,
                                           player.current_track.copy() if player.current_track is not None else None,
                                           player.next_track.copy() if player.next_track is not None else None))

            time.sleep(0.1)
        except Exception as e:
            print(e)
            traceback.print_exc()


player = Player()
pipe = 0


def launch_player(pip: Connection):
    player.init_player()
    pipe = pip
    t = Thread(target=loop, args=[pipe, player])
    t.start()
