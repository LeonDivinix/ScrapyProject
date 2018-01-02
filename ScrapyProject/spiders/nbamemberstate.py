# -*- coding: utf-8 -*-
import scrapy
import json
import os
import datetime

from scrapy import Selector

PATH = "D:/live/"
PUBLISH_VERSION = 1


# 爬取nba球员状态
class NbaMemberStateSpider(scrapy.Spider):
    name = "nba_member_state"
    allowed_domains = ["rotoworld.com"]
    start_urls = ['http://www.rotoworld.com/teams/injuries/nba/all/']
    handle_httpstatus_list = [404, 403, 408]

    def parse(self, response):
        result = {'status': 0}
        status = response.status
        if status in [404, 403, 408]:
            result['status'] = status
        else:
            areas = response.xpath('//div[@class="pb"]').extract()
            count = len(areas)
            list = []
            if count == 0:
                result['status'] = 1
            else:
                for i in range(count):
                    content = Selector(text=areas[i])
                    teams = content.xpath('//a[re:test(@href, "/teams/nba/")]/text()').extract()
                    members = content.xpath('//td//a/text()').extract()
                    remarks = content.xpath('//div[@class=\'report\']/text()').extract()
                    items = content.xpath('//td/text()').extract()
                    ids = content.xpath('//div[@class="playercard"]/@id').extract()
                    num = len(members)
                    if num == 0 or len(teams) == 0 or len(members) == 0 or len(remarks) == 0 or len(items) == 0:
                        result['status'] = 2
                        break
                    else:
                        for j in range(num):
                            data = {}
                            data['id'] = ids[j]
                            data['teamName'] = teams[0]
                            data['name'] = members[j]
                            data['pos'] = items[j * 5]
                            data['status'] = items[j * 5 + 1]
                            data['date'] = items[j * 5 + 2].replace(u'\xa0', u' ')
                            data['injury'] = items[j * 5 + 3]
                            data['returns'] = items[j * 5 + 4]
                            data['remark'] = remarks[j]
                            list.append(data)
                if result['status'] == 0:
                    result['result'] = list
        if PUBLISH_VERSION == 1:
            filename = PATH + datetime.datetime.now().strftime('%Y%m%d%H%M') + ".json"
            with open(filename, 'w') as f:
                f.write(json.dumps(result))
        with open(PATH + "999999999999.json", 'w') as f:
            f.write(json.dumps(result))
        pass
