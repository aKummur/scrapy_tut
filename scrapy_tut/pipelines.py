# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo as pym


class MongoDbPipeline:
    collection_name = "transcripts"

    def open_spider(self, spider):
        self.client = pym.MongoClient("mongodb+srv://adarshkummur:aks@cluster0.huneuxs.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["My_DB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item