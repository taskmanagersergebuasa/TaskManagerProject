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
    bdd_path = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"
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


# Définir les classes
class Formation(Base):
    __tablename__ = 'formation'
    id_formation = Column(Integer, primary_key=True)
    titre_formation = Column(String)
    filiere = Column(String)
    certifications = relationship('Certification',
                                  secondary=formation_certification,
                                  back_populates='formations')
    sessions = relationship("Session", back_populates="formations")

class Session(Base):
    __tablename__ = 'session'
    id_session = Column(Integer, primary_key=True, autoincrement=True)
    id_formation = Column(Integer, ForeignKey('formation.id_formation')) 
    location = Column(String)
    duree = Column(Integer)
    date_debut = Column(date_type)
    formations = relationship("Formation", back_populates="sessions")

class Certification(Base):
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
    __tablename__ = 'certificateur'
    siret = Column(String, primary_key=True)
    legal_name = Column(String)
    certifications = relationship('Certification',
                                  secondary=certification_certificateur,
                                  back_populates='certificateurs')

class NSF(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(String, primary_key=True)
    nsf_name = Column(String)
    certifications = relationship('Certification',
                              secondary=certification_nsf,
                              back_populates='nsfs')

class Forma(Base):
    __tablename__ = 'forma'
    forma_code = Column(Integer, primary_key=True)
    forma_name = Column(String)
    certifications = relationship('Certification',
                              secondary=certification_forma,
                              back_populates='formas')
    

engine = create_engine(bdd_path)
Base.metadata.create_all(engine)