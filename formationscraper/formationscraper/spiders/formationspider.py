from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import FormationItem, SessionItem, RncpItem, RsItem

class FormationspiderSpider(CrawlSpider):
    name = "formationspider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = (
        Rule(LinkExtractor(allow=r"https://simplon.co/formation/.*/\d+"), callback="parse_formation", follow=True),
        Rule(LinkExtractor(allow=r"https://simplon.co/i-apply/.*/\d+"), callback="parse_session", follow=False),
        Rule(LinkExtractor(allow=r"https://www.francecompetences.fr/recherche/rncp/\d+"), callback="parse_rncp", follow=False),
        Rule(LinkExtractor(allow=r"https://www.francecompetences.fr/recherche/rs/\d+"), callback="parse_rs", follow=False),
    )

    def parse_formation(self, response):
        item_formation = FormationItem()
        item_formation["filiere"] = response.xpath("//li[@class='breadcrumb-item']//a[contains(@href, 'https://simplon.co/formations')]/text()").get()
        item_formation["titre_formation"] = response.xpath("//h1/text()").get()
        item_formation["id_formation"] = response.url
        item_formation["type_certif"] = response.xpath("//li/a[contains(@href, '/rs/') or contains(@href, '/rncp/')]/@href").getall()
        item_formation["id_certif"] = response.xpath("//li/a[contains(@href, '/rs/') or contains(@href, '/rncp/')]/@href").getall()
        yield item_formation


    def parse_session(self, response):
        item_session = SessionItem()
        item_session["id_formation"] = response.url
        item_session["date_debut"] = response.xpath('//i[contains(text(), "event")]/../text()').getall()
        item_session["location"] = response.xpath('//i[contains(text(), "location_on")]/../text()').getall()
        item_session["duree"] = response.xpath('//i[contains(text(), "hourglass_empty")]/../text()').getall()
        yield item_session

    def parse_rncp(self, response):
        item_rncp = RncpItem()
        self.logger.debug(f"Processing RNCP certification for {response.url}")
        item_rncp["type_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rncp["id_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rncp["titre"] = response.xpath("//h1[@class='title--page--generic']/text()").get()
        item_rncp["etat"] = response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rncp["niveau"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").get()
        item_rncp["nsf_code"] = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        item_rncp["nsf_name"] = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        item_rncp["formacode"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        item_rncp["formaname"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        yield item_rncp


    def parse_rs(self, response):
        item_rs = RsItem()
        self.logger.debug(f"Processing RS certification for {response.url}")
        item_rs["type_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rs["id_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rs["titre"] = response.xpath("//h1[@class='title--page--generic']/text()").get()
        item_rs["etat"] = response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_rs["nsf_code"] = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        item_rs["nsf_name"] = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        item_rs["formacode"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        item_rs["formaname"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        yield item_rs



#     def parse_session(self, response):
#         item_formation = response.meta.get('item_formation')
#         item_session = SessionItem()
#         item_session['date_debut'] = [i.strip() for i in response.xpath('//i[contains(text(), "event")]/../text()').getall() if i.strip() != '']
#         item_session['location'] = [i.strip() for i in response.xpath('//i[contains(text(), "location_on")]/../text()').getall() if i.strip() != '']
#         item_formation['sessions'] = item_session
#         yield item_formation


    # def parse_rncp(self, response):
    #     # suivre les liens RNCP (quand ils existent) et récupérer :
    #     item = response.meta['item']
    #     self.logger.debug(f"Processing RNCP certification for {response.url}")
    #     item.update({
    #         # numéro RNCP
    #         'certif_fp_rnpc' : response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
    #         # le titre de la formation
    #         'titre_certif_fp_rncp' : response.xpath("//h1[@class='title--page--generic']/text()").get(),
        
    #         # l'état
    #         'etat_fp_rncp' : response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
    #         # le niveau
    #         'niveau_fp_rncp' : response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").get(),
        
    #         # le(s) code(s) NSF et leur désignation
    #         'nsf_fp_rncp' : response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall(),
        
    #         # le(s) formacode(s) et leur désignation
    #         'formacode_fp_rncp' : response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        
    #     })


    # def parse_rs(self, response):
    # # suivre les liens RS (quand ils existent) et récupérer :
    #     item = response.meta['item']
    #     self.logger.debug(f"Processing RS certification for {response.url}")
    #     item.update({
    #         # numéro RS
    #         'certif_fp_rs' : response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
    #         # le titre de la formation
    #         'titre_certif_fp_rs' : response.xpath("//h1[@class='title--page--generic']/text()").get(),
    #         # l'état
    #         'etat_fp_rs' : response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
    #         # le(s) code(s) NSF et leur désignation
    #         'nsf_fp_rs' : response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall(),
    #         # le(s) formacode(s) et leur désignation
    #         'formacode_fp_rs' : response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
    #     })
    #     yield item


