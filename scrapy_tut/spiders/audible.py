import scrapy


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):
        books = response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')
        
        for book in books:
            book_name = book.xpath('.//h3/a/text()').get()
            book_author = book.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_length = book.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()
            yield {
                'book_name': book_name,
                'author': book_author,
                'length': book_length
            }

        next_page = response.xpath('//span[contains(@class, "nextButton")]/a/@href').get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse) 
