from edifice import component, View, Label

@component
def ShowTrack(self, track):
    track_label_style = {"width": 170, "margin": 20, "align": "center",
                            "padding": 25, "background-color": "#225c54"}
    with View(style={"background-color": "#666666"}):
        Label(track.name, style=track_label_style)
