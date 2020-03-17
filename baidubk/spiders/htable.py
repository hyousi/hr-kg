# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from baidubk.items import BaidubkItem


class HtableSpider(scrapy.Spider):
    name = "htable"
    allowed_domains = ["baike.baidu.com"]

    def start_requests(self):
        years = range(1970, 2020)
        urls = [f"https://baike.baidu.com/item/{year}年" for year in years]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        year = response.url.split("item/")[1].split("/")[0]
        year = urllib.parse.unquote(year)
        paras = response.xpath("//div[@class='para']/a/..")
        for para in paras:
            data = para.xpath("./text() | ./a/text()").getall()
            if (len(data)) != 3:
                continue
            birth, name, desc = [_.strip() for _ in data]
            if birth[-1] != "—" or "中国" not in desc:
                continue
            # ['1月24日——', '小彩旗', '，中国香港男歌手。']
            birth = year + birth[:-2]
            profile_url = para.xpath("./a/@href").get()
            yield response.follow(
                url=profile_url,
                callback=self.parse_profile,
                meta={"flag": "true", "name": name},
            )

    def parse_profile(self, response):
        name = response.meta.get("name")
        birth = response.xpath("//div/dl/dd").re("\d+年\d+月\d+日")
        flag = bool(response.meta.get("flag"))
        if len(birth) > 0:
            birth = birth[0]
            yield BaidubkItem(name=name, birth=birth)
        if flag:
            ul = response.xpath("//dt[contains(text(), '明星')]/..//ul/li")
            if len(ul) > 0:
                for li in ul:
                    profile_url = li.xpath("./a/@href").get()
                    div = li.xpath(".//div[@class='name']")
                    friend_name, relation = div.xpath("text() | @title").getall()
                    yield response.follow(
                        url=profile_url,
                        callback=self.parse_profile,
                        meta={"flag": "false", "name": friend_name},
                    )
