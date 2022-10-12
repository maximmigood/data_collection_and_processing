import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/'
                  '%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0']

    def parse(self, response: HtmlResponse):
        site = 'https://www.labirint.ru'
        nxt = response.xpath('//a[@title="Следующая"]/@href').get()
        nxt = response.url.split("?")[0]+nxt
        books = response.xpath("//a[@class='product-title-link']/@href").getall()
        print(f'--------------------------------------\n'
              f'{response.url}\n'
              f'{nxt}\n'
              f'{len(books)}\n'
              f'{books[0]}\n'
              f'--------------------------------------')

        yield response.follow(nxt, callback=self.parse)

        for book in books:
            lnk = f'{site}{book}'
            yield response.follow(lnk, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        link = response.url
        name = response.css('h1::text').get().split(':', 1)[1].strip()
        author = response.xpath("//div[@class='authors']/a[@data-event-label='author']/text()").get()
        price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        price_full = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        if not price_full:
            price_full = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()

        # print(f'+++++++++++++++++++++++++++++++++++++\n'
        #       f'{link}\n'
        #       f'{name}\n'
        #       f'{author}\n'
        #       f'{price_full}\n'
        #       f'{price}\n'
        #       f'{rating}\n'
        #       f'++++++++++++++++++++++++++++++++++++++')
        yield BooksItem(
            link=link,
            name=name,
            author=author,
            price_full=price_full,
            price=price,
            rating=rating
        )
