# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class BaidubkPipeline(object):
    def __init__(self):
        super().__init__()
        self.item_set = set()

    def process_item(self, item, spider):
        uuid = item["name"] + item["birth"]
        if uuid in self.item_set:
            raise DropItem(f"重复项{item}")
        else:
            self.item_set.add(uuid)
            return item
