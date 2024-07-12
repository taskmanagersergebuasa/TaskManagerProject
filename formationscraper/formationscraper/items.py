# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from abc import ABC

class FormationItem(scrapy.Item):
    filiere = scrapy.Field()
    titre_formation = scrapy.Field()
    id_formation = scrapy.Field()
    id_certif = scrapy.Field()

class SessionItem(scrapy.Item):
    location = scrapy.Field()
    date_debut = scrapy.Field()
    id_formation = scrapy.Field()

class CertifItemBase(ABC,scrapy.Item):
    id_certif = scrapy.Field()
    titre = scrapy.Field()
    etat = scrapy.Field()
    nsf_code = scrapy.Field()
    nsf_name = scrapy.Field()
    formacode = scrapy.Field()
    formaname = scrapy.Field()

class RncpItem(CertifItemBase):
    niveau = scrapy.Field()

class RsItem(CertifItemBase):
    pass


    
    
