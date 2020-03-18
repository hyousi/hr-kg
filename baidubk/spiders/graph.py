# -*- coding: utf-8 -*-
import scrapy


class GraphSpider(scrapy.Spider):
    def __init__(self):
        with open("people.jl") as f:
            self.profiles = [eval(line.strip()) for line in f.readlines()]

    name = "graph"
    allowed_domains = ["baike.baidu.com"]
    start_urls = ["http://baike.baidu.com/"]

    def parse(self, response):
        pass
