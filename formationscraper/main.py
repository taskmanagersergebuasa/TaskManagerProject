from fastapi import FastAPI
from .formationscraper.api.endpoints import main_router as formations_router
from .formationscraper.db.session import Base, get_engine, choice_bdd

app = FastAPI()

# Créer les tables de la base de données
database_url = choice_bdd()
engine = get_engine(database_url)
Base.metadata.create_all(bind=engine)

app.include_router(formations_router, prefix="/api")