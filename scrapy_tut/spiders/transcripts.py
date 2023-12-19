import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies"]
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]/a')), callback="parse_item", follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@rel='next'])[1]")), process_request='set_user_agent'),
        )
    
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")

        yield {
            'title': article.xpath("./h1/text()").get(),
            'plot': article.xpath("./p/text()").get(),
            # 'transcript': article.xpath("./div[@class='full-script']/text()").getall(),
            # 'url': response.url,
            # 'user-agent': response.request.headers['User-Agent'],
        }
