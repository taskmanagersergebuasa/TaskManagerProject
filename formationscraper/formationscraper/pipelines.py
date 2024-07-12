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


    # def open_spider(self, spider):
    #     # Ouverture du fichier en mode écriture
    #     self.file = open('formation_test.csv', 'w', newline='', encoding='utf-8')
        
    #     # Définition des en-têtes
    #     # fieldnames = ['filiere', 'titre_formation', 'id_certif_fp_rnpc', 'titre_certif_fp_rncp', 'etat_fp_rncp', 'niveau_fp_rncp', 'nsf_code_fp_rncp', 'nsf_name_fp_rncp', 'formacode_code_fp_rncp', 'formacode_name_fp_rncp', 'id_certif_fp_rs', 'titre_certif_fp_rs', 'etat_fp_rs', 'nsf_code_fp_rs', 'nsf_name_fp_rs', 'formacode_code_fp_rs', 'formacode_name_fp_rs' ]

    #     fieldnames = ['filiere', 'titre_formation', 'id_formation', 'id_certif', 'location', 'date_debut', 'id_formation_session', 'id_certif_fp', 'titre', 'etat', 'nsf_code', 'nsf_name', 'formacode', 'formaname', 'niveau' ]

        
    #     # Création de l'objet writer avec les en-têtes
    #     self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        
    #     # Écriture des en-têtes
    #     self.writer.writeheader()

    # def close_spider(self, spider):
    #     # Fermeture du fichier
    #     self.file.close()

    # def process_item(self, item, spider):
    #     # Écriture des données
    #     self.writer.writerow(item)
    #     return item


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


    