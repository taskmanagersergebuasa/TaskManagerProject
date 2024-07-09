import pytest
from scrapy.http import Request, HtmlResponse

from formationscraper.formationscraper.spiders.formationspider import FormationspiderSpider

@pytest.fixture
def a_response():
    """
    home maid html response for testing
    construire le body pour chaque elt de l item parsé
    choisir des valeurs réelles sur un cas pour verifier 
    la perennite du spider
    """
    html = ""

    # le request est l url que je scrappe
    request = Request(url="")
    # je fournit la reponse avec mon html csutom
    response = HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
    return response


    # je compare

def test_parse_item(a_response):
    spider = FormationspiderSpider() 
    parsed_items = list(spider.parse_item(a_response))
    assert len(parsed_items) == 1

    item = parsed_items[0]
    assert item['domain_id'] == ''
    assert item['name'] == ''
    assert item['description'] == ''


    pass