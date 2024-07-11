# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationscraperItem(scrapy.Item):
    filiere = scrapy.Field()
    titre_formation = scrapy.Field()
    certif_rncp = scrapy.Field()
    certif_rs = scrapy.Field()
    sessions = scrapy.Field()
    id = scrapy.Field()


class SessionscraperItem(scrapy.Item):
    location = scrapy.Field()
    date_debut = scrapy.Field()
    id = scrapy.Field()

    
