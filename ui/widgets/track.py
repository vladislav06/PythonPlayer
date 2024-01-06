from edifice import component, View, Label, Button
from tinytag import TinyTag

# Styles
track_style = {"height": 25, "margin": 10, "padding": 25,
                   "border": "1px solid black"}
button_style = {"height": 15, "width": 15, "font-size": 8}

# At least on Windows, if a metadata field is empty, tinytag will always yield this string:
empty_data_string = '                              '
# It's used here to check whether certain metadata exists or not.

### TEST FUNCTION TO SEE WHETHER ON_CLICK FOR LABEL WORKS!!
def click():
    print("")

# Function to convert data from track_metadata.duration to minutes for display:
def ConvertToMinutes(seconds):
    # Convert to int
    seconds = int(seconds)
    # Figure out minutes
    minutes = seconds // 60
    # Figure out remaining seconds
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

@component
def ShowTrack(self, track):
    # Get metadata from the track
    #track_metadata = TinyTag.get(track.path)
    with View(layout="row", style=track_style, on_click=click):
        # Display for title-artist
        with View(layout="column", style={"align": "left"}):
            # Show track name, display file name if title is empty in metadata
            '''  
            if (track_metadata.title != empty_data_string):
                Label(track_metadata.title)
            else:
                Label(track.name)
            '''
            Label(track.name)
            # Show artist name, display - if artist is empty in metadata
            '''
            # Show track name, display file name if title is empty in metadata
            if (track_metadata.artist != empty_data_string):
                Label(track_metadata.artist)
            else:
                Label('-')
            '''
            Label('Very cool track')
        # Display for buttons (move up or down)
        with View(layout="column", style={"align": "right"}):
            Button('▲', style=button_style)
            Button('▼', style=button_style)
        # Display for length
        with View(style={"align": "right"}):
            Label('2:28')
            # Label(ConvertToMinutes(track_metadata.duration))