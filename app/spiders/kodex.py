import scrapy


class KodexSpider(scrapy.Spider):
    name = 'kodex'
    allowed_domains = ['kodex.com']
    start_urls = ['http://www.kodex.com/main.do']
    custom_settings = {
        'FEED_URI': 'tmp/kodex_total.csv'
    }

    def parse(self, response):
        for items in response.xpath('/html/body/div[3]/header/div/div[4]/div/div/div'):
            for item in items.css('li'):
                detail_data = {
                    'href': item.css('a').attrib['href'],
                    'title': item.css('a::text').get()
                }

                yield scrapy.Request(response.urljoin(detail_data['href']), self.parse_detail)
                break

    def parse_detail(self, response):
        yield {
            'title': ' '.join(response.xpath('/html/body/div[3]/div[2]/section/div[1]/div/h2/text()').getall()),
            'etf_num': response.xpath('/html/body/div[3]/div[2]/section/div[1]/div/h2/span/text()').get().strip('()'),
            'descution': ' '.join(''.join(response.xpath('/html/body/div[3]/div[2]/section/div[1]/div/p[2]/b/text()').getall()).split()),
            'index': {
                'value': ' '.join(response.css('.idx-value::text').get().split()),
                'text': ' '.join(''.join(response.xpath('/html/body/div[3]/div[2]/section/div[2]/div[4]/div[1]/p[2]/text()').getall()).split()),
                'href': response.xpath('/html/body/div[3]/div[2]/section/div[2]/div[4]/div[1]/a/@href').get()
            },
            'expense_rate': ' '.join(''.join(response.xpath('/html/body/div[3]/div[2]/section/div[2]/div[4]/div[1]/div/table/tbody/tr[3]/td[1]/text()').getall()).split()),
            'distributions': ' '.join(''.join(response.xpath('/html/body/div[3]/div[2]/section/div[2]/div[4]/div[1]/div/table/tbody/tr[4]/td[1]/text()').getall()).split())
        }