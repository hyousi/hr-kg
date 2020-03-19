# -*- coding: utf-8 -*-
import scrapy
from baidubk.items import RelationItem


class GraphSpider(scrapy.Spider):

    name = "graph"
    allowed_domains = ["baike.baidu.com"]

    def __init__(self):
        with open("people_filter.jl") as f:
            self.profiles = [eval(line.strip()) for line in f.readlines()]
        self.names = set(profile["name"] for profile in self.profiles)
        self.country_list = ["中国", "中华人民共和国", "中国香港"]

    def start_requests(self):
        for profile in self.profiles:
            name = profile["name"]
            url = url = "https://baike.baidu.com/item/" + name
            yield scrapy.Request(url, callback=self.parse, meta={"name": name})

    def parse(self, response):
        # 如果关系表中的人不在人名册中：1.将名字yield到人名册 2. 加入关系
        # 如果人民在人名册中：加入关系
        # relations = response.xpath('')
        ul = response.xpath("//dt/em[contains(text(), '关系')]/../..//ul/li")
        country = response.xpath(
            "//dt[contains(@class, 'basicInfo-item') and contains(text(), '国\xa0\xa0\xa0\xa0籍')]/following-sibling::*[1]/text()"
        ).get()
        name = response.meta.get("name")
        if name in self.names or (country and country.strip() in self.country_list):
            if ul:
                print("=" * 10 + name + "=" * 10)
                for li in ul:
                    friend_name, relation = li.xpath(
                        ".//div/@title | .//div/text()"
                    ).getall()
                    friend_link = li.xpath("./a/@href").get()
                    yield RelationItem(subj=name, pred=relation, obj=friend_name)
                    if friend_name not in self.names and friend_link:
                        yield response.follow(
                            friend_link, callback=self.parse, meta={"name": friend_name}
                        )

