import scrapy
from scrapy import Request
from ..items import PartnersItem
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import pathlib
import logging

logger = logging.getLogger()

option = input('What do you want? Enter "images" for images or "json" for json results, here>>>')

def run_jenwoodhouse_spider():
    if option == 'images':
        process = CrawlerProcess(settings={
            "RETRY_TIMES": 5,
            # "LOG_LEVEL":'I',
            # 'DOWNLOAD_DELAY': 1,
            "DOWNLOADER_MIDDLEWARES": {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            },
            "USER_AGENTS": [
                'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
                'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            ],
            "ROBOTSTXT_OBEY": False,
            "USER_AGENT": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            "ITEM_PIPELINES": {'partners.pipelines.PartnersPipeline': 1},
            "IMAGES_STORE": '.',
            }

        )
        process.crawl(JenwoodhouseSpider)
        process.start()
        process.stop()
    elif option == 'json':
        process = CrawlerProcess(settings={
            "RETRY_TIMES": 5,
            'DOWNLOAD_DELAY':0.1,
            "DOWNLOADER_MIDDLEWARES" : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
                },
            "USER_AGENTS" : [
            'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            ],
            "ROBOTSTXT_OBEY": False,
            "FEEDS": {
                pathlib.Path("JenWoodhouse_files/Results.json"): {"format": "json",
                                 "encoding": "utf-8"},
            },

        })
        process.crawl(JenwoodhouseSpider)
        process.start()
    elif option not in ['images', 'json']:
        logger.error('Wrong input, check spelling and try again')

class JenwoodhouseSpider(scrapy.Spider):
    name = 'jenwoodhouse'
    # allowed_domains = ['www.jenwoodhouse.com']
    start_urls = [
        'https://jenwoodhouse.com/category/furniture/',
        'https://jenwoodhouse.com/category/recipes/',
        'https://jenwoodhouse.com/category/crafts/',
        'https://jenwoodhouse.com/category/decorating/',
        'https://jenwoodhouse.com/category/kids/',
        'https://jenwoodhouse.com/category/lighting/',
        'https://jenwoodhouse.com/category/organization/',
        'https://jenwoodhouse.com/category/outdoor/'
                  ]

    def parse(self, response):
        items = response.xpath("//a[@class='entry-title-link']/@href").extract()
        self.project_count = len(items)

        if option == 'images':
            for url in items:
                yield Request(url = url, callback = self.parse_images)
        elif option == 'json':
            for url in items:
                yield Request(url = url, callback = self.parse_json)

        next_page_url = response.xpath("//li[@class='pagination-next']/a/@href").extract_first()
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse)

    def parse_images(self, response):
        header = response.xpath("//header/h1[@class='entry-title']/text()").extract_first()
        image_urls = response.xpath("//img[contains(@class,'alignnone')]/@src").extract()
        loader = ItemLoader(item=PartnersItem())
        for image in image_urls:
            loader.add_value('image_urls', image)
            loader.add_value('Title',header)

            yield loader.load_item()





    def parse_json(self, response):
        date_item = response.xpath("//time[@class='entry-time']/text()").extract()
        header = response.xpath("//header/h1[@class='entry-title']/text()").extract_first()
        tags = response.xpath("//header/p/span/a[@rel='category tag']/text()").extract()
        intro_header = response.xpath("//div[@class='entry-content']/h2/text()").extract_first()

        project_detail = {}

        intro_text = response.xpath("//div[@class='entry-content']/h2/following-sibling::p[not(preceding-sibling::div)]"
                                    "//text()").extract()
        intro_text_formatted = ''
        for text in intro_text:
            intro_text_formatted += text
        youtube_link = response.xpath("//div[@class='rll-youtube-player']/@data-src").extract_first()
        list_keywords = ['Tools', 'Supplies', 'Source', 'Shop', 'Cut']
        all_lists = []

        for keyword in list_keywords:
            list_xpaths = response.xpath(
                f"//div[@class='entry-content']/h3[contains(text(), '{keyword}')]/following-sibling::ul[1]/li")
            if list_xpaths:
                list_title = keyword
                list_content = {}
                list_content['Title'] = list_title
                items = []
                for list_xpath in list_xpaths:
                    item_name = list_xpath.xpath(".//text()").extract()
                    formatted_name = ''
                    for name in item_name:
                        formatted_name += name

                    item_url = list_xpath.xpath(".//@href").extract_first()
                    if item_url is not None:
                        formatted_item = formatted_name + '(link: ' + item_url + ')'
                    else:
                        formatted_item = formatted_name
                    items.append(formatted_item)

                list_content['items'] = items
                all_lists.append(list_content)


        for keyword in list_keywords:
            list_xpaths = response.xpath(
                f"//div[@class='entry-content']/h3[contains(span/text(), '{keyword.upper()}')]/following-sibling::ul[1]/li")
            if list_xpaths:
                list_title = keyword
                list_content = {}
                list_content['Title'] = list_title
                items = []
                for list_xpath in list_xpaths:
                    item_name = list_xpath.xpath(".//text()").extract()
                    formatted_name = ''
                    for name in item_name:
                        formatted_name += name

                    item_url = list_xpath.xpath(".//@href").extract_first()
                    if item_url is not None:
                        formatted_item = formatted_name + '(link: ' + item_url + ')'
                    else:
                        formatted_item = formatted_name
                    items.append(formatted_item)

                list_content['items'] = items
                all_lists.append(list_content)


        for keyword in list_keywords:
            list_xpaths = response.xpath(
                f"//div[@class='entry-content']/h3[contains(text(), '{keyword.upper()}')]/following-sibling::ul[1]/li")
            if list_xpaths:
                list_title = keyword
                list_content = {}
                list_content['Title'] = list_title
                items = []
                for list_xpath in list_xpaths:
                    item_name = list_xpath.xpath(".//text()").extract()
                    formatted_name = ''
                    for name in item_name:
                        formatted_name += name

                    item_url = list_xpath.xpath(".//@href").extract_first()
                    if item_url is not None:
                        formatted_item = formatted_name + '(link: ' + item_url + ')'
                    else:
                        formatted_item = formatted_name
                    items.append(formatted_item)

                list_content['items'] = items
                all_lists.append(list_content)            
        steps_xpath = response.xpath("//div[@class='entry-content']/h3[contains(text(), '')]")
        step_count = len(steps_xpath) + 1
        all_steps = []
        for i in range(1, step_count):
            step = {}
            step_title = response.xpath(
                f"(//div[@class='entry-content']/h3[contains(text(), '')]/text())[{i}]").extract_first()
            step_text = response.xpath(
                f"(//div[@class='entry-content']/h3[contains(text(), '')])[{i}]/following-sibling"
                f"::p[preceding-sibling::h3[{i}]][not(preceding-sibling::h3[{i + 1}])]//text()").extract()
            formatted_step_text = ''
            for text in step_text:
                formatted_step_text += text
            step['Title'] = step_title
            step['Text'] = formatted_step_text
            all_steps.append(step)

        project_detail['Published Date'] = date_item
        project_detail['Tags'] = tags
        project_detail['Intro Header'] = intro_header
        project_detail['Intro body'] = intro_text_formatted
        project_detail['Lists'] = all_lists
        project_detail['Steps'] = all_steps
        project_detail['Youtube Link'] = youtube_link
        project_detail['Page Url'] = response.url

        yield {
            header: project_detail
        }


run_jenwoodhouse_spider()



