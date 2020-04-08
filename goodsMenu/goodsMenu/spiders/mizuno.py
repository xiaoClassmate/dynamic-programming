# -*- coding: utf-8 -*-
import scrapy
import json
import random
import pretty_errors
from bs4 import BeautifulSoup
from goodsMenu.items import GoodsmenuItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MizunoSpider(CrawlSpider):
	name = 'mizuno'
	start_urls = []

	# rules = [
	#     Rule(
	#         LinkExtractor(allow=('/category/mens/')),
	#         callback = 'parse_list',
	#     )
	# ]

	serial = 0

	def start_requests(self):
		urls = ['https://www.mizunousa.com/category/sports/running/sports+running+apparel.do?c=100262.100269.100356&sortby=bestSellersAscend&pp=100',
				'https://www.mizunousa.com/category/sports/golf/accessories.do?c=100262.100351.100363&sortby=ourPicksAscend&pp=100',
				'https://www.mizunousa.com/category/sports/running/accessories.do?c=100262.100269.100357&sortby=ourPicksAscend&page=all']
		yield scrapy.Request(urls, self.parst_list)

	def parst_list(self, response):
		domain = ['https://www.mizunousa.com']
		soup = BeautifulSoup(response.body, 'lxml')
		for post in soup.select('div.ml-thumb-image-container'):
			yield scrapy.Request(domain[0] + post.select('a')[0]['href'], self.parse_detail)

	def parse_detail(self, response):
		soup = BeautifulSoup(response.body, 'lxml')
		# print(response.url)

		self.serial += 1
		number = random.randint(1, 10)

		name = soup.select('div.ml-product-name')[0].text.strip().replace('\"','').replace('\u00ae','')
		value = int(soup.select('span.ml-item-price')[0].text.split('.')[0].replace('$',''))
		

		crawlitem = GoodsmenuItem()
		crawlitem['serial'] = self.serial
		crawlitem['name'] = name
		crawlitem['value'] = value
		crawlitem['number'] = number
		return crawlitem