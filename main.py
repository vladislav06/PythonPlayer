import ui.ui as ui
from player.player import Player
import time
def main():
    player = Player()
    player.load_from_folder("/home/vm/Documents/PythonPlayer/music/")
    player.start_play()
    print("Asdasda")
    while True:
        time.sleep(1000)
        2+2;



    #ui.launch()



if __name__ == "__main__":
    main()
