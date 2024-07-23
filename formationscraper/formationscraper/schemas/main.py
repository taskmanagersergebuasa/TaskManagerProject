from pydantic import BaseModel
from ..db.session import get_datetype

class Formation(BaseModel):
    id_formation: int
    titre_formation: str
    filiere: str

    class Config:
        orm_mode = True

class Session(BaseModel):
    id_session: int
    id_formation: int
    location: str
    duree: int
    date_debut: get_datetype
    duree: str

    class Config:
        orm_mode = True

class Certification(BaseModel):
    id_certif: str
    type_certif: str
    certif_name: str
    niveau: str
    etat: str

    class Config:
        orm_mode = True

class Certificateur(BaseModel):
    siret: str
    legal_name: str

    class Config:
        orm_mode = True

class NSF(BaseModel):
    nfs_code: str
    nsf_nam: str

    class Config:
        orm_mode = True

class Forma(BaseModel):
    forma_code: int
    forma_name: str

    class Config:
        orm_mode = True
