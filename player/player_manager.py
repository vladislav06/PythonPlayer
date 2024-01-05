from multiprocessing import Process, set_start_method, Pipe

from player.player_interface import *

import time


class PlayerManager:
    connection: Connection

    def launch_player(self):
        pair: (Connection, Connection) = Pipe()
        Process(target=launch_player, args=(pair[0],)).start()
        self.connection = pair[1]

    def play(self):
        self.connection.send(PlayMessage())

    def pause(self):
        self.connection.send(PauseMessage())

    def set_next_track(self, track: Track):
        self.connection.send(NextMessage(track))

    def play_next(self):
        self.connection.send(PlayNextMessage())

    def get_status(self) -> Track | None:
        self.connection.send(TrackMessage())
        while not self.connection.poll():
            time.sleep(0.1)

        trck: TrackMessage = self.connection.recv()
        return trck.track
