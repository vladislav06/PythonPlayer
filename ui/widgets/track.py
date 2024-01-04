from edifice import component, View, Label, Button

@component
def ShowTrack(self, track):
    track_style = {"width": 170, "align": "left",
                   "margin": 10, "padding": 25, "border": "1px solid black"}
    with View(style=track_style):
        Label(track.name)
        Label('Very cool track')
        #Button(title=track.name)
