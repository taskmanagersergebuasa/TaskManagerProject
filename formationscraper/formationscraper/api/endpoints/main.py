from fastapi import APIRouter, HTTPException, Depends
from formationscraper.formationscraper.schemas.main import Formation
from typing import List
from sqlalchemy.orm import Session
from formationscraper.formationscraper.db.session import get_db
from formationscraper.formationscraper.db.models import Formation as DBFormation
from formationscraper.formationscraper.db.models import Session as DBSession
from formationscraper.formationscraper.db.models import Certification as DBCertification
from formationscraper.formationscraper.db.models import Certificateur as DBCertificateur
from formationscraper.formationscraper.db.models import NSF as DBNSF
from formationscraper.formationscraper.db.models import Forma as DBForma


router = APIRouter()

# @router.get(
#     "/formations")
# def get_all_formations(db: Session = Depends(get_db)):
#     """
#     Retourne toutes les formations stockées dans la base de données.
#     """
#     formations = db.query(DBFormation).all()
#     return formations

# récupérer l'ensemble des formations Simplon
@router.get(
    "/formations/", 
    response_model=List[Formation], 
    summary="Obtenir toutes les formations",
    description="Ce point de terminaison renvoie une liste de toutes les formations présentes dans la base de données.",
    tags=["Formations"])

async def get_all_formations(db: Session = Depends(get_db)):
    """
    Retourne toutes les formations stockées dans la base de données.
    """
    formations = db.query(DBFormation).all()
    return formations

# récupérer une formation selon un critère
@router.get("/formations/{formation_id}", response_model=Formation)
async def get_formation(formation_id: int, db: Session = Depends(get_db)):
    formation = db.query(DBFormation).filter(DBFormation.id_formation == formation_id).first()
    if formation is None:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return formation

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