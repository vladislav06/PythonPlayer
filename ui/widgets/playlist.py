from edifice import component, View, Label


@component
def Playlist(self, name):
    with View(style={"background-color": "#777777"}):
        Label(name)
