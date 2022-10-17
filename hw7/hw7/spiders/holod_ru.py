import scrapy
from scrapy.http import HtmlResponse

class HolodRuSpider(scrapy.Spider):
    name = 'holod_ru'
    allowed_domains = ['holodilnik.ru']
    start_urls = ['https://www.holodilnik.ru/smarthome/']

    def parse(self, response: HtmlResponse):
        next_lnk = response.xpath('//a[@aria-label="Следующая"]/@href').get()
        items = response.xpath('//div[@class="product-name"]/a/@href').getall()
        if next_lnk:
            yield response.follow(next_lnk, callback=self.parse)
        print(f'===================================\n'
              f'{response.url}\n'
              f'{next_lnk}\n'
              f'{len(items)}\n'
              f'===================================')
        yield response.follow(items[7], callback=self.parse_item)
        yield response.follow(items[8], callback=self.parse_item)


    def parse_item(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        old_price = response.xpath('//div[@class="price_old"]/text()').get()
        actual_price = response.xpath('//div[@class="prc_val"]/span/text()').get()
        url = response.url
        print(f'++++++++++++++++++++++++++++++++++++++++\n'
              f'{name}\n'
              f'{old_price}\n'
              f'{actual_price}\n'
              f'{url}\n'
              f'++++++++++++++++++++++++++++++++++++++++')
