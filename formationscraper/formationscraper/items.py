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
    type_certif = scrapy.Field()
    id_certif = scrapy.Field()

class SessionItem(scrapy.Item):
    id_formation = scrapy.Field()
    location = scrapy.Field()
    date_debut = scrapy.Field()
    duree = scrapy.Field()
    
class CertifItemBase(ABC,scrapy.Item):
    type_certif = scrapy.Field()
    id_certif = scrapy.Field()
    titre = scrapy.Field()
    etat = scrapy.Field()
    nsf = scrapy.Field()
    forma = scrapy.Field()
    certificateur = scrapy.Field()

class RncpItem(CertifItemBase):
    niveau = scrapy.Field()

class RsItem(CertifItemBase):
    pass

class CodeItem(ABC,scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    type_certif = scrapy.Field()
    id_certif = scrapy.Field()

class NsfItem(CodeItem):
    pass

class FormaItem(CodeItem):
    pass

class CertificateurItem(scrapy.Item):
    siret = scrapy.Field()
    certificateur_name = scrapy.Field()
    type_certif = scrapy.Field()
    id_certif = scrapy.Field()
