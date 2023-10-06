## создаём парсер данных

from bs4 import BeautifulSoup as bs # навигация в разметке html кода
import requests

class Parser:
	def __init__(self, url='https://zakupki.gov.ru/epz/order/extendedsearch/results.html'):
		self.url = url
		self.info = dict()
		self.filtered_cards = list()

	def get_page(self):
		page = requests.get(self.url)
		if str(page.status_code) == '200':
			print('connected')
		content = bs(page.text, 'html.parser')
		return content


	def filter_page(self):
		cards = self.get_page().findAll('div', class_='row no-gutters registry-entry__form mr-0')
		
		def param(class_):
			p = card.find('div', class_=class_)
			return p
		
		for card in cards:
		
			self.info['name'] = param('registry-entry__body-value').text.strip()
			self.info['price'] = ''.join(i for i in param('price-block__value').text if i.isdigit() or i == ',' or i == '₽')
			self.info['fdate'] = param('data-block mt-auto').findAll('div', class_='data-block__value')[0].text
			self.info['ldate'] = param('data-block mt-auto').findAll('div', class_='data-block__value')[1].text
			self.info['customer'] = param('registry-entry__body-href').text.strip().lower()
			self.info['number'] = param('registry-entry__header-mid__number').text.strip()[2:]
			self.info['link'] = 'https://zakupki.gov.ru' + param('registry-entry__header-mid__number').find('a')['href']

			self.filtered_cards.append(self.info)

			print(self.filtered_cards)


		return self.filtered_cards
