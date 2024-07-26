from sqlalchemy import create_engine, Column, String, Integer, Float, Date, ForeignKey, Table, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

if bool(int(os.getenv("IS_POSTGRES"))):
    username = os.getenv("DB_USERNAME")
    hostname = os.getenv("DB_HOSTNAME")
    port = os.getenv("DB_PORT")
    database_name = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    bdd_path = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}"
else:
    bdd_path = 'sqlite:///database.db'

engine = create_engine(bdd_path)
Base = declarative_base()
if engine.dialect.name == 'sqlite':
    date_type = String
elif engine.dialect.name == 'postgresql':
    date_type = Date
else:
    raise ValueError(f"SGBD non pris en charge : {engine.dialect.name}")

certification_forma = Table(
    'certification_forma',
    Base.metadata,
    Column('id_certif'),
    Column('type_certif'),
    Column('forma_code', ForeignKey('forma.forma_code')),
    PrimaryKeyConstraint('forma_code', 'id_certif', 'type_certif'),
    ForeignKeyConstraint(
        ['id_certif', 'type_certif'],
        ['certification.id_certif', 'certification.type_certif']
    )
)

certification_nsf = Table(
    'certification_nsf',
    Base.metadata,
    Column('id_certif'),
    Column('type_certif'),
    Column('nsf_code', ForeignKey('nsf.nsf_code')),
    PrimaryKeyConstraint('nsf_code', 'id_certif', 'type_certif'),
    ForeignKeyConstraint(
        ['id_certif', 'type_certif'],
        ['certification.id_certif', 'certification.type_certif']
    )
)

formation_certification = Table(
    'formation_certification',
    Base.metadata,
    Column('id_formation', ForeignKey('formation.id_formation')),
    Column('id_certif'),
    Column('type_certif'),
    PrimaryKeyConstraint('id_formation', 'id_certif', 'type_certif'),
    ForeignKeyConstraint(
        ['id_certif', 'type_certif'],
        ['certification.id_certif', 'certification.type_certif']
    )
)

certification_certificateur = Table(
    'certification_certificateur',
    Base.metadata,
    Column('id_certif'),
    Column('type_certif'),
    Column('siret', ForeignKey('certificateur.siret')),
    PrimaryKeyConstraint('id_certif', 'type_certif', 'siret'),
    ForeignKeyConstraint(
        ['id_certif', 'type_certif'],
        ['certification.id_certif', 'certification.type_certif']
    )
)

class Formation(Base):
    """
    Classe représentant une formation.

    Attributes:
        id_formation (int): L'identifiant unique de la formation.
        titre_formation (str): Le titre de la formation.
        filiere (str): La filière de la formation.
        certifications (list of Certification): Les certifications associées à la formation.
        sessions (list of Session): Les sessions associées à la formation.
    """
    __tablename__ = 'formation'
    id_formation = Column(Integer, primary_key=True)
    titre_formation = Column(String)
    filiere = Column(String)
    certifications = relationship('Certification',
                                  secondary=formation_certification,
                                  back_populates='formations')
    sessions = relationship("Session", back_populates="formation")

class Session(Base):
    """
    Classe représentant une session de formation.

    Attributes:
        id_session (int): L'identifiant unique de la session.
        id_formation (int): L'identifiant de la formation associée.
        location (str): Le lieu de la session.
        duree (int): La durée de la session en jours.
        date_debut (str/date): La date de début de la session (String pour SQLite, Date pour PostgreSQL).
        formation (Formation): La formation associée à cette session.
    """
    __tablename__ = 'session'
    id_session = Column(Integer, primary_key=True)
    id_formation = Column(Integer, ForeignKey('formation.id_formation')) 
    location = Column(String)
    duree = Column(Integer)
    date_debut = Column(date_type)
    formation = relationship("Formation", back_populates="sessions")

class Certification(Base):
    """
    Classe représentant une certification.

    Attributes:
        id_certif (str): L'identifiant unique de la certification.
        type_certif (str): Le type de certification.
        certif_name (str): Le nom de la certification.
        niveau (int): Le niveau de la certification.
        etat (int): L'état de la certification (actif, inactif, etc.).
        certificateurs (list of Certificateur): Les certificateurs associés à la certification.
        formations (list of Formation): Les formations associées à la certification.
        nsfs (list of NSF): Les catégories NSF associées à la certification.
        formas (list of Forma): Les catégories Forma associées à la certification.
    """
    __tablename__ = 'certification'
    id_certif = Column(String, primary_key=True)
    type_certif = Column(String, primary_key=True)
    certif_name = Column(String)
    niveau = Column(Integer)
    etat = Column(Integer)
    certificateurs = relationship('Certificateur',
                                  secondary=certification_certificateur,
                                  back_populates='certifications')
    formations = relationship('Formation',
                              secondary=formation_certification,
                              back_populates='certifications')
    nsfs = relationship('NSF',
                        secondary=certification_nsf,
                        back_populates='certifications')
    formas = relationship('Forma',
                          secondary=certification_forma,
                          back_populates='certifications')

class Certificateur(Base):
    """
    Classe représentant un certificateur.

    Attributes:
        siret (str): Le numéro SIRET du certificateur.
        legal_name (str): Le nom légal du certificateur.
        certifications (list of Certification): Les certifications associées au certificateur.
    """
    __tablename__ = 'certificateur'
    siret = Column(String, primary_key=True)
    legal_name = Column(String)
    certifications = relationship('Certification',
                                  secondary=certification_certificateur,
                                  back_populates='certificateurs')

class NSF(Base):
    """
    Classe représentant une catégorie NSF (Nomenclature des Spécialités de Formation).

    Attributes:
        nsf_code (str): Le code unique de la catégorie NSF.
        nsf_name (str): Le nom de la catégorie NSF.
        certifications (list of Certification): Les certifications associées à la catégorie NSF.
    """
    __tablename__ = 'nsf'
    nsf_code = Column(String, primary_key=True)
    nsf_name = Column(String)
    certifications = relationship('Certification',
                              secondary=certification_nsf,
                              back_populates='nsfs')

class Forma(Base):
    """
    Classe représentant une catégorie Forma.

    Attributes:
        forma_code (int): Le code unique de la catégorie Forma.
        forma_name (str): Le nom de la catégorie Forma.
        certifications (list of Certification): Les certifications associées à la catégorie Forma.
    """
    __tablename__ = 'forma'
    forma_code = Column(Integer, primary_key=True)
    forma_name = Column(String)
    certifications = relationship('Certification',
                              secondary=certification_forma,
                              back_populates='formas')

engine = create_engine(bdd_path)
Base.metadata.create_all(engine)
