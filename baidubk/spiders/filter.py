# -*- coding: utf-8 -*-
import scrapy


class FilterSpider(scrapy.Spider):

    name = "filter"
    allowed_domains = ["baike.baidu.com"]

    def __init__(self):
        with open("people.jl") as f:
            self.profiles = [eval(line.strip()) for line in f.readlines()]
        self.country_list = ["中国", "中华人民共和国", "中国香港"]

    def start_requests(self):
        for profile in self.profiles:
            url = "https://baike.baidu.com/item/" + profile["name"]
            yield scrapy.Request(
                url, callback=self.parse, meta={"name": profile["name"]}
            )

    def parse(self, response):
        country = response.xpath(
            "//dt[contains(@class, 'basicInfo-item') and contains(text(), '国\xa0\xa0\xa0\xa0籍')]/following-sibling::*[1]/text()"
        ).get()
        if country:
            country = country.strip()
            if country in self.country_list:
                name = response.meta.get("name")
                print(f"{name} - {country}")
                yield {"name": name}
