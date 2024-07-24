from pydantic import BaseModel
from typing import List, Optional 
from ..db.session import get_datetype


class Certification(BaseModel):
    type_certif: str
    id_certif: str
    certif_name: str
    niveau: Optional[int]
    etat: Optional[int]
    
    class Config:
        from_attributes = True

class Formation(BaseModel):
    filiere: str
    id_formation: int
    titre_formation: str
    
    certifications: List[Certification]

    class Config:
        from_attributes = True

class Session(BaseModel):
    id_session: int
    id_formation: int
    location: str
    duree: int
    date_debut: get_datetype
    duree: str

    class Config:
        from_attributes = True

class Certificateur(BaseModel):
    siret: str
    legal_name: str

    class Config:
        from_attributes = True

class NSF(BaseModel):
    nfs_code: str
    nsf_nam: str

    class Config:
        from_attributes = True

class Forma(BaseModel):
    forma_code: int
    forma_name: str

    class Config:
        from_attributes = True


