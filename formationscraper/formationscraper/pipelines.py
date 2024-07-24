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
from sqlalchemy import select
import re
import csv

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

    def check_and_insert(session, table, unique_constraints, values):
        """
        Pour éviter les doublons et UNIQUE constraint, vérifie l'existence d'une association dans la table et l'insère si elle n'existe pas.
        créé dans l'objectif de factoriser, mais ne fonctionne pas pour l'instant

        :param session: La session SQLAlchemy
        :param table: L'objet de la table SQLAlchemy
        :param where_conditions: Un dictionnaire des conditions WHERE
        :param values: Un dictionnaire des valeurs à insérer
        """

        # Construire la requête de sélection pour vérifier l'existence
        query = select([table])
        for column, value in unique_constraints.items():
            query = query.where(column == value)

        existing_association = session.execute(query).first()

        # Si l'association n'existe pas, insérer
        if existing_association is None:
            try:
                session.execute(table.insert().values(values))
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise


    def save_formation(self, item):
        formation = Formation(
            titre_formation=item.get("titre_formation"),
            filiere=item.get("filiere"),
            id_formation=item.get("id_formation")
        )
        try:
            self.session.merge(formation)
            self.session.commit()
        except:
            self.session.rollback()

        # Associer la formation avec les certifications
        for id_certif, type_certif in list(set(zip(item.get("id_certif"), item.get("type_certif")))):         
        
        ### complété suite à pb de contrainte UNIQUE (doublons)

            # Vérifier si l'association existe déjà
            existing_association = self.session.execute(
            select(formation_certification)
            .where(formation_certification.c.id_formation == formation.id_formation)
            .where(formation_certification.c.id_certif == str(id_certif))
            .where(formation_certification.c.type_certif == type_certif)
        ).first()

        # Si l'association n'existe pas, l'insérer
            if existing_association is None:
                try:
                    self.session.execute(formation_certification.insert().values(id_formation=formation.id_formation, id_certif=id_certif, type_certif=type_certif))
                    self.session.commit()
                except IntegrityError as e:
                    self.session.rollback()
                    raise

    def save_session(self, item):
        session = Session(
            id_formation=item.get("id_formation"),
            location=item.get("location"),
            date_debut=item.get("date_debut"),
            duree=item.get("duree")
        )
        try:
            self.session.merge(session)
            self.session.commit()
        except:
            self.session.rollback()

    def save_rncp(self, item):
        rncp = Certification(
            id_certif=str(item.get("id_certif")),
            type_certif=item.get("type_certif"),
            certif_name=item.get("titre"),
            niveau=item.get("niveau"),
            etat=item.get("etat")
        )
        try:
            self.session.merge(rncp)
            self.session.commit()
        except:
            self.session.rollback()

    def save_rs(self, item):
        rs = Certification(
            id_certif=str(item.get("id_certif")),
            type_certif=item.get("type_certif"),
            certif_name=item.get("titre"),
            etat=item.get("etat")
        )
        try:
            self.session.merge(rs)
            self.session.commit()
        except:
            self.session.rollback()

    def save_nsf(self, item):
        nsf = NSF(
            nsf_code=item.get("code"),
            nsf_name=item.get("name")
        )
        try:
            self.session.merge(nsf)
            self.session.commit()
        except:
            self.session.rollback()

        existing_association = self.session.execute(
            select(certification_nsf)
            .where(certification_nsf.c.id_certif==str(item.get("id_certif")))
            .where(certification_nsf.c.type_certif==item.get("type_certif"))
            .where(certification_nsf.c.nsf_code==nsf.nsf_code)
        ).first()

        # Si l'association n'existe pas, l'insérer
        if existing_association is None:
            try:
                self.session.execute(certification_nsf.insert().values(id_certif=item.get("id_certif"), type_certif=item.get("type_certif"), nsf_code=nsf.nsf_code))
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                raise


    def save_forma(self, item):
        forma_code = item.get("code")
        forma = Forma(
            forma_code=forma_code,
            forma_name=item.get("name")
        )
        try:
            self.session.merge(forma)
            self.session.commit()
        except:
            self.session.rollback()

        existing_association = self.session.execute(
            select(certification_forma)
            .where(certification_forma.c.id_certif==str(item.get("id_certif")))
            .where(certification_forma.c.type_certif==item.get("type_certif"))
            .where(certification_forma.c.forma_code==forma_code)
        ).first()

        # Si l'association n'existe pas, l'insérer
        if existing_association is None:
            try:
                self.session.execute(certification_forma.insert().values(id_certif=item.get("id_certif"), type_certif=item.get("type_certif"), forma_code=forma_code))
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                raise


    def save_certificateur(self, item):
        certificateur = Certificateur(
            siret=item.get("siret"),
            legal_name=item.get("certificateur_name")
        )
        try:
            self.session.merge(certificateur)
            self.session.commit()
        except:
            self.session.rollback()

        existing_association = self.session.execute(
            select(certification_certificateur)
            .where(certification_certificateur.c.id_certif==str(item.get("id_certif")))
            .where(certification_certificateur.c.type_certif==item.get("type_certif"))
            .where(certification_certificateur.c.siret==certificateur.siret)
        ).first()

        # Si l'association n'existe pas, l'insérer
        if existing_association is None:
            try:
                self.session.execute(certification_certificateur.insert().values(id_certif=item.get("id_certif"), type_certif=item.get("type_certif"), siret=certificateur.siret))
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                raise

        ### appel de la fonction factorisée (qui ne fonctionne pas encore...) 
        # self.check_and_insert(
        #     self.session,
        #     certification_certificateur,
        #     {
        #         certification_certificateur.c.id_certif: item.get("id_certif"),
        #         certification_certificateur.c.type_certif: item.get("type_certif"),
        #         certification_certificateur.c.siret: certificateur.siret
        #     },
        #     {
        #         'id_certif': item.get("id_certif"),
        #         'type_certif': item.get("type_certif"),
        #         'siret': certificateur.siret
        #             }
        #         )





    def close_spider(self, spider):
        self.session.close()





#######


        # # 1) formation_certification
        # 
        # check_and_insert_association(
        #     self.session,
        #     formation_certification,
        #     {
        #         formation_certification.c.id_formation: formation.id_formation,
        #         formation_certification.c.id_certif: id_certif,
        #         formation_certification.c.type_certif: type_certif
        #     },
        #     {
        #         'id_formation': formation.id_formation,
        #         'id_certif': id_certif,
        #         'type_certif': type_certif
        #     }
        # )

        # # 2) certification_nsf
        # check_and_insert_association(
        #     self.session,
        #     certification_nsf,
        #     {
        #         certification_nsf.c.id_certif: item.get("id_certif"),
        #         certification_nsf.c.type_certif: item.get("type_certif"),
        #         certification_nsf.c.nsf_code: nsf.nsf_code
        #     },
        #     {
        #         'id_certif': item.get("id_certif"),
        #         'type_certif': item.get("type_certif"),
        #         'nsf_code': nsf.nsf_code
        #     }
        # )

        # # 3) certification_forma
        # check_and_insert_association(
        #     self.session,
        #     certification_forma,
        #     {
        #         certification_forma.c.id_certif: item.get("id_certif"),
        #         certification_forma.c.type_certif: item.get("type_certif"),
        #         certification_forma.c.forma_code: forma_code
        #     },
        #     {
        #         'id_certif': item.get("id_certif"),
        #         'type_certif': item.get("type_certif"),
        #         'forma_code': forma_code
        #     }
        # )

        # # 4) certification_certificateur
        # check_and_insert_association(
        #     self.session,
        #     certification_certificateur,
        #     {
        #         certification_certificateur.c.id_certif: item.get("id_certif"),
        #         certification_certificateur.c.type_certif: item.get("type_certif"),
        #         certification_certificateur.c.siret: certificateur.siret
        #     },
        #     {
        #         'id_certif': item.get("id_certif"),
        #         'type_certif': item.get("type_certif"),
        #         'siret': certificateur.siret
        #     }
        # )