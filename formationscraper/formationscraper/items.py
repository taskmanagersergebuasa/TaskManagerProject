# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationscraperItem(scrapy.Item):
    # define the fields for your item here like:
    filiere = scrapy.Field()
    titre_formation = scrapy.Field()
    # simplon_titre_certif = scrapy.Field()
    # certif_france_competence = scrapy.Field()
    certif_rncp = scrapy.Field()
    certif_rs = scrapy.Field()
    
