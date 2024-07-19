from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import FormationItem, SessionItem, RncpItem, RsItem, NsfItem, FormaItem, CertificateurItem
import scrapy

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
        rncp_url = response.xpath("//a[contains(@href, '/rncp/')]/@href").get()
        rs_urls = response.xpath("//a[contains(@href, '/rs/')]/@href").getall()
        item_formation["type_certif"] = ([rncp_url] + rs_urls) if rs_urls else [rncp_url] if rncp_url else []
        item_formation["id_certif"] = ([rncp_url] + rs_urls) if rs_urls else [rncp_url] if rncp_url else []
        yield item_formation


    def parse_session(self, response):
        id_formation = response.url
        dates_debut = response.xpath('//i[contains(text(), "event")]/../text()').getall()[1::2]
        locations = response.xpath('//i[contains(text(), "location_on")]/../text()').getall()[1::2]
        durees = response.xpath('//i[contains(text(), "hourglass_empty")]/../text()').getall()[1::2]
        for date_debut,location,duree in zip(dates_debut,locations,durees):
            item_session = SessionItem()
            item_session["id_formation"] = id_formation
            item_session["date_debut"] = date_debut
            item_session["location"] = location
            item_session["duree"] = duree
            yield item_session


    def parse_nsf(self, response, item_certif):
        nsf_codes = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        nsf_names = response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()[1::2]
        for nsf_code,nsf_name in zip(nsf_codes,nsf_names):
            item_nsf = NsfItem()
            item_nsf["code"] = nsf_code
            item_nsf["name"] = nsf_name
            item_nsf["type_certif"] = item_certif["type_certif"]
            item_nsf["id_certif"] = item_certif["id_certif"]
            yield item_nsf


    def parse_forma(self, response, item_certif):
        formacodes = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").getall()
        formanames = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()[1::2]
        for formacode,formaname in zip(formacodes,formanames):
            item_forma = FormaItem()
            item_forma["code"] = formacode
            item_forma["name"] = formaname
            item_forma["type_certif"] = item_certif["type_certif"]
            item_forma["id_certif"] = item_certif["id_certif"]
            yield item_forma


    def parse_certificateur(self, response, item_certif):
        sirets = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell text-center']/text()").getall()
        certificateur_names = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell']/text()").getall()
        for siret,certificateur_name in zip(sirets,certificateur_names):
            item_certificateur = CertificateurItem()
            item_certificateur["siret"] = siret
            item_certificateur["certificateur_name"] = certificateur_name
            item_certificateur["type_certif"] = item_certif["type_certif"]
            item_certificateur["id_certif"] = item_certif["id_certif"]
            yield item_certificateur


    def parse_certif(self, response, item_certif):
        item_certif["type_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_certif["id_certif"] = response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        item_certif["titre"] = response.xpath("//h1[@class='title--page--generic']/text()").get()
        item_certif["etat"] = response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get()
        yield item_certif
        yield from self.parse_nsf(response, item_certif)
        yield from self.parse_forma(response, item_certif)
        yield from self.parse_certificateur(response, item_certif)


    
    def parse_rncp(self, response):
        self.logger.debug(f"Processing RNCP certification for {response.url}")
        item_rncp = RncpItem()
        item_rncp["niveau"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").get()
        yield from self.parse_certif(response, item_rncp)


    def parse_rs(self, response):
        self.logger.debug(f"Processing RS certification for {response.url}")
        item_rs = RsItem()
        yield from self.parse_certif(response, item_rs)