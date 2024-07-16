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
        rncp_url = response.xpath("//a[contains(@href, '/rncp/')]/@href").get()
        rs_urls = response.xpath("//a[contains(@href, '/rs/')]/@href").getall()
        item_formation["type_certif"] = ([rncp_url] + rs_urls) if rs_urls else [rncp_url] if rncp_url else []
        item_formation["id_certif"] = ([rncp_url] + rs_urls) if rs_urls else [rncp_url] if rncp_url else []
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
        item_rncp["certificateur"] = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell']/text()").get()
        item_rncp["siret"] = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell text-center']/text()").get()
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
        item_rs["certificateur"] = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell']/text()").get()
        item_rs["siret"] = response.xpath("//button[contains(text(),'Certificateur')]/following-sibling::div//td[@class='table--fcpt-certification__body__cell text-center']/text()").get()
        yield item_rs