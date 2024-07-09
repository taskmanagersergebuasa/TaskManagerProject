import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FormationspiderSpider(CrawlSpider):
    name = "formationspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = (Rule(LinkExtractor(allow=r"https://simplon.co/formation/.*/\d+"), callback="parse_item", follow=False),
             Rule(LinkExtractor(allow=r"https://simplon.co/i-apply/.*/\d+"), callback="parse_session", follow=False),)

    def parse_item(self, response):
        item = {}
        item["filiere"] = response.xpath("//li[@class='breadcrumb-item']//a[contains(@href, 'https://simplon.co/formations')]/text()").get()
        item["titre_formation"] = response.xpath("//h1/text()").get()
        # item["simplon_titre_certif"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(@href, 'simplon.co')]/text()").getall()
        # item["certif_france_competence"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(@href, 'francecompetences.fr')]/text()").getall()
        item["certif_rncp"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RNCP')]/text()").getall()
        item["certif_rs"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RS')]/text()").getall()

        yield item

    