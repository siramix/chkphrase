"""
The models module encapsulates the parameters data inherent in a large database
of phrases.
"""
import hashlib
from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from chkphrase.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    full_name = Column(Unicode(255), unique=True)
    password = Column(String(64))

    def __init__(self, name=None, full_name=None, password=None):
        self.name = name
        self.full_name = full_name
        self.password = hashlib.sha256(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % (self.name)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)


class PreCategory(Base):
    __tablename__ = 'precategories'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<PreCategory %r>' % (self.name)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Genre %r>' % (self.name)


class Difficulty(Base):
    __tablename__ = 'difficulties'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Difficulty %r>' % (self.name)


class Pack(Base):
    __tablename__ = 'packs'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Pack %r>' % (self.name)


class Badword(Base):
    """
    There are five bad words associated with each 'phrase', for buzzowrds a
    phrase is actually just a word.
    """

    __tablename__ = 'badwords'
    id = Column(Integer, primary_key=True)
    phrase_id = Column(Integer, ForeignKey('phrases.id'))
    word = Column(Unicode(255))

    def __init__(self, word=None, phrase_id=None):
        """
        Standard constructor for creating a bad word.
        """
        self.word = word
        self.phrase_id = phrase_id


class Phrase(Base):

    __tablename__ = 'phrases'
    id = Column(Integer, primary_key=True)
    phrase = Column(Unicode(255), unique=True)
    source = Column(Unicode(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    pre_category_id = Column(Integer, ForeignKey('precategories.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    difficulty_id = Column(Integer, ForeignKey('difficulties.id'))
    pack_id = Column(Integer, ForeignKey('packs.id'))
    approved = Column(Integer, default=0)
    buzzworthy = Column(Integer, default=0)

    # -1 do not use
    #  0 in the database
    #  1 has been approved (needs bad words)
    #  2 has bad words (need to be verified)
    #  3 needs further verification
    #  4 ready for a pack
    #  5 in a shippable pack
    stage = Column(Integer, default=0)

    user = relationship('User', backref='users')
    pre_category = relationship('PreCategory', backref='precategories')
    genre = relationship('Genre', backref='genres')
    category = relationship('Category', backref='categories')
    difficulty = relationship('Difficulty', backref='difficulties')
    pack = relationship('Pack', backref='packs')
    badwords = relationship('Badword', backref='badwords')

    def __init__(self, phrase=None, source=None):
        self.phrase = phrase
        self.source = source

    def __repr__(self):
        return '<Phrase %r>' % (self.phrase)
