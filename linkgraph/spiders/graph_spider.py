from urllib.parse import urlparse, urldefrag, unquote_plus

from scrapy.http.response import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from config_loader import get_configs
from linkgraph.items import LinkGraphItem


class GraphSpider(CrawlSpider):
    name = 'graph'

    allowed_domains = get_configs()['graph-spider']['allowed-domains']
    start_urls = get_configs()['graph-spider']['start-urls']

    rules = (
        Rule(LinkExtractor(allow='/*', attrs='href'), follow=True, callback='parse_item'),
    )

    def __is_valid_page_path(self, page_path):
        parsed_url = urlparse(page_path)
        for domain in self.allowed_domains:
            if domain not in parsed_url.netloc:
                return False
        return True

    def parse_item(self, response):
        item = LinkGraphItem()
        item['predecessor_url'] = unquote_plus(urldefrag(response.url).url.rstrip('/'))
        linked_urls = []
        for anchor in response.css('a::attr(href)'):
            page_path = urljoin(response.url, anchor.get())
            is_valid = self.__is_valid_page_path(page_path)
            if is_valid:
                page_path = unquote_plus(urldefrag(page_path).url.rstrip('/'))
                linked_urls.append(page_path)
        item['successor_urls'] = linked_urls
        return item
