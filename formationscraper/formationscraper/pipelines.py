# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dateutil.parser import parse
from dotenv import load_dotenv
from .items import FormationItem, SessionItem, CertifItemBase, RncpItem, RsItem, NsfItem, FormaItem, CertificateurItem
from .db.models import Formation, Session, Certification, NSF, Forma, Certificateur, formation_certification, certification_nsf, certification_forma, certification_certificateur
from .db.session import get_session, choice_bdd
from sqlalchemy.exc import IntegrityError
from collections import deque
import re
import csv
import dateparser



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

        elif isinstance(item, CertifItemBase):
            self.clean_type_certif_fp(item)
            self.clean_id_certif_fp(item)
            self.clean_niveau(item)
            self.clean_etat(item)

        elif isinstance(item, NsfItem):
            self.clean_code(item)
            self.clean_name(item)

        elif isinstance(item,FormaItem):
            self.clean_code(item)
            self.clean_name(item)

        elif isinstance(item,CertificateurItem):
            self.clean_certificateur_name(item)
            self.clean_siret(item)

        elif isinstance(item, SessionItem):
            self.clean_id_formation(item)
            self.clean_location(item)
            self.clean_date_debut(item)
            self.clean_duree(item)

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
            adapter['id_certif'] = str(re.search(r'(RS|RNCP)(\d+)', id_certif).group(2))
        return item


    def clean_id_formation(self, item):
        adapter = ItemAdapter(item)
        id_formation = adapter.get('id_formation')
        if id_formation:
            match1 = re.search(r'(\d+)/?$', id_formation)
            match2 = re.search(r'(\d+)$', id_formation)
            if match1:
                adapter['id_formation'] = int(match1.group(1))
            if match2:
                adapter['id_formation'] = int(match2.group(1))
        return item

    def clean_type_certif(self, item):
        adapter = ItemAdapter(item)
        types_certif = adapter.get('type_certif')
        if types_certif :
            types_certif = [(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(1)) for element in types_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]
            types_certif = [str(type_certif.upper()) for type_certif in types_certif]
            adapter['type_certif'] = types_certif
        return item


    def clean_id_certif(self, item):
        adapter = ItemAdapter(item)
        # ids_certif = adapter.get('id_certif')
        # if ids_certif :
            # ids_certif = [(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(2)) for element in ids_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]
            # adapter['id_certif'] = [str(id_certif) for id_certif in ids_certif]
        id_certif = adapter.get('id_certif')
        if id_certif :
            adapter['id_certif'] = list(set([(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(2)) for element in id_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]))
        return item
        
    def clean_location(self, item):
        adapter = ItemAdapter(item)
        location = adapter.get('location')
        if location :          
            adapter['location'] = location.strip()
        else :
            adapter['location'] = None
        return item

    def clean_date_debut(self, item):
        adapter = ItemAdapter(item)
        debut = adapter.get('date_debut')
        if debut :          
            debut = debut.strip().replace('Début : ','')
            dt = dateparser.parse(debut, date_formats=['%d %B %Y']  ,settings={'PREFER_DAY_OF_MONTH': 'first','DATE_ORDER': 'YMD'})
            adapter['date_debut'] = dt
        else :
            adapter['date_debut'] = None
        return item
    

    def clean_duree(self, item):
        adapter = ItemAdapter(item)
        duree = adapter.get('duree')
        if duree :
            duree = duree.strip()
            match = re.search(r"\d+", duree)
            if match :
                match = int(match.group(0))
                if re.search(r"mois", duree):
                    adapter['duree'] = int(match)*30
                else : 
                    adapter['duree'] = int(match)
            else : 
                adapter['duree'] = None
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
    
    def clean_etat(self, item):
        adapter = ItemAdapter(item)
        etat = adapter.get('etat')
        if etat :
            etat = int(etat.strip() == "Active") 
            adapter['etat'] = etat
        return item


class SQLAlchemyPipeline(object):
    def __init__(self):
        # Charger la configuration de la base de données à partir de l'environnement
        load_dotenv()
        self.bdd_path = choice_bdd()
        
        # Créer le moteur SQLAlchemy et initialiser la session
        self.SessionLocal = get_session(self.bdd_path)
        self.session = self.SessionLocal()
        self.pending_sessions = deque() 

    def process_item(self, item, spider):
        try:
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
            
            self.process_pending_sessions()
            self.session.commit()

        except IntegrityError as e:
            self.session.rollback()
            spider.logger.error(f"Integrity error: {e}")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error processing item: {e}")

            return item
    
    def process_pending_sessions(self):
        for _ in range(len(self.pending_sessions)):
            item = self.pending_sessions.popleft()
            self.save_session(item)

    def save_formation(self, item):
        with self.session.no_autoflush:
            formation = self.session.query(Formation).filter_by(id_formation=item.get("id_formation")).one_or_none()
            if not formation:
                formation = Formation(
                    titre_formation=item.get("titre_formation"),
                    filiere=item.get("filiere"),
                    id_formation=item.get("id_formation")
                )
                self.session.add(formation)
                self.session.flush()

            # Associer la formation avec les certifications
            for id_certif, type_certif in list(set(zip(item.get("id_certif"), item.get("type_certif")))):
                certification = self.session.query(Certification).filter_by(id_certif=id_certif, type_certif=type_certif).first()
                if certification :
                    if certification not in formation.certifications and formation not in formation.certifications:
                        formation.certifications.append(certification)

    def save_session(self, item):
        with self.session.no_autoflush:
            formation = self.session.query(Formation).filter_by(id_formation=item.get("id_formation")).one_or_none()
            if formation:
                sess = self.session.query(Session).filter_by(id_formation=item.get("id_formation"), location=item.get("location"), date_debut=item.get("date_debut")).one_or_none()
                if not sess:
                    sess = Session(
                        id_formation=item.get("id_formation"),
                        location=item.get("location"),
                        date_debut=item.get("date_debut"),
                        duree=item.get("duree")
                    )
                    self.session.add(sess)
                    self.session.flush()

            else:
                # Ajouter la session à la file d'attente si la formation n'existe pas encore
                self.pending_sessions.append(item)
            
    def save_rncp(self, item):
        rncp = self.session.query(Certification).filter_by(id_certif=item.get("id_certif"), type_certif=item.get("type_certif")).first()
        if rncp is None:
            rncp = Certification(
                id_certif=item.get("id_certif"),
                type_certif=item.get("type_certif"),
                certif_name=item.get("titre"),
                niveau=item.get("niveau"),
                etat=item.get("etat")
            )
        self.session.add(rncp)


    def save_rs(self, item):
        rs = self.session.query(Certification).filter_by(id_certif=item.get("id_certif"), type_certif=item.get("type_certif")).first()
        if rs is None:
            rs = Certification(
                id_certif=item.get("id_certif"),
                type_certif=item.get("type_certif"),
                certif_name=item.get("titre"),
                etat=item.get("etat")
            )
        self.session.add(rs)


    def save_nsf(self, item):
        nsf = self.session.query(NSF).filter_by(nsf_code=item.get("code")).first()
        if nsf is None:
            nsf = NSF(
                nsf_code=item.get("code"),
                nsf_name=item.get("name")
            )
        self.session.add(nsf)

        certification = self.session.query(Certification).filter_by(id_certif=item.get("id_certif"), type_certif=item.get("type_certif")).first()
        if certification and nsf not in certification.nsfs:
            certification.nsfs.append(nsf)
        

    def save_forma(self, item):
        forma = self.session.query(Forma).filter_by(forma_code=item.get("code")).first()
        if not forma :
            forma = Forma(
                forma_code=item.get("code"),
                forma_name=item.get("name")
            )
            self.session.add(forma)

        certification = self.session.query(Certification).filter_by(id_certif=item.get("id_certif"), type_certif=item.get("type_certif")).first()
        if certification and forma not in certification.formas:
            certification.formas.append(forma)



    def save_certificateur(self, item):
        certificateur = self.session.query(Certificateur).filter_by(siret=item.get("siret")).first()
        if certificateur is None:
            certificateur = Certificateur(
                siret=item.get("siret"),
                legal_name=item.get("certificateur_name")
            )
        self.session.add(certificateur)
        certification = self.session.query(Certification).filter_by(id_certif=item.get("id_certif"), type_certif=item.get("type_certif")).first()
        if certification and certificateur not in certification.certificateurs:
            certification.certificateurs.append(certificateur)
        

    def close_spider(self, spider):
        self.session.close()

