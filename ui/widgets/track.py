from edifice import component, View, Label


@component
def Track(self, name):
    with View(style={"background-color": "#666666"}):
        Label(name)
