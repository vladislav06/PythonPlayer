from PySide6.QtWidgets import QLabel
from edifice import App, component, View, Label, ButtonView, Icon, Button, use_state, alert

from playlists.playlist_manager import PlaylistManager

#Styles
text_regular_style = {"align": "left", "height": 25,
                      "padding": 25, "font-size": 20, "max-width": "200px"}
text_chosen_style = {"align": "left", "font-style": "italic", "height": 25,
                     "padding": 25, "text-decoration": "underline", "font-size": 20, "max-width": "200px"}
icon_style = {"width": 10, "padding": 10}
button_style = {"max-width": "50px", "height": 75, "margin": 10, "align": "right", "font-size": 8,
                "border-top-right-radius": 15, "border-bottom-right-radius": 15}


@component
def playlist(self, plst, playlist_notifier, playlist_manager: PlaylistManager):
    x, x_setter = use_state(0)
    selected = plst == playlist_notifier.value

    def on_change(val):
        try:
            x_setter(0)
        except Exception as e:
            pass

    def on_click(e):
        playlist_notifier.value = plst

    playlist_notifier.attach(on_change)

    def on_delete(e):
        # ask user
        answer = alert(message="Are you sure?", choices=["Yes", "No"])
        if answer ==1:
            return
        playlist_manager.playlists.remove(plst)
        playlist_notifier.detach(on_change)
        playlist_notifier.value = None
        playlist_manager.save_playlists()


    # Set background
    with View(style={"margin": 10}):
        with View(style={"border": "2px solid black"} if selected else {"border": "1px solid black"}):
            # Set button and mark the chosen playlist
            with View(layout="row"):
                with ButtonView(
                        layout="row",
                        style={"background-color": "", "border-top-left-radius": 15, "border-bottom-left-radius": 15},
                        on_click=on_click,
                ):
                    Icon(name="music", style=icon_style)
                    Label(text=plst.name, style=text_chosen_style if selected else text_regular_style)

                Button(
                    title="X",
                    style=button_style,
                    on_click=on_delete)
