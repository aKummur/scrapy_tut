import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()
        countries = response.xpath('//*[@id="example2"]/tbody/tr/td/a/text()').getall()

        yield {
            'title': title,
            'countries': countries
        }
