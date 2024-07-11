

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import FormationscraperItem, SessionscraperItem

class FormationspiderSpider(CrawlSpider):
    name = "formationspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = (
        Rule(LinkExtractor(allow=r"https://simplon.co/formation/.*/\d+"), callback="parse_formation", follow=False),
        Rule(LinkExtractor(allow=r"https://simplon.co/i-apply/.*/\d+"), callback="parse_session", follow=False),
    )


    def parse_formation(self, response):
        item_formation = FormationscraperItem()
        item_formation["filiere"] = response.xpath("//li[@class='breadcrumb-item']//a[contains(@href, 'https://simplon.co/formations')]/text()").get()
        item_formation["titre_formation"] = response.xpath("//h1/text()").get()
        item_formation["certif_rncp"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RNCP')]/text()").getall()
        item_formation["certif_rs"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RS')]/text()").getall()
        item_formation["id"] = int(response.url.split('/')[-1])
        yield item_formation


    def parse_session(self, response):
        item_session = SessionscraperItem()
        item_session['date_debut'] = [i.strip() for i in response.xpath('//i[contains(text(), "event")]/../text()').getall() if i.strip() != '']
        item_session['location'] = [i.strip() for i in response.xpath('//i[contains(text(), "location_on")]/../text()').getall() if i.strip() != '']
        item_session["id"] = int(response.url.split('/')[-1])
        yield item_session




# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from ..items import FormationscraperItem, SessionscraperItem

# class FormationspiderSpider(CrawlSpider):
#     name = "formationspider"
#     allowed_domains = ["simplon.co"]
#     start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

#     rules = (Rule(LinkExtractor(allow=r"https://simplon.co/formation/.*/\d+"), callback="parse_formation", follow=False)     )


#     def parse_formation(self, response):
#         item_formation = FormationscraperItem()
#         item_formation["filiere"] = response.xpath("//li[@class='breadcrumb-item']//a[contains(@href, 'https://simplon.co/formations')]/text()").get()
#         item_formation["titre_formation"] = response.xpath("//h1/text()").get()
#         item_formation["certif_rncp"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RNCP')]/text()").getall()
#         item_formation["certif_rs"] = response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RS')]/text()").getall()
#         response.meta['item_formation'] = item_formation

#         session_link = response.xpath('//a[contains(@href, "/i-apply/")]/@href').get()
#         if session_link:
#             yield scrapy.Request(response.urljoin(session_link), callback=self.parse_session, meta={'item_formation': item_formation})
#         else :
#             item_formation['sessions'] = []
#             yield item_formation


#     def parse_session(self, response):
#         item_formation = response.meta.get('item_formation')
#         item_session = SessionscraperItem()
#         item_session['date_debut'] = [i.strip() for i in response.xpath('//i[contains(text(), "event")]/../text()').getall() if i.strip() != '']
#         item_session['location'] = [i.strip() for i in response.xpath('//i[contains(text(), "location_on")]/../text()').getall() if i.strip() != '']
#         item_formation['sessions'] = item_session
#         yield item_formation


