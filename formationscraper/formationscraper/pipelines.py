# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import FormationItem, SessionItem, CertifItemBase
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
        self.certif_headers = ['type_certif', 'id_certif', 'titre', 'etat', 'niveau', 'nsf_code', 'nsf_name', 'formacode', 'formaname', 'certificateur']

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
            self.clean_nsf_code(item)
            self.clean_nsf_name(item)
            self.clean_formacode(item)
            self.clean_formaname(item)

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
        type_certif = adapter.get('type_certif')
        if type_certif :
            adapter['type_certif'] = list(set([(re.search(r'recherche/(rs|rncp)/(\d+)', element).group(1))
        for element in type_certif if element and re.search(r'recherche/(rs|rncp)/(\d+)', element)]))
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
            adapter['location'] = [element.strip() for element in location][1::2]
        return item

    def clean_date_debut(self, item):
        adapter = ItemAdapter(item)
        debut = adapter.get('date_debut')
        if debut :          
            adapter['date_debut'] = [element.strip().replace('Début : ','') for element in debut][1::2]
        return item

    def clean_duree(self, item):
        adapter = ItemAdapter(item)
        duree = adapter.get('duree')
        if duree :          
            adapter['duree'] = [element.strip() for element in duree][1::2]
        return item

    def clean_niveau(self, item):
        adapter = ItemAdapter(item)
        niveau = adapter.get('niveau')
        if niveau :
            adapter['niveau'] = int(re.search(r'(\d)', niveau).group(1))
        return item

    def clean_nsf_code(self, item):
        adapter = ItemAdapter(item)
        code = adapter.get('nsf_code')
        if code :          
            adapter['nsf_code'] = [element.strip().split(' :')[0] for element in code][1::2]
        return item

    def clean_nsf_name(self, item):
        adapter = ItemAdapter(item)
        name = adapter.get('nsf_name')
        if name :          
            adapter['nsf_name'] = [element.strip() for element in name if element.strip()]
        return item

    def clean_formacode(self, item):
        adapter = ItemAdapter(item)
        code = adapter.get('formacode')
        if code :          
            adapter['formacode'] = [element.strip() for element in code][1::2]
        return item

    def clean_formaname(self, item):
        adapter = ItemAdapter(item)
        name = adapter.get('formaname')
        if name :          
            adapter['formaname'] = [element.strip() for element in name][1::2]
        return item



    