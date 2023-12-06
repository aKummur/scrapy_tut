import scrapy


class WorldometerSpider(scrapy.Spider):
    name = "worldometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath(".//@href").get()

            # yield {
            #     'coountry_name': country_name,
            #     'link': link
            # }
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name':country_name})

    def parse_country(self, response):
        historic_data = response.xpath('(//table[contains(@class,"table")])[1]/tbody/tr')
        country = response.request.meta['country_name']
        
        for row in historic_data:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//strong/text()').get()

            yield {
                'country': country,
                'year' : year,
                'population' : population
            }
