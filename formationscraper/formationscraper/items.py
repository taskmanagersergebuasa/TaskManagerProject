# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationscraperItem(scrapy.Item):
    # define the fields for your item here like:
    filiere = scrapy.Field()
    titre_formation = scrapy.Field()
    # certif_rncp = scrapy.Field()
    # certif_rs = scrapy.Field()
    certif_fp_rnpc = scrapy.Field()
    titre_certif_fp_rncp = scrapy.Field()
    etat_fp_rncp = scrapy.Field()
    niveau_fp_rncp = scrapy.Field()
    nsf_fp_rncp  = scrapy.Field()
    formacode_fp_rncp = scrapy.Field()
    certif_fp_rs = scrapy.Field()
    titre_certif_fp_rs = scrapy.Field()
    etat_fp_rs = scrapy.Field()
    nsf_fp_rs = scrapy.Field()
    formacode_fp_rs = scrapy.Field()
