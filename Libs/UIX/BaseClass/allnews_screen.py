import json
from Libs.UIX.components.articlecard import ArticleCard
from components.screen import PScreen
from kivy.properties import ListProperty, StringProperty
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from kivy.clock import Clock

class AllNewsScreen(PScreen):

	date = StringProperty("")
	articles = []
	category = "News"
	oldcategory = "News"

	def __init__(self, **kwargs):
		Clock.schedule_once(self.render, .1)
		Clock.schedule_interval(self.OnCategoryChange, 1)
		super().__init__(**kwargs)

	def render(self, _):
		with open('assets//Files//News.json', 'r') as file:
			news = json.load(file)
		self.all_articles = news[self.category]

		self.articles = []

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
				cover = "assets//Images//logo.png"

			art['title'] = article['title']
			art['cover'] = cover
			art['publisher'] = article['source']['name']
			art['date'] = article['publishedAt'][0:10]
			art['content'] = content
			art['link'] = article['url']
			self.articles.append(art)

		grid = self.ids.gl_all
		grid.clear_widgets()

		for article in self.articles:
			art = ArticleCard()
			
			art.title = article['title']
			art.cover = article['cover']
			art.publisher = article['publisher']
			art.date = article['date']
			art.content = article['content']
			art.link = article['link']


			grid.add_widget(art)

	def Category(self):
		PDialog(content=CategoryDialogContent()).open()

	def OnCategoryChange(self, _):
		if self.category != self.oldcategory:
			self.oldcategory = self.category
			self.ids.title.text = self.category
			self.render(_=None)

class CategoryDialogContent(PBoxLayout):
	
	def general(self):
		AllNewsScreen.category = "News"
	def business(self):
		AllNewsScreen.category = "Business"
	def entertainment(self):
		AllNewsScreen.category = "Entertainment"
	def health(self):
		AllNewsScreen.category = "Health"
	def science(self):
		AllNewsScreen.category = "Science"
	def sports(self):
		AllNewsScreen.category = "Sports"
	def technology(self):
		AllNewsScreen.category = "Technology"
