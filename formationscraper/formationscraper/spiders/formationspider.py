import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FormationspiderSpider(CrawlSpider):
    name = "formationspider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]

    rules = (Rule(LinkExtractor(allow=r"https://simplon.co/formation/.*/\d+"), callback="parse_item", follow=True),)
            #  Rule(LinkExtractor(allow=r"https://www.francecompetences.fr/recherche/rncp/\d+"), callback="parse_certif_rncp", follow=True),
            #  Rule(LinkExtractor(allow=r"https://www.francecompetences.fr/recherche/rs/\d+"), callback="parse_certif_rs", follow=True),)

    def parse_item(self, response):
        item = {
        'filiere' : response.xpath("//li[@class='breadcrumb-item']//a[contains(@href, 'https://simplon.co/formations')]/text()").get(),
        'titre_formation' : response.xpath("//h1/text()").get(),
        # 'certif_rncp' : response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RNCP')]/text()").getall(),
        # 'certif_rs' : response.xpath("//div[@class='smp-box two-column certification']//div[@class='card-text']//a[contains(text(), 'RS')]/text()").getall()
        }

        links_rncp = response.xpath('//a[contains(@href, "francecompetences.fr/recherche/rncp")]/@href').getall()
        self.logger.debug(f"Found RNCP certification links: {links_rncp}")

        links_rs = response.xpath('//a[contains(@href, "francecompetences.fr/recherche/rs")]/@href').getall()
        self.logger.debug(f"Found RS certification links: {links_rs}")

        # Si aucun lien n'est trouvé, on yield l'item directement
        if not links_rncp and not links_rs:
            self.logger.warning('No RNCP or RS links found on the initial page.')
            yield item
        else:
            # On suit les liens RNCP et RS
            for link in links_rncp:
                yield response.follow(link, callback=self.parse_certif_rncp, meta={'item': item}, dont_filter=True)

            for link in links_rs:
                yield response.follow(link, callback=self.parse_certif_rs, meta={'item': item}, dont_filter=True)


    def parse_certif_rncp(self, response):
        # suivre les liens RNCP (quand ils existent) et récupérer :
        item = response.meta['item']
        self.logger.debug(f"Processing RNCP certification for {response.url}")
        item.update({
            # numéro RNCP
            'certif_fp_rnpc' : response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
            # le titre de la formation
            'titre_certif_fp_rncp' : response.xpath("//h1[@class='title--page--generic']/text()").get(),
        
            # l'état
            'etat_fp_rncp' : response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
            # le niveau
            'niveau_fp_rncp' : response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text()").get(),
        
            # le(s) code(s) NSF et leur désignation
            'nsf_fp_rncp' : response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall(),
        
            # le(s) formacode(s) et leur désignation
            'formacode_fp_rncp' : response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        
        })

        yield item

    def parse_certif_rs(self, response):
    # suivre les liens RS (quand ils existent) et récupérer :
        item = response.meta['item']
        self.logger.debug(f"Processing RS certification for {response.url}")
        item.update({
            # numéro RS
            'certif_fp_rs' : response.xpath("//p[@class='tag--fcpt-certification black']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
            # le titre de la formation
            'titre_certif_fp_rs' : response.xpath("//h1[@class='title--page--generic']/text()").get(),
        
            # l'état
            'etat_fp_rs' : response.xpath("//p[@class='tag--fcpt-certification green']/span[@class='tag--fcpt-certification__status font-bold']/text()").get(),
        
            # le(s) code(s) NSF et leur désignation
            'nsf_fp_rs' : response.xpath("//p[contains(text(),'Code(s) NSF')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Code(s) NSF')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall(),
        
            # le(s) formacode(s) et leur désignation
            'formacode_fp_rs' : response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span[@class='list--fcpt-certification--essential--desktop__line__text--highlighted']/text() | //p[contains(text(),'Formacode')]/following-sibling::div/p[@class='list--fcpt-certification--essential--desktop__line__text__default']/text()").getall()
        
        })

        yield item