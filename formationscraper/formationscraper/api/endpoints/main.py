from fastapi import APIRouter, HTTPException, Depends, Query
from formationscraper.formationscraper.schemas.main import Formation as FormationSch, Certification as CertificationSch
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from formationscraper.formationscraper.db.session import get_db
from formationscraper.formationscraper.db.models import Formation as DBFormation
from formationscraper.formationscraper.db.models import Session as DBSession
from formationscraper.formationscraper.db.models import Certification as DBCertification
from formationscraper.formationscraper.db.models import Certificateur as DBCertificateur
from formationscraper.formationscraper.db.models import NSF as DBNSF
from formationscraper.formationscraper.db.models import Forma as DBForma
from formationscraper.formationscraper.db.models import formation_certification, certification_forma


router = APIRouter()

# récupérer l'ensemble des formations Simplon
@router.get("/formations/", 
    response_model=List[FormationSch], 
    summary="Obtenir la liste de toutes les formations certifiantes du site Simplon",
    description="Ce point de terminaison renvoie une liste de toutes les formations présentes dans la base de données.")

async def get_all_formations(db: Session = Depends(get_db)):
    """
    Retourne toutes les formations stockées dans la base de données.
    """
    formations = db.query(DBFormation).all()
    return formations

# récupérer une formation selon un critère (mot clé du titre)
@router.get("/formations/{mot}",
        response_model=List[FormationSch],
        summary="Obtenir la liste des formations Simplon selon un mot clé")

async def get_formation_via_mot_cle(db: Session = Depends(get_db),
    keyword: Optional[str] = Query(None, description="Mot-clé à rechercher dans le titre de la formation")):
    """
    Retourne les formations dont le titre contient le mot-clé fourni.
    """
    query = db.query(DBFormation)
    
    if keyword:
        query = query.filter(DBFormation.titre_formation.ilike(f"%{keyword}%"))
    
    formations = query.all()
    return formations

# récupérer une formation selon le critère de la certification (RS ou RNCP)
@router.get("/formations/certification/{type}/{numero}",
        response_model=List[FormationSch],
        summary="Rechercher une formation Simplon selon sa certification RS ou RNCP")

async def get_formation_par_certif(
    type_certif: str = Query(..., description="type de certification RS ou RNCP"),
    id_certif: str = Query(None, description="numéro de la certification RS ou RNCP"),
    db: Session = Depends(get_db)
):
    """
    Retourne la formation correspondant au RS ou RNCP fourni.
    """

    query = db.query(DBFormation).join(
            formation_certification,
            formation_certification.c.id_formation == DBFormation.id_formation
        ).join(
            DBCertification,
            and_(
                formation_certification.c.id_certif == DBCertification.id_certif,
                formation_certification.c.type_certif == DBCertification.type_certif
            )
        )

    query = query.filter(
        DBCertification.type_certif == type_certif,
        DBCertification.id_certif == id_certif
        )
    
    # # Récupérer les formations associées à la recherche
    formations = query.all()
    
    if not formations:
        raise HTTPException(status_code=404, detail="Certification non trouvée")
    
    return formations

# trouver une formation selon un formacode
@router.get("/formations/formacode/{code}",
        response_model=List[FormationSch],
        summary="Rechercher une formation Simplon selon un formacode")

async def get_formation_par_formacode(
    forma_code: int = Query(..., description="formacode recherché"),
    
    db: Session = Depends(get_db)
):
    """
    Retourne les formations comprenant le formacode fourni.
    """

    query = db.query(DBFormation).join(
            formation_certification,
            formation_certification.c.id_formation == DBFormation.id_formation
        ).join(
            DBCertification,
            and_(
                DBCertification.id_certif == formation_certification.c.id_certif,
                DBCertification.type_certif == formation_certification.c.type_certif
            )
        ).join(
            certification_forma,
            and_(
                certification_forma.c.id_certif == DBCertification.id_certif,
                certification_forma.c.type_certif == DBCertification.type_certif
        )
        ).join(
            DBForma,
            DBForma.forma_code == certification_forma.c.forma_code
        )
        
    query = query.filter(
        DBForma.forma_code == forma_code
        )
    
    # # Récupérer les formations associées à la recherche
    formations = query.all()
    
    if not formations:
        raise HTTPException(status_code=404, detail="Certification non trouvée")
    
    return formations

# trouver une formation selon un formacode (et la région)
@router.get("/formations/formacode_region/{code}/{region}",
        response_model=List[FormationSch],
        summary="Rechercher une formation Simplon selon un formacode et la région")

async def get_formation_par_formacode(
    forma_code: int = Query(..., description="formacode recherché"),
    location: str = Query(..., description="région recherchée"),
    db: Session = Depends(get_db)
):
    
    """
    Retourne les formations comprenant le formacode fourni et dans une région donnée.
    """

    query = db.query(
            DBFormation
        ).join(
            DBSession,
            DBSession.id_formation == DBFormation.id_formation
        ).join(
            formation_certification,
            formation_certification.c.id_formation == DBFormation.id_formation
        ).join(
            DBCertification,
            and_(
                DBCertification.id_certif == formation_certification.c.id_certif,
                DBCertification.type_certif == formation_certification.c.type_certif
            )
        ).join(
            certification_forma,
            and_(
                certification_forma.c.id_certif == DBCertification.id_certif,
                certification_forma.c.type_certif == DBCertification.type_certif
        )
        ).join(
            DBForma,
            DBForma.forma_code == certification_forma.c.forma_code
        )
        
    query = query.filter(
        DBForma.forma_code == forma_code, 
        DBSession.location == location
        )
    
    # # Récupérer les formations associées à la recherche
    formations = query.all()
    
    if not formations:
        raise HTTPException(status_code=404, detail="Certification non trouvée")
    
    return formations


### Comparaison avec une autre table
# @router.get("/compare/")
# async def compare_formation_with_another_table(formation_id: int, db: Session = Depends(get_db)):
#     formation = db.query(DBFormation).filter(DBFormation.id_formation == formation_id).first()
#     if formation is None:
#         raise HTTPException(status_code=404, detail="Formation non trouvée")

#     # Comparaison avec une autre table
#     results = db.query(AnotherModel).filter(
#         AnotherModel.type_certif == formation.type_certif,
#         AnotherModel.id_certif == formation.id_certif
#     ).all()

#     if not results:
#         return {"message": "No matching records found in another table."}

#     return results

# @router.post("/scrape")
# def scrape():
#     process = CrawlerProcess(settings=scrapy_settings)
#     process.crawl(formationspider)
#     process.start()
#     return {"status": "scraping started"}