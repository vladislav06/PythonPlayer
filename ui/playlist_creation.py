from edifice import component, View, Label, ScrollView, Button, Window, App, TextInput

# Styles
label_style = {"height": 25, "width": 100, "margin": 10}
textinput_style = {"height": 25, "width": 225, "margin": 10}
button_style = {"height": 25, "width": 75, "margin": 10}

# Dialogue for creation of new playlist
@component
def CreatePlaylist(self):
    with Window(title='PythonPlayer'):  # Top of every App must be a Window
        with View(layout="column"):  # Top Window must have one static child
            with View(layout="row"):
                Label('Playlist Name:', style=label_style)
                TextInput(placeholder_text='Greatest Playlist of all time...', style=textinput_style)
            with View(style={"align": "right"}):
                Button('Confirm', style=button_style)

def Dialogue(e):
    App(CreatePlaylist()).start()

'''
def Test(e):
    print("test")
'''