from sqlalchemy import Column, String, Integer, ForeignKey, Table, PrimaryKeyConstraint, ForeignKeyConstraint, Date
from sqlalchemy.orm import relationship
from .session import Base, get_datetype

date_type = get_datetype()
 

# Définir les tables d'association en premier
certification_forma = Table(
    'certification_forma',
    Base.metadata,
    Column('id_certif', String),
    Column('type_certif', String),
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
    Column('id_certif', String),
    Column('type_certif', String),
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
    Column('id_certif', String),
    Column('type_certif', String),
    PrimaryKeyConstraint('id_formation', 'id_certif', 'type_certif'),
    ForeignKeyConstraint(
        ['id_certif', 'type_certif'],
        ['certification.id_certif', 'certification.type_certif']
    )
)

certification_certificateur = Table(
    'certification_certificateur',
    Base.metadata,
    Column('id_certif', String),
    Column('type_certif', String),
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
    sessions = relationship("Session", back_populates="formation")

class Session(Base):
    __tablename__ = 'session'
    id_session = Column(Integer, primary_key=True)
    id_formation = Column(Integer, ForeignKey('formation.id_formation')) 
    location = Column(String)
    duree = Column(Integer)
    date_debut = Column(Date) # date_type
    formation = relationship("Formation", back_populates="sessions")

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
    
