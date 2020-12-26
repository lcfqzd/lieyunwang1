import scrapy

from ..items import LieyunwangItem

class LieyunSpider(scrapy.Spider):
    name = 'lieyun_spider'
    allowed_domains = ['lieyunwang.com']
    start_urls = ['https://www.lieyunwang.com/latest/p1.html']
    # start_urls = []
    # for i in range(1,4):
    #     base_url = 'https://www.lieyunwang.com/latest/p{}.html'.format(i)
    #     start_urls.append(base_url)
    # print(start_urls)

    def parse(self, response):
        node_list = response.xpath('//*[@class="article-info pore"]')
        # print(len(node_list))
        item = LieyunwangItem()

        for div in node_list:
            item['title'] = div.xpath('./h2/a/text()').extract_first()
            item['content'] = div.xpath('./p[@class="article-digest mt10"]/text()').extract_first()
            yield item

        # 模拟翻页
        part_url = response.xpath('//*/li[@class ="next"]/a/@href').get()

        # 判断终止条件
        if part_url:
            next_url = response.urljoin(part_url)
            # 构建请求对象，并且返回给引擎
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )
