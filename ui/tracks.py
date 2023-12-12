from edifice import component, View, Label, ScrollView

tracks = ["1", "12", "2", "3", "4"]


@component
def Tracks(self):
    with ScrollView(layout="column"):
        for item in tracks:
            Label(item)
