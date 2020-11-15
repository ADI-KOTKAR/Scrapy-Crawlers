# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3
import os

class SQLitePipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO besT_movies (title, year, duration, genre, rating, movie_url) VALUES (?,?,?,?,?,?)
        ''', (
            item.get('title'), 
            item.get('year'), 
            item.get('duration'), 
            item.get('genre'), 
            item.get('rating'), 
            item.get('movie_url')
        ))
        self.connection.commit()        
        return item


class MongodbPipeline(object):
    collection_name = "best_movies"

    def open_spider(self, spider):
        mongo_uri = os.environ.get('MONGO_URI')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item )
        return item
