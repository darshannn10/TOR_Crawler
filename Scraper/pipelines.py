# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from . import settings
# from .settings import (
#     MONGODB_SERVER,
#     MONGODB_PORT,
#     MONGODB_DB,
#     MONGODB_COLLECTION
# )

# class DarkWebScrapingPipeline:

#     def process_item(self, item, spider):
#         return item 


# class MongoDBPipeline(object):
#     def __init__(self):
#         self.connection = pymongo.MongoClient("mongodb+srv://crawleruser:crawleruser@cluster0.rj3te.mongodb.net/OnionCrawler?retryWrites=true&w=majority")
#         self.db = self.connection[MONGODB_DB]
#         self.collection = self.db[MONGODB_COLLECTION]

#     def process_item(self, item, spider):
#         self.collection.insert(dict(item))
#         return item

class DarkWebScrapingPipeline:

    ## Local
    # def __init__(self):
    #     self.connection = pymongo.MongoClient("mongodb+srv://crawleruser:crawleruser@cluster0.rj3te.mongodb.net/OnionCrawler?retryWrites=true&w=majority")
    #     db = self.connection['oc-collection']
    #     self.collection = db.ocdb
    def __init__(self):        
        client = pymongo.MongoClient("mongodb+srv://crawleruser:crawleruser@cluster0.rj3te.mongodb.net/OnionCrawler?retryWrites=true&w=majority")
        db = client.data
        self.collection = db.occ

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        #return item
        return ''