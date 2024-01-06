import asyncio
from multiprocessing import Process, set_start_method, Pipe

from player.player_interface import *

import time


class PlayerManager:
    connection: Connection
    current_status: int = 0
    next_status: int = 0

    def launch_player(self):
        pair: (Connection, Connection) = Pipe()
        self.proc = Process(target=launch_player, args=(pair[0],))
        self.proc.start()
        self.connection = pair[1]

    def play(self):
        self.connection.send(PlayMessage())

    def pause(self):
        self.connection.send(PauseMessage())

    def set_next_track(self, track: Track):
        self.connection.send(SetNextMessage(track))

    def set_current_track(self, track: Track):
        track.status = 0
        self.connection.send(SetCurrentMessage(track))

    def play_next(self):
        self.connection.send(PlayNextMessage())

    async def get_status(self) -> TrackMessage | None:
        self.connection.send(TrackMessage(0, 0, False, False, False))
        while not self.connection.poll():
            await asyncio.sleep(0.2)

        trck: TrackMessage = self.connection.recv()
        return trck

    def get_full_status(self) -> TrackMessage:
        self.connection.send(TrackMessage(0, 0, False, False, False))
        trck: TrackMessage = self.connection.recv()
        return trck
        # return TrackMessage(0,0,False,False)
