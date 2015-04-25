#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import codecs
import random
import collections
import re

random.seed()

class MarkovChain(object):


	def __init__(self):
		self.n = 4

	def generate_markov_chain(self,ngrams):
		stats = self._create_statistics(ngrams)
	
	def generate_ngrams(self,collection,letters):
		if letters == True:
			ngrams = [ (''.join([collection[i+j] for j in xrange(self.n )]),collection[i+ self.n - 1]) for i in xrange(len(collection) - self.n + 1) ]
		else:
			ngrams = [ (' '.join([collection[i+j] for j in xrange(self.n)]), collection[i + self.n - 1]) for i in xrange(len(collection) - self.n + 1) ]
		return ngrams

	def generate_notes_from_file(self,filename,min_length,number_of_notes):
		f = self._load_utf8_file(filename)
		ngrams = self.generate_ngrams(re.sub("#[0-9]+","",f.read()).split(),False)
		stats = self._create_statistics(ngrams)
		for i in xrange(number_of_notes):
			print self.generate_random_notes(stats,min_length)
			print
		return stats

	def generate_words_from_file(self,filename,min_length,max_length,number_of_words):
		f = self._load_utf8_file(filename)
		ngrams = self.generate_ngrams(re.sub(r'[^ a-zążćśńółę]','',f.read().lower().strip()),True)
		stats = self._create_statistics(ngrams)
		for i in xrange(number_of_words):
			print self.generate_random_words(stats,min_length, max_length)
			print
		return stats

	def generate_random_words(self,stats,min_length,max_length):
		s = u""
		e = random.choice(stats.keys())
		min_length = int(random.random()*(max_length - min_length)+ min_length)
		while len(s) < min_length:
			chosen = self._weighted_choice(stats[e])
			if chosen != None:
				s += stats[e][chosen]["last"]
				e = chosen
			else:
				e = random.choice(stats.keys())

		return s

	def generate_random_notes(self,stats, min_length):
		s = u""
		e = random.choice(stats.keys())
		s += e
		while len(s) < min_length:
			chosen = self._weighted_choice(stats[e])
			if chosen != None:
				s += u" " + stats[e][chosen]["last"]
				e = chosen
			else:
				s += "."
				e = random.choice(stats.keys())
		return s

	def _weighted_choice(self,choices):
			total = sum(choices[w]["prob"] for w in choices)
			r = random.uniform(0, total)
			upto = 0
			for w in choices:
				if upto + choices[w]["prob"] > r:
					return w
				upto += choices[w]["prob"]

	def _create_statistics(self,ngrams):

		stats = {}

		for i in xrange(len(ngrams)-1):
			curr = ngrams[i]
			next = ngrams[i+1]
			if curr[0] in stats:
				if next[0] in stats[curr[0]]:
					stats[curr[0]][next[0]]["prob"] += 1.0
				else:
					stats[curr[0]][next[0]] = { "prob" : 1.0, "last": next[1]}
			else:
				stats[curr[0]] = {}
				stats[curr[0]][next[0]] = { "prob" : 1.0, "last": next[1]}


		for ngram in stats:
			count = 0.0
			for ngram1 in stats[ngram]:
				count += stats[ngram][ngram1]["prob"]

			for ngram1 in stats[ngram]:
				stats[ngram][ngram1]["prob"] /= count

		return stats



	def _load_utf8_file(self,filename):
		return codecs.open(filename,encoding="utf-8");

#
a = MarkovChain()
#words = a.generate_notes_from_file('pap_training.txt');
#for i in xrange(10):
#	print a.generate_random_notes(words,150,6)
#
#print "############# WORDS ##############"

#letters = a.generate_words_from_file('pap_training.txt')
#for i in xrange(10):
#	print a.generate_random_words(letters, 10, 15)

#s = raw_input('>>>')
#print a.generate_ngrams(s.split(), False)
#print a.generate_ngrams(s, True)
stats = a.generate_notes_from_file('pap.txt',500,10);
a.generate_words_from_file('pap.txt',7,15,10)