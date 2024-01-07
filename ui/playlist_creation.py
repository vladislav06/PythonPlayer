import asyncio
import signal

from edifice import component, View, Label, ScrollView, Button, Window, App, TextInput
from multiprocessing import Process, set_start_method, Pipe
from multiprocessing.connection import Connection

# Styles
label_style = {"height": 25, "width": 100, "margin": 10}
textinput_style = {"height": 25, "width": 225, "margin": 10}
button_style = {"height": 25, "width": 75, "margin": 10}

name = ""

loop = 0


# Dialogue for creation of new playlist
@component
def create_playlist(self, connection: Connection):
    def on_confirm(e):
        # exit
        global name
        connection.send(name)
        loop.stop()

    def on_change(s):
        global name
        name = s

    with Window(title='PythonPlayer'):  # Top of every App must be a Window
        with View(layout="column"):  # Top Window must have one static child
            with View(layout="row"):
                Label('Playlist Name:', style=label_style)
                TextInput(placeholder_text='Greatest Playlist of all time...', style=textinput_style,
                          on_change=on_change)
            with View(style={"align": "right"}):
                Button('Confirm', style=button_style, on_click=on_confirm)


def start(connection):
    app = App(create_playlist(connection))
    global loop
    with app.start_loop() as lop:
        loop = lop
        #lop.add_signal_handler(signal.SIGINT, lop.stop)
        lop.run_forever()


async def dialogue():
    pair: (Connection, Connection) = Pipe()
    proc = Process(target=start, args=(pair[0],))
    proc.start()
    connection = pair[1]
    while not connection.poll():
        await asyncio.sleep(0.2)
    print("received")
    return connection.recv()


'''
def Test(e):
    print("test")
'''
