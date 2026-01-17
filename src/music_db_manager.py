# src/music_db_manager.py

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from src.create_music_db import Base, Song, Artist

# --------------------
# Engine & Session
# --------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "music.db"

ENGINE = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=ENGINE)


# --------------------
# Public API
# --------------------

def create_music_db():
    """
    Create music.db with all tables.
    """
    os.makedirs(DB_PATH.parent, exist_ok=True)
    Base.metadata.create_all(ENGINE)


def get_music_session():
    """
    Get a new SQLAlchemy session for music.db.
    """
    return SessionLocal()

def rename_artist(old_name: str, new_name: str):
    """
    Rename an artist in music.db (case-insensitive lookup).
    """
    session = get_music_session()

    artist = (
        session.query(Artist)
        .filter(func.lower(Artist.name) == old_name.lower())
        .first()
    )

    if not artist:
        session.close()
        print(f"❌ Artist '{old_name}' not found.")
        return

    if artist.name == new_name:
        session.close()
        print(f"ℹ️ Artist name is already '{new_name}'. No changes made.")
        return

    artist.name = new_name
    session.commit()
    session.close()

    print(f"✏️ Renamed artist '{old_name}' → '{new_name}'.")


def delete_artist_and_songs(artist_name: str):
    """
    Delete an artist and ALL their songs from music.db.
    """
    session = get_music_session()

    artist = session.query(Artist).filter(func.lower(Artist.name) == artist_name).first()
    if not artist:
        session.close()
        print(f"❌ Artist '{artist_name}' not found.")
        return

    # Delete songs first
    deleted_songs = (
        session.query(Song)
        .filter(Song.artist_id == artist.id)
        .delete(synchronize_session=False)
    )

    # Delete artist
    session.delete(artist)
    session.commit()
    session.close()

    print(f"🗑️ Deleted artist '{artist_name}' and {deleted_songs} songs.")

def delete_song(song_title: str, artist_name: str):
    """
    Delete a song by title and artist name (case-insensitive).
    """
    session = get_music_session()

    song = (
        session.query(Song)
        .join(Artist)
        .filter(
            func.lower(Song.title) == song_title.lower(),
            func.lower(Artist.name) == artist_name.lower(),
        )
        .first()
    )

    print("DEBUG", song)

    if not song:
        session.close()
        print(
            f"❌ Song '{song_title}' by '{artist_name}' not found."
        )
        return

    session.delete(song)
    session.commit()
    session.close()

    print(
        f"🗑️ Deleted song '{song_title}' by '{artist_name}'."
    )




