import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger, CHAR, VARCHAR
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy import func


BaseModel = declarative_base()

class Ksiazki(BaseModel):
    __tablename__   = 'ksiazki'
    ksiazka_id      = Column(BigInteger, primary_key=True)
    nazwa           = Column(VARCHAR(255))
    sciezka         = Column(VARCHAR(255))


class Strony(BaseModel):
    __tablename__   = 'strony'
    strona_id       = Column(BigInteger, primary_key=True)
    ksiazka_id      = Column(BigInteger, ForeignKey('ksiazki.ksiazka_id'))
    numer_strony    = Column(BigInteger)
    sciezka         = Column(VARCHAR(255))
    linie           = relationship('Ksiazki')


class Linie(BaseModel):
    __tablename__   = 'linie'
    linia_id        = Column(BigInteger, primary_key=True)
    strona_id       = Column(BigInteger, ForeignKey('strony.strona_id'))
    numer_linii     = Column(BigInteger)
    strony          = relationship('Strony', foreign_keys=strona_id)
    

class Wyrazy(BaseModel):
    __tablename__   = 'wyrazy'
    wyraz_id        = Column(BigInteger, primary_key=True)
    linia_id        = Column(BigInteger, ForeignKey('linie.linia_id'))
    numer_wyrazu    = Column(BigInteger)
    strony          = relationship('Linie', foreign_keys=linia_id)
    

class Litery(BaseModel):
    __tablename__   = 'litery'
    litera_id       = Column(BigInteger, primary_key=True)
    wyraz_id        = Column(BigInteger, ForeignKey('wyrazy.wyraz_id'))
    numer_litery    = Column(BigInteger)
    sciezka         = Column(VARCHAR(255))
    predykcja       = Column(CHAR(1))
    predykcja_slownik = Column(CHAR(1))
    litery          = relationship('Wyrazy', foreign_keys=wyraz_id)
    

engine = db.create_engine(
    'mysql+mysqlconnector://kacper:5fUwXohpL6rh5xvK@10.8.0.1/baza_wynikowa')


DbSession = sessionmaker(bind=engine)
session = DbSession()


#Return dictionary {page_nr,word_count}
def WordsOnPages(bookName):
    
    pages = session.query(Strony.strona_id,func.count(Wyrazy.wyraz_id)).\
        select_from(Strony,Wyrazy).\
        join(Linie,(Wyrazy.linia_id == Linie.linia_id)).\
        join(Strony,(Strony.strona_id == Linie.strona_id)).\
        group_by(Strony.strona_id).all()


    session.close()
    return pages
     

<<<<<<< HEAD
def LettersOnPage(letter,page):
    
    try:
        letters = session.query(func.count(Litery.litera_id)).\
            join(Wyrazy,(Wyrazy.wyraz_id == Litery.wyraz_id)).\
            join(Linie ,(Linie.linia_id == Wyrazy.linia_id)).\
            join(Strony,(Strony.strona_id == Linie.strona_id)).\
            filter(Litery.predykcja == letter, Strony.numer_strony == page).\
            all()
    except:
        return "Zla liczba stron"
=======
def LettersOnPages(bookName): 
    letters = session.query(Strony.numer_strony,func.count(Litery.litera_id)).\
        join(Wyrazy,(Wyrazy.wyraz_id == Litery.wyraz_id)).\
        join(Linie ,(Linie.linia_id == Wyrazy.linia_id)).\
        join(Strony,(Strony.strona_id == Linie.strona_id)).\
        join(Ksiazki, (Ksiazki.ksiazka_id == Strony.ksiazka_id)).\
        filter(Ksiazki.nazwa == bookName).\
        group_by(Strony.numer_strony).all()
        
>>>>>>> server

    session.close()
    return letters


<<<<<<< HEAD
def LettersInBook(letter,book):
    letters = session.query(func.count(Litery.litera_id)).\
        join(Wyrazy, (Wyrazy.wyraz_id == Litery.wyraz_id)).\
        join(Linie, (Linie.linia_id == Wyrazy.linia_id)).\
        join(Strony, (Strony.strona_id == Linie.strona_id)).\
        join(Ksiazki,(Ksiazki.ksiazka_id == Strony.strona_id)).\
        filter(Litery.predykcja == letter, Ksiazki.nazwa == book).\
        all()
=======
def LettersInBook(book):
    letters = session.query(Litery.predykcja_slownik, func.count(Litery.litera_id)).\
        join(Wyrazy, (Wyrazy.wyraz_id == Litery.wyraz_id)).\
        join(Linie, (Linie.linia_id == Wyrazy.linia_id)).\
        join(Strony, (Strony.strona_id == Linie.strona_id)).\
        join(Ksiazki, (Ksiazki.ksiazka_id == Strony.ksiazka_id)).\
        filter(Ksiazki.nazwa == book).\
        group_by(Litery.predykcja_slownik).\
        order_by(Litery.predykcja_slownik).all()
>>>>>>> server
        
    session.close()
    return letters

<<<<<<< HEAD
=======
#Returns (PageNum,wordLen)
def LenOfWords(book):
    letters = session.query(Strony.numer_strony,func.count(Litery.litera_id)).\
        join(Wyrazy, (Wyrazy.wyraz_id == Litery.wyraz_id)).\
        join(Linie, (Linie.linia_id == Wyrazy.linia_id)).\
        join(Strony, (Strony.strona_id == Linie.strona_id)).\
        join(Ksiazki, (Ksiazki.ksiazka_id == Strony.ksiazka_id)).\
        filter(Ksiazki.nazwa == book).\
        group_by(Litery.wyraz_id,Strony.numer_strony).\
        order_by(Strony.numer_strony).all()

    session.close()
    return letters
>>>>>>> server
