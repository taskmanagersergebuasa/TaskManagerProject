# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import FormationItem, SessionItem, CertifItemBase, RncpItem, RsItem, NsfItem, FormaItem, CertificateurItem
import re
import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from scrapy.exceptions import DropItem
from .models import Formation, Session, Certification, NSF, Forma, Certificateur, engine
from dateutil.parser import parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

class CsvPipeline:
    def open_spider(self, spider):
        # Ouverture des fichiers en mode écriture
        self.file_formation = open('formations_clean.csv', 'w', newline='', encoding='utf-8')
        self.file_session = open('sessions_clean.csv', 'w', newline='', encoding='utf-8')
        self.file_certif = open('certifs_clean.csv', 'w', newline='', encoding='utf-8')

        # Définition des en-têtes
        self.formation_headers = ['filiere', 'titre_formation', 'id_formation', 'type_certif', 'id_certif']
        self.session_headers = ['id_formation', 'location', 'date_debut', 'duree']
        self.certif_headers = ['type_certif', 'id_certif', 'titre', 'etat', 'niveau', 'nsf_code', 'nsf_name', 'formacode', 'formaname', 'certificateur', 'siret']

        # Création des objets writer pour chaque fichier avec les en-têtes correspondantes
        self.formation_writer = csv.DictWriter(self.file_formation, fieldnames=self.formation_headers)
        self.session_writer = csv.DictWriter(self.file_session, fieldnames=self.session_headers)
        self.certif_writer = csv.DictWriter(self.file_certif, fieldnames=self.certif_headers)

        # Écriture des en-têtes dans chaque fichier
        self.formation_writer.writeheader()
        self.session_writer.writeheader()
        self.certif_writer.writeheader()

    def close_spider(self, spider):
        # Fermeture des fichiers
        self.file_formation.close()
        self.file_session.close()
        self.file_certif.close()

    def process_item(self, item, spider):
        if isinstance(item, FormationItem):
            # Écriture des données de l'item formation dans le fichier formations.csv
            self.formation_writer.writerow(item)
        elif isinstance(item, SessionItem):
            # Écriture des données de l'item session dans le fichier sessions.csv
            self.session_writer.writerow(item)
        elif isinstance(item, CertifItemBase):
            self.certif_writer.writerow(item)


class FormationscraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, FormationItem):
            self.clean_id_formation(item)
            self.clean_type_certif(item)
            self.clean_id_certif(item)

        elif isinstance(item, SessionItem):
            self.clean_id_formation(item)
            self.clean_location(item)
            self.clean_date_debut(item)
            self.clean_duree(item)
            
        elif isinstance(item, CertifItemBase):
            self.clean_type_certif_fp(item)
            self.clean_id_certif_fp(item)
            self.clean_niveau(item)

        elif isinstance(item, NsfItem):
            self.clean_code(item)
            self.clean_name(item)

        elif isinstance(item,FormaItem):
            self.clean_code(item)
            self.clean_name(item)

        elif isinstance(item,CertificateurItem):
            self.clean_certificateur_name(item)
            self.clean_siret(item)

        return item
    


    def clean_certificateur_name(self,item):
        adapter = ItemAdapter(item)
        certificateur_name = adapter.get('certificateur_name')
        if certificateur_name :
            adapter['certificateur_name'] = certificateur_name.strip()
        return item
    
    def clean_siret(self,item):
        adapter = ItemAdapter(item)
        siret = adapter.get('siret')
        if siret :
            adapter['siret'] = siret.strip()
        return item
    
    def clean_type_certif_fp(self, item):
        adapter = ItemAdapter(item)
        type_certif = adapter.get('type_certif')
        if type_certif:
            adapter['type_certif'] = re.search(r'(RS|RNCP)(\d+)', type_certif).group(1)
        return item
    
    def clean_id_certif_fp(self, item):
        adapter = ItemAdapter(item)
        id_certif = adapter.get('id_certif')
        if id_certif:           
            adapter['id_certif'] = int(re.search(r'(RS|RNCP)(\d+)', id_certif).group(2))
        return item


    def clean_id_formation(self, item):
        adapter = ItemAdapter(item)
        id_formation = adapter.get('id_formation')
        if id_formation:
            match = re.search(r'(\d+)(?=/|$)', id_formation)
            if match:
                adapter['id_formation'] = int(match.group(1))
            else:
                adapter['id_formation'] = None
        else:
            adapter['id_formation'] = None 
        return item

    def clean_type_certif(self, item):
        adapter = ItemAdapter(item)
        types_certif = adapter.get('type_certif')
        if types_certif :
            types_certif = list(set(types_certif))
            types_certif = [(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(1))
        for element in types_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]
            types_certif = [type_certif.upper() for type_certif in types_certif]
            adapter['type_certif'] = types_certif
        return item


    def clean_id_certif(self, item):
        adapter = ItemAdapter(item)
        id_certif = adapter.get('id_certif')
        adapter['id_certif'] = list(set([int(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(2))
        for element in id_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]))
        return item
        

    def clean_location(self, item):
        adapter = ItemAdapter(item)
        location = adapter.get('location')
        if location :          
            adapter['location'] = location.strip()
        return item

    def clean_date_debut(self, item):
        adapter = ItemAdapter(item)
        debut = adapter.get('date_debut')
        if debut :          
            debut = debut.strip().replace('Début : ','')
            dt = parse(debut, fuzzy_with_tokens=True)[0]
            adapter['date_debut'] = dt.strftime("%m/%Y")
        return item
    

    def clean_duree(self, item):
        adapter = ItemAdapter(item)
        duree = adapter.get('duree')
        if duree :          
            duree = duree.strip()
            match = re.search(r"\d+", duree)
            if match :
                adapter['duree'] = match.group(0)
        return item

    def clean_niveau(self, item):
        adapter = ItemAdapter(item)
        niveau = adapter.get('niveau')
        if niveau :
            adapter['niveau'] = int(re.search(r'(\d)', niveau).group(1))
        return item


    def clean_code(self, item):
        adapter = ItemAdapter(item)
        code = adapter.get('code')
        if code :
            adapter['code'] = code.replace(':','').strip()
        return item


    def clean_name(self, item):
        adapter = ItemAdapter(item)
        name = adapter.get('name')
        if name :          
            adapter['name'] = name.strip()
        return item




load_dotenv()

class SQLAlchemyPipeline(object):
    def __init__(self):
        load_dotenv()
        if bool(int(os.getenv("IS_POSTGRES"))):
            username = os.getenv("DB_USERNAME")
            hostname = os.getenv("DB_HOSTNAME")
            port = os.getenv("DB_PORT")
            database_name = os.getenv("DB_NAME")
            password = os.getenv("DB_PASSWORD")
            self.bdd_path = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"
        else:
            self.bdd_path = 'sqlite:///database.db'
        
        self.engine = create_engine(self.bdd_path)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        if isinstance(item, FormationItem):
            self.save_formation(item)
        elif isinstance(item, SessionItem):
            self.save_session(item)
        elif isinstance(item, RncpItem):
            self.save_rncp(item)
        elif isinstance(item, RsItem):
            self.save_rs(item)
        elif isinstance(item, NsfItem):
            self.save_nsf(item)
        elif isinstance(item, FormaItem):
            self.save_forma(item)
        elif isinstance(item, CertificateurItem):
            self.save_certificateur(item)
        return item

    def save_formation(self, item):
        formation = Formation(
            titre_formation=item.get("titre_formation"),
            filiere=item.get("filiere"),
            id_formation=item.get("id_formation")
        )

        # for certif_id,type_certif in zip(item['id_certif'],item['type_certif']):
        #     certification = self.session.query(Certification).filter_by(certif_id=certif_id, type_certif=type_certif).first()
        #     if certification:
        #         formation.certifications.append(certification)
        #     else:
        #         new_certification = Certification(id=certif_id)#, titre="Unknown Title")
        #         formation.certifications.append(new_certification)
        #         self.session.add(new_certification)

        self.session.merge(formation)
        self.session.commit()

    def save_session(self, item):
        session = Session(
            id_formation=item.get("id_formation"),
            location=item.get("location"),
            date_debut=item.get("date_debut"),
            duree=item.get("duree")
        )
        self.session.merge(session)
        self.session.commit()

    def save_rncp(self, item):
        rncp = Certification(
            id_certif=item.get("id_certif"),
            type_certif=item.get("type_certif"),
            certif_name=item.get("titre"),
            niveau=item.get("niveau"),
            etat=item.get("etat")
        )
        self.session.merge(rncp)
        self.session.commit()

    def save_rs(self, item):
        rs = Certification(
            id_certif=item.get("id_certif"),
            type_certif=item.get("type_certif"),
            certif_name=item.get("titre"),
            etat=item.get("etat")
        )
        self.session.merge(rs)
        self.session.commit()

    def save_nsf(self, item):
        nsf = NSF(
            nsf_code=item.get("code"),
            nsf_name=item.get("name")
        )
        self.session.merge(nsf)
        self.session.commit()

    def save_forma(self, item):
        forma = Forma(
            forma_code=item.get("code"),
            forma_name=item.get("name")
        )
        self.session.merge(forma)
        self.session.commit()

    def save_certificateur(self, item):
        certificateur = Certificateur(
            siret=item.get("siret"),
            legal_name=item.get("certificateur_name")
        )
        self.session.merge(certificateur)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()

