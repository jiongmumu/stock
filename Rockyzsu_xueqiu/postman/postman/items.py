# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostmanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    userid = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    retweet_count = scrapy.Field()
    reply_count = scrapy.Field()
    fav_count = scrapy.Field()
    truncated = scrapy.Field()
    commentId = scrapy.Field()
    symbol_id = scrapy.Field()
    description = scrapy.Field()
    source_link = scrapy.Field()
    user = scrapy.Field()
    target = scrapy.Field()
    timeBefore = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    retweeted_status = scrapy.Field()
    # source = scrapy.Field()
    # source = scrapy.Field()
