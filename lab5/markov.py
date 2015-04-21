#!/usr/bin/python
import pickle
import codecs
import random
import re

random.seed()

class MarkovChain(object):


	def __init__(self):
		self.n = 2

	def generate_markov_chain(self,ngrams):
		stats = self._create_statistics(ngrams)
	
	def generate_ngrams(self,collection,letters):
		if letters == True:
			ngrams = [ ''.join([collection[i+j] for j in xrange(self.n)]) for i in xrange(len(collection) - self.n + 1) ]
		else:
			ngrams = [ [collection[i+j] for j in xrange(self.n)] for i in xrange(len(collection) - self.n + 1) ]
		return ngrams

	def generate_notes_from_file(self,filename):
		f = self._load_utf8_file(filename)
		ngrams = self.generate_ngrams(f.read().split(),False)
		stats = self._create_statistics(ngrams)
		return stats
		#out = open('stats')
		#pickle.dump(stats,out);

	def generate_words_from_file(self,filename):
		f = self._load_utf8_file(filename)
		ngrams = self.generate_ngrams(re.sub(r'[^[a-zA-Z]]','',''.join(f.read().strip().split())).lower(),True)
		stats = self._create_statistics(ngrams)
		return stats

	def generate_random_words(self,stats,min_length,max_length):
		l = 0
		s = u""
		min_length = int(random.random()*(max_length - min_length)+ min_length)
		while l < min_length:
			e = stats[random.choice(stats.keys())]
			next = len(e) > 0
			while next and l < min_length: 
				chosen = self._weighted_choice(e)
				s += chosen
				e = stats[chosen]
				next = len(e) > 0
				l += len(chosen)

		return s

	def generate_random_notes(self,stats, min_length, next_elements):
		l = 0
		s = u""
		while l < min_length:
			e = stats[random.choice(stats.keys())]
			next = len(e) > 0
			used = 0
			while next and used < next_elements:
				chosen = self._weighted_choice(e)
				used += 1
				s += u" " + chosen
				e = stats[chosen]
				next = len(e) > 0
				l += len(chosen)

		return s

	def _weighted_choice(self,choices):
			total = sum(choices[w] for w in choices)
			r = random.uniform(0, total)
			upto = 0
			for w in choices:
				if upto + choices[w] > r:
					return w
				upto += choices[w]

	def _create_statistics(self,ngrams):
		stats = {}
		for ngram in ngrams:
			if ngram[0] in stats:
				if ngram[1] in stats[ngram[0]]:
					stats[ngram[0]][ngram[1]] += 1
				else:	
					stats[ngram[0]][ngram[1]] = 1
			else:
				stats[ngram[0]] = {}
				stats[ngram[0]][ngram[1]] = 1

		for ngram in stats:
			count = 0.0
			for ngram1 in stats[ngram]:
				count += stats[ngram][ngram1]

			for foll_ngram in stats[ngram]:
				stats[ngram][foll_ngram] /= float(count)

		return stats


	def _load_utf8_file(self,filename):
		return codecs.open(filename,encoding="utf-8");


a = MarkovChain()
for i in xrange(10):
	print a.generate_random_words(a.generate_words_from_file('pap.txt'), 10, 15)

s = raw_input('>>>')
#print a.generate_ngrams(s.split(), False)
#print a.generate_ngrams(s, True)
#a._create_statistics(a.generate_ngrams(s.split(),False))