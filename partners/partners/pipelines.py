# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
import os
from urllib.parse import urlparse


class PartnersPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # for image_url in item.get('image_urls'):
        #   yield Request(url=image_url)
        return [Request(x, meta={'Name': item.get('Title')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None, *, item=None):
        # image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        Name = request.meta['Name']
        return f'JenWoodhouse_files/{Name}/' + os.path.basename(urlparse(request.url).path)

# class PartnersPipeline:
#     def process_item(self, item, spider):
#         return item
