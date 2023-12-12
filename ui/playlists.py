from edifice import component, View, Label, ScrollView

playlists = ["1", "12", "2", "3", "4"]


@component
def Playlists(self):
    with ScrollView(layout="column"):
        for item in playlists:
            Label(item)
