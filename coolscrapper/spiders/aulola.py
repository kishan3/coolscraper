# -*- coding: utf-8 -*-
import scrapy


class AulolaSpider(scrapy.Spider):
    name = 'aulola'
    allowed_domains = ['www.aulola.co.uk/']
    start_urls = ['http://www.aulola.co.uk//']
    
    def parse(self, response):
        urls = response.css(".x-featured-product::attr(href)").extract()
        urls += response.css(".hot-products-text").xpath("./a/@href").extract()
        items = []
        for url in urls:
            yield response.follow(url, callback=self.extract_page, dont_filter=True)
    
    def extract_page(self, response):
        data = {}
        data['title'] = response.css('.commodity-title::text').extract_first()
        data['price'] = response.css('.product-price::text').extract_first()
        data['weight'] = response.css('.clo-f60::text').extract_first()
        data['moq'] = response.css('.li-moq-num::text').extract_first()
        data['total_cost'] = response.css('.n-total-cost-num::text').extract_first()
        # data['shipping_cost'] = response.css('.n-total-cost-num::text').extract_first()
        data['description'] = response.css('.tagContent').xpath('./p/text()').extract()
        data['item_code'] = response.css('.n-sku-num::text').extract_first()
        return data
