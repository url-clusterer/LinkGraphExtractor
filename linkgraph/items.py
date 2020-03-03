import scrapy


class LinkGraphItem(scrapy.Item):
    predecessor_url = scrapy.Field()
    successor_urls = scrapy.Field()
