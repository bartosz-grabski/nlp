import sys
import math

class CorpusBuilder(object):

	def __init__(self, n):
		self.n = n
		self.corpus = { 
			'english': [ "Harry Potter 1 Sorcerer's_Stone.txt", 
						 "Harry Potter 2 Chamber_of_Secrets.txt", 
						 "Harry Potter 3 Prisoner of Azkaban.txt", 
						 "Harry Potter 4 and the Goblet of Fire.txt" ],
			'german': [ '2momm10.txt', '4momm10.txt', '5momm10.txt', '8momm10.txt'],
			'finish': [ 'finnish.txt', 'finnish1.txt'],
			'italian': [ 'q.txt','54.txt' ],
			'polish': [ 'polski.txt', 'polski2.txt','polski3.txt'],
			'spanish': [ 'spanish.txt','spanish1.txt']
		}
		self.lang_dict = {}


	def build_test_data(self):
		for lang in self.corpus:
			lang_ngram_count = 0
			if not lang in self.lang_dict:
				self.lang_dict[lang] = {}
			for filename in self.corpus[lang]:
				with open(filename) as f:
					contents = ''.join(f.read().lower().strip().split())
					self.ngrams = [ ''.join([contents[i+j] for j in xrange(self.n)]) for i in xrange(len(contents) - self.n + 1) ]
					for ngram in self.ngrams:
						if ngram in self.lang_dict[lang]:
							self.lang_dict[lang][ngram] += 1
						else:
							self.lang_dict[lang][ngram] = 1
						lang_ngram_count += 1
			for ngram in self.lang_dict[lang]:
				self.lang_dict[lang][ngram] /= float(lang_ngram_count)

class LanguageIdentifier(object):

	def __init__(self,lang_dict,n):
		self.n = n
		self.lang_dict = lang_dict

	def identify_language(self,text):
		contents = ''.join(text.lower().strip().split())
		ngrams = [ ''.join([contents[i+j] for j in xrange(self.n)]) for i in xrange(len(contents) - self.n + 1)]
		scores = []

		for lang in self.lang_dict:
			scores.append((reduce(lambda x,y: x+y, map(lambda x: self.lang_dict[lang][x],filter(lambda x: x in self.lang_dict[lang],ngrams)),0.0),lang))
			
		highest = sorted(scores,key=lambda x: -x[0])
		print highest[0]



if __name__ == '__main__':
	builder = CorpusBuilder(int(sys.argv[1]))
	builder.build_test_data()
	identifier = LanguageIdentifier(builder.lang_dict, builder.n)
	while True:
		s = raw_input('>>>')
		if s == 'exit':
			break
		identifier.identify_language(s)
