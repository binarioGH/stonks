#-*-coding: utf-8-*-

from json import loads



class Searcher:
	def __init__(self, file='symbols.json'):
		self.file = file
		self.data = {}
		self.load_data()


	def load_data(self):
		with open(self.file, "r") as f:
			self.data = loads(f.read())


	def search(self, string):
		results = []
		for entry in self.data:
			if string.lower() in entry.lower():
				results.append([entry, self.data[entry]])

		return results
