# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class PartnersItem(scrapy.Item):
    Title = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field()
