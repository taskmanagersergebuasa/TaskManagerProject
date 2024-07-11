# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class FormationscraperPipeline:
    def process_item(self, item, spider):
        return item


class CsvPipeline:
    def open_spider(self, spider):
        # Ouverture du fichier en mode écriture
        self.file = open('formation6.csv', 'w', newline='', encoding='utf-8')
        
        # Définition des en-têtes
        fieldnames = ['filiere', 'titre_formation', 'certif_rncp', 'certif_rs', 'certif_fp_rnpc', 'titre_certif_fp_rncp', 'etat_fp_rncp', 'niveau_fp_rncp', 'nsf_fp_rncp', 'formacode_fp_rncp', 'certif_fp_rs', 'titre_certif_fp_rs', 'etat_fp_rs', 'nsf_fp_rs', 'formacode_fp_rs' ]
        
        # Création de l'objet writer avec les en-têtes
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        
        # Écriture des en-têtes
        self.writer.writeheader()

    def close_spider(self, spider):
        # Fermeture du fichier
        self.file.close()

    def process_item(self, item, spider):
        # Écriture des données
        self.writer.writerow(item)
        return item
