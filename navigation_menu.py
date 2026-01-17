import questionary

from src.create_yt_playlist import create_yt_playlist
from src.get_songs import get_songs
from src.get_songs import get_songs_by_language
from src.get_songs import get_songs_by_tag, get_all_artists, get_songs_by_artist
from src.import_from_txt import load_songs_from_txt
from src.music_db_manager import create_music_db, rename_artist, delete_artist_and_songs, delete_song
from src.scan_and_import import import_music_from_folder
from src.tag_db_manager import create_tag_db, delete_tag


def main_loop():
    action_map = {
        "Get artists": get_artists,
        "Get songs": get_songs_navigation,
        "Import songs": import_songs,
        "Database manager": database_manager,
    }

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Get artists",
                "Get songs",
                "Create playlist",
                "Import songs",
                "Database manager",
                "Exit"
            ]
        ).ask()

        # match choice:
        #     case "Get artists":
        #         get_artists()
        #     case "Get songs":
        #         get_songs_navigation()
        #     case "Create playlist":
        #         print("Choose the name of the playlsit:")
        #         playlist_name = input()
        #         songs = load_songs_from_txt("../songs.txt")
        #         print(songs)
        #         create_yt_playlist(songs, playlist_name)
        #     case "Import songs":
        #         import_songs()
        #     case "Database manager":
        #         database_manager()
        #     case _:
        #         break

        if choice == "Create playlist":
            print("Choose the name of the playlsit:")
            playlist_name = input()
            songs = load_songs_from_txt("../songs.txt")
            print(songs)
            create_yt_playlist(songs, playlist_name)
        elif choice == "Exit":
            break
        else:
            action_map[choice]()

        # if choice == "Get artists":
        #     get_artists()
        # elif choice == "Get songs":
        #     get_songs_navigation()
        # elif choice == "Create playlist":
        #     print("Choose the name of the playlsit:")
        #     playlist_name = input()
        #     songs = load_songs_from_txt("../songs.txt")
        #     print(songs)
        #     create_yt_playlist(songs, playlist_name)
        # elif choice == "Import songs":
        #     import_songs()
        # elif choice == "Database manager":
        #     database_manager()
        # elif choice == "Exit":
        #     break


def get_artists():
    print("Warning - As for now this code lists only all artists")
    artists = get_all_artists()
    for artist in artists:
        print(f"- {artist.name}")


def get_songs_navigation():
    choice = questionary.select(
        "Get songs by:",
        choices=[
            "EXPERIMENTAL",
            "Artist",
            "Language",
            "Tags",
            "Back"
        ]
    ).ask()

    if choice == "EXPERIMENTAL":
        items = get_songs("Artist", "Aurora")
        for item in items:
            print(f"- {item.title}")

    elif choice == "Artist":
        artist = questionary.text("Artist:").ask()
        songs = get_songs_by_artist(artist)
        for song in songs:
            print(f"- {song.artist.name} - {song.title}")

    elif choice == "Language":
        lang = questionary.text("Language:").ask()
        songs = get_songs_by_language(lang)
        for song in songs:
            print(f"- {song.artist.name} - {song.title}")

    elif choice == "Tags":
        tags = questionary.text("Tags:").ask()
        songs = get_songs_by_tag(tags)
        print(songs)


def import_songs():
    import_music_from_folder("/home/shianman/Music", mode="update")


def database_manager():
    choice = questionary.select(
        "Database Manager:",
        choices=[
            "Music.db",
            "Tag.db",
            "Back"
        ]
    ).ask()

    if choice == "Music.db":
        database_manager_music_db()

    elif choice == "Tag.db":
        database_manager_tag_db()


def database_manager_music_db():
    choice = questionary.select(
        "Database Manager: Music.db:",
        choices=[
            "Create a new database",
            "Rename an artist",
            "Remove an artist",
            "Remove a song",
            "Back"
        ]
    ).ask()

    if choice == "Create a new database":
        create_music_db()

    elif choice == "Rename an artist":
        oldname = questionary.text("Rename which artist:").ask()
        newname = questionary.text("To what name:").ask()
        rename_artist(oldname, newname)

    elif choice == "Remove an artist":
        artist = questionary.text("Artist:").ask()
        delete_artist_and_songs(artist)

    elif choice == "Remove a song":
        artist = questionary.text("Song's artist:").ask()
        song = questionary.text("Song name:").ask()
        delete_song(song, artist)


def database_manager_tag_db():
    choice = questionary.select(
        "Database Manager: Tag.db:",
        choices=[
            "Create a new database",
            "Remove tag",
            "Back"
        ]
    ).ask()

    if choice == "Create a new database":
        create_tag_db()

    elif choice == "Remove tag":
        tag = questionary.text("Tag:").ask()
        print(type(tag))  # debug
        delete_tag(tag)


def main():
    print("This code can't be run directly")


if __name__ == "__main__":
    main()
