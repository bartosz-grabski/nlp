#!/usr/bin/python
import sys
import collections
from levenshtein_distance import DamerauLevenshteinDistance


class Metrics(object):

	def __init__(self,n):
		self.n = n
		self.damerau_levensthtein = DamerauLevenshteinDistance()

	def generate_ngrams(self,str1):
		a = [ ''.join([str1[i+j] for j in xrange(self.n)]) for i in xrange(len(str1) - self.n + 1) ]
		dict_out = collections.defaultdict(lambda: 0)
		count = 0
		for el in a:
			dict_out[el] += 1
			count += 1
		dict_out[0] = count
		return dict_out


	def ngram_cosine_gen(self,str1,str2):
		ngrams1 = self.generate_ngrams(str1)
		ngrams2 = self.generate_ngrams(str2)
		dict1 = collections.defaultdict(lambda: 0)
		dict2 = collections.defaultdict(lambda: 0)
		for gram in ngrams1:
			dict1[gram] += 1
		for gram in ngrams2:
			dict2[gram] += 1
			
		dist = reduce(lambda x,y: x+y, map(lambda x:dict1[x]*dict2[x],dict1), 0.0)
		dist /= reduce(lambda x,y: x+y,map(lambda x: dict1[x],dict1)) + reduce(lambda x,y: x+y,map(lambda x: dict2[x],dict2))

		return 1.0 - dist

	def ngram_dice_gen(self,str1,str2):
		ngrams1 = [ ''.join([str1[i+j] for j in xrange(self.n)]) for i in xrange(len(str1) - self.n + 1) ]
		ngrams2 = [ ''.join([str2[i+j] for j in xrange(self.n)]) for i in xrange(len(str2) - self.n + 1) ]
		dict1 = collections.defaultdict(lambda: 0)
		dict2 = collections.defaultdict(lambda: 0)
		for gram in ngrams1:
			dict1[gram] += 1
		for gram in ngrams2:
			dict2[gram] += 1
		dict3 = collections.defaultdict(lambda: 0)
		for gram in dict2:
			if gram in dict1:
				dict3[gram] = 1

	def ngram_cosine(self,dict1,dict2):
			
		dist = reduce(lambda x,y: x+y, map(lambda x:dict1[x]*dict2[x],dict1), 0.0)
		dist /= reduce(lambda x,y: x+y,map(lambda x: dict1[x],dict1)) + reduce(lambda x,y: x+y,map(lambda x: dict2[x],dict2))

	def ngram_dice(self,dict1,dict2):
		count = 0.0
		for ngram in dict1:
			if ngram in dict2:
				count += 1
		dist = (count - 2) / (len(dict1) + len(dict2) - count)
		return 1.0 - 2 * dist

	def lcs(self,X, Y):
		m = len(X)
		n = len(Y)
		# An (m+1) times (n+1) matrix
		C = [[0 for j in range(n+1)] for i in range(m+1)]
		for i in range(1, m+1):
			for j in range(1, n+1):
				if X[i-1] == Y[j-1]: 
					C[i][j] = C[i-1][j-1] + 1
				else:
					C[i][j] = max(C[i][j-1], C[i-1][j])
		return 1.0 - float(C[m][n])/m if m > n else n

	def levenshtein(self,str1,str2):
		return 1.0 - self.damerau_levensthtein.check_damerau_iterative(str1,str2)/float(len(str1) if len(str1) > len(str2) else len(str2))

if __name__ == "__main__":
	m = Metrics()
	print m.ngram_cosine(3,sys.argv[1],sys.argv[2])
	print m.ngram_dice(3,sys.argv[1],sys.argv[2])
	print m.lcs(sys.argv[1],sys.argv[2])
	print m.levenshtein(sys.argv[1],sys.argv[2])
