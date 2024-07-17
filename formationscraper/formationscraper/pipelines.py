# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import FormationItem, SessionItem, CertifItemBase, RncpItem, RsItem
import re
import csv


import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from scrapy.exceptions import DropItem
from .models import Formation, Session, Certification, NSF, Forma, engine
from dotenv import load_dotenv


class CsvPipeline:
    def open_spider(self, spider):
        # Ouverture des fichiers en mode écriture
        self.file_formation = open('formations.csv', 'w', newline='', encoding='utf-8')
        self.file_session = open('sessions.csv', 'w', newline='', encoding='utf-8')
        self.file_certif = open('certifs.csv', 'w', newline='', encoding='utf-8')

        # Définition des en-têtes
        self.formation_headers = ['filiere', 'titre_formation', 'id_formation', 'id_certif']
        self.session_headers = ['location', 'date_debut', 'id_formation']
        self.certif_headers = ['id_certif', 'titre', 'etat','niveau', 'nsf_code', 'nsf_name', 'formacode', 'formaname']

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
        self.clean_niveau_fp_rncp(item)  # nettoyage du niveau RNCP de francecompetences
        self.clean_nsf_rncp(item)
        self.clean_nsf_rs(item)
        # self.clean_formacode(item)  # nettoyage des formacodes
        return item
    

    def clean_niveau_fp_rncp(self, item):
        adapter = ItemAdapter(item)
        niveau_fp_rncp = adapter.get('niveau_fp_rncp')
        if niveau_fp_rncp :
            cleaned_niveau_fp_rncp = niveau_fp_rncp.replace('\n', '')
            adapter['niveau_fp_rncp'] = re.search(r'\s+(Niveau\s\d)\s+', cleaned_niveau_fp_rncp).group(1)
        return item


    def clean_nsf_get(self,item,certif):
        adapter = ItemAdapter(item)
        nsf_certif = adapter.get(certif)
        if nsf_certif:
            adapter[certif] = self.clean_nsf(nsf_certif)

    def clean_nsf_rs(self,item):
        return self.clean_nsf_get(item,'nsf_fp_rs')

    def clean_nsf_rncp(self,item):
        return self.clean_nsf_get(item,'nsf_fp_rncp')

    def clean_nsf(self, nsf_list):
        if isinstance(nsf_list, list): 
            liste_nsf = nsf_list.split(",")
            print(liste_nsf)
            for nsf in liste_nsf :
                nsf_list_cleaned = (re.search(r'\s+(\d+\w)', nsf).group(1)).join(",")
                print(nsf_list_cleaned)
                return nsf_list_cleaned
        else :
            return re.search(r'\s+(\d+\w)', nsf_list).group(1)
    
    def clean_formacode(self, item):
        pass



load_dotenv()

class SQLAlchemyPipeline(object):
    def __init__(self):
        self.Session = sessionmaker(bind=engine, autoflush=False)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            if isinstance(item, FormationItem):
                self._process_formation_item(item, session)
            elif isinstance(item, SessionItem):
                self._process_session_item(item, session)
            elif isinstance(item, RncpItem):
                self._process_rncp_item(item, session)
            elif isinstance(item, RsItem):
                self._process_rs_item(item, session)

            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Error saving item due to integrity error: {e}")
            raise DropItem(f"Error saving item due to integrity error: {e}")
        except Exception as e:
            session.rollback()
            print(f"Error processing item: {e}")
            raise DropItem(f"Error processing item: {e}")
        finally:
            session.close()

        return item

    def _process_formation_item(self, item, session):
        formation = session.query(Formation).filter_by(
            id_formation=item['id_formation']
        ).first()

        if not formation:
            formation = Formation(
                id_formation=item['id_formation'],
                titre_formation=item['titre_formation'],
                filiere=item['filiere']
            )
            session.add(formation)

        # Add or update certification association
        if 'id_certif' in item:
            certification = session.query(Certification).filter_by(id_certif=item['id_certif']).first()
            if certification and certification not in formation.certifications:
                formation.certifications.append(certification)
        session.add(formation)

    def _process_session_item(self, item, session):
        session_obj = Session(
            id_formation=item['id_formation'],
            location=item['location'],
            date_debut=item['date_debut']
        )
        session.add(session_obj)

    def _process_rncp_item(self, item, session):
        certification = session.query(Certification).filter_by(id_certif=item['id_certif']).first()

        if not certification:
            certification = Certification(
                id_certif=item['id_certif'],
                certif_name=item['titre'],
                etat=item['etat'],
                niveau=item['niveau']
            )
            session.add(certification)

        nsf = session.query(NSF).filter_by(nsf_code=item['nsf_code']).first()
        if not nsf:
            nsf = NSF(
                nsf_code=item['nsf_code'],
                nsf_name=item['nsf_name']
            )
            session.add(nsf)

        forma = session.query(Forma).filter_by(forma_code=item['formacode']).first()
        if not forma:
            forma = Forma(
                forma_code=item['formacode'],
                forma_name=item['formaname']
            )
            session.add(forma)

        certification.nsfs.append(nsf)
        certification.formas.append(forma)
        session.add(certification)

    def _process_rs_item(self, item, session):
        certification = session.query(Certification).filter_by(id_certif=item['id_certif']).first()

        if not certification:
            certification = Certification(
                id_certif=item['id_certif'],
                certif_name=item['titre'],
                etat=item['etat']
            )
            session.add(certification)

        nsf = session.query(NSF).filter_by(nsf_code=item['nsf_code']).first()
        if not nsf:
            nsf = NSF(
                nsf_code=item['nsf_code'],
                nsf_name=item['nsf_name']
            )
            session.add(nsf)

        forma = session.query(Forma).filter_by(forma_code=item['formacode']).first()
        if not forma:
            forma = Forma(
                forma_code=item['formacode'],
                forma_name=item['formaname']
            )
            session.add(forma)

        certification.nsfs.append(nsf)
        certification.formas.append(forma)
        session.add(certification)
