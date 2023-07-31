from newsapi.newsapi_client import NewsApiClient
import json
import datetime
import random
from Libs.UIX.components.articlecard import ArticleTile
from components.screen import PScreen
from kivy.properties import ListProperty, StringProperty
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from kivy.clock import Clock

class NewsScreen(PScreen):

	date = StringProperty("")
	articles = ListProperty([])

	def __init__(self, **kwargs):
		with open("assets//Files//Jokes.json", 'r') as file:
			self.jokes = json.load(file)
		date = datetime.datetime.now()
		with open('assets//Files//yesterdate.txt', 'r') as file:
			yesterdate = file.read()
		if yesterdate != str(date.strftime("%x")):
			yesterdate = str(date.strftime("%x"))
			with open('assets//Files//yesterdate.txt', 'w') as file:
				file.write(yesterdate)
			self.newsapi = NewsApiClient(api_key='f3409616bbd14dc197b83cd37dc4260c')
			all_articles = self.newsapi.get_top_headlines(category="general", language='en')
			business_articles = self.newsapi.get_top_headlines(category="business", language='en')
			entertainment_articles = self.newsapi.get_top_headlines(category="entertainment", language='en')
			health_articles = self.newsapi.get_top_headlines(category="health", language='en')
			science_articles = self.newsapi.get_top_headlines(category="science", language='en')
			sports_articles = self.newsapi.get_top_headlines(category="sports", language='en')
			technology_articles = self.newsapi.get_top_headlines(category="technology", language='en')
			with open('assets//Files//News.json', 'r') as file:
				data = json.load(file)
				data['News'] = all_articles
				data['Business'] = business_articles
				data['Entertainment'] = entertainment_articles
				data['Health'] = health_articles
				data['Science'] = science_articles
				data['Sports'] = sports_articles
				data['Technology'] = technology_articles
			with open('assets//Files//News.json', 'w') as file:
				json.dump(data, file, indent = 4)
		Clock.schedule_once(self.render, .1)
		super().__init__(**kwargs)

	def render(self, _):
		with open('assets//Files//News.json', 'r') as file:
			news = json.load(file)
		self.all_articles = news['News']
		for article in self.all_articles['articles']:
			art = {"title":"", "cover":"", "publisher":"", "date":"", "content":""}

			content = article['content']
			if not content:
				content = article['description']
			else:
				if not article['description']:
					content = content[:201]
				else:
					content = article['description'] + '\n' + content[:201]

			cover = article['urlToImage']
			if not cover:
				cover = "assets//Images//scenery.jpg"

			art['title'] = article['title']
			art['cover'] = cover
			art['publisher'] = article['source']['name']
			art['date'] = article['publishedAt'][0:10]
			art['content'] = content
			art['link'] = article['url']
			self.articles.append(art)

		grid1 = self.ids.gl_all
		grid1.clear_widgets()

		for article in self.articles:
			art = ArticleTile()
			
			art.title = article['title']
			art.cover = article['cover']
			art.publisher = article['publisher']
			art.date = article['date']
			art.content = article['content']
			art.link = article['link']

			grid1.add_widget(art)

	def show_joke(self):
		self.joke = random.choice(self.jokes["jokes"])
		PDialog(content=JokeDialogContent(joke = self.joke)).open()

class JokeDialogContent(PBoxLayout):
	joke = StringProperty("")