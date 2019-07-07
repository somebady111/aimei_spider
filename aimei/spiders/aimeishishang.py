# -*- coding: utf-8 -*-
import scrapy
from ..items import ImageItem
from .. import settings


class AimeiPipeline(scrapy.Spider):
    name = 'aimeishishang'
    allowed_domains = ['www.aimeishishang.com']
    start_urls = ['https://www.aimeishishang.com/meituitupian/']

    def start_requests(self):
        for i in range(1, settings.PAGE + 1):
            url = 'https://www.aimeishishang.com/qipaomeinv/{}/'.format(i)
            print(url)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        text_url = response.xpath('//ul[@id="waterfall"]//div[@class="c cl"]/a/@href').extract()
        for result in text_url:
            yield scrapy.Request(result, self.parse_image)

    def parse_image(self, response):
        ps_url = response.xpath('//ignore_js_op/img/@zoomfile').extract()
        for p_url in ps_url:
            item = ImageItem()
            p_url = 'https://www.aimeishishang.com/' + p_url
            item['photo_url'] = p_url
            yield item
