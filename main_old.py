from src.scan_and_import import import_music_from_folder
from src.read_music_db import read_music_db
from src.get_songs import get_songs_by_language
from src.get_songs import get_songs_by_tag
from src.create_yt_playlist import create_yt_playlist
from src.music_db_manager import create_music_db, delete_artist_and_songs
from src.tag_db_manager import create_tag_db, delete_tag

def mainLoop():
    running = True
    while (running):
        print("What do you want to do:")
        userInput = input()

        if (userInput == "exit"):
            running = False

        if (userInput == "getSongs"):
            getSongs()

        if (userInput == "importSongs"):
            importSongs()

def getSongs():
    songs = []
    running = True
    while (running):
        print("What songs do you want to get?")
        userInput = input()
        if (userInput == "back"):
            running = False
            mainLoop()
        if (userInput == "language"):
            print("What language?")
            userInput = input()
            songs = get_songs_by_language(userInput)
            running = False
            printAndExit(songs)
        if (userInput == "tags"):
            print("What tags?")
            userInput = input()
            songs = get_songs_by_tag(userInput)
            running = False
            printAndExit(songs)


def importSongs():
    import_music_from_folder("/home/shianman/Music", mode = "update")

def printAndExit(songs: list):
    print(songs)
    exit


def main():

    mainLoop()





    # import_music_from_folder("/home/shianman/Music", mode = "update")
    # read_music_db()
    # songs = get_songs_by_language("Polish")
    # print(songs)
    # create_yt_playlist(songs)


if __name__ == "__main__":
    main()
