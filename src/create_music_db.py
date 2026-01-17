import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# --------------------
# Artist table
# --------------------
class Artist(Base):
    """
    To moja klasa na artyste.

    :param id: artists id
    :param name: artists hobby
    :param origin: you f***ing racist
    """
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origin = Column(String)  # NEW

    songs = relationship("Song", back_populates="artist")


# --------------------
# Song table
# --------------------
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    album = Column(String)   # NEW
    year = Column(Integer)
    language = Column(String)

    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    nostalgic = Column(Integer)
    melancholic = Column(Integer)
    party = Column(Integer)

    artist = relationship("Artist", back_populates="songs")


# --------------------
# DB creation
# --------------------
def main():
    db_folder = os.path.join(os.path.dirname(__file__), "../database")
    os.makedirs(db_folder, exist_ok=True)

    db_path = os.path.join(db_folder, "music.db")
    engine = create_engine(f"sqlite:///{db_path}")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Example artist
    artist = Artist(
        name="Men I Trust",
        origin="Canada"
    )

    # Example song
    song = Song(
        title="Say Can You Hear",
        album="Oncle Jazz",
        year=2019,
        language="English",
        nostalgic=1,
        melancholic=1,
        party=0,
        artist=artist
    )

    session.add(artist)
    session.add(song)
    session.commit()

    print(f"Database created at {db_path}!")


if __name__ == "__main__":
    main()
