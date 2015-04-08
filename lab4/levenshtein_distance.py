#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

class LevenshteinDistance(object):

	def __init__(self):
		self.diacritics = { u'ą':'a',
			u'ę':'e',
			u'ć':'c',
			u'ż':'z',
			u'ź':'z',
			u'ó':'o',
			u'ń':'n',
			u'ł':'l',
			u'ś':'s' 
		}
		self.ortographical_errors_double = {
			'rz':u'ż',
			'ch':u'h',
			'om':u'ą'
		}
		self.ortographical_errors_single = {
			'u':u'ó',
			'w':u'f'
		}
		self.cost = 1
		self.cost_diacritics = 1
		self.cost_transposition = 1
		self.cost_ortographical = 1


	def check(self,str1,str2):
		
		if len(str1) == 0:
			return len(str2)
		if len(str2) == 0:
			return len(str1)

		cost = 0

		if str1[-1] != str2[-1]:
			cost = 1

		return min(self.check(str1[:-1],str2) + 1, self.check(str1,str2[:-1]) + 1, self.check(str1[:-1],str2[:-1]) + cost)


	def check_iterative(self,str1,str2):

		cost = self.cost

		d = [[0 for j in xrange(len(str2)+1)] for i in xrange(len(str1)+1)]

		for i in xrange(len(str1)+1):
			d[i][0] = i
		for j in xrange(len(str2)+1):
			d[0][j] = j

		for j in xrange(1,len(str2)+1):
			for i in xrange(1,len(str1)+1):

				if str1[i-1] == str2[j-1]:
					d[i][j] = d[i-1][j-1]

				else:
					d[i][j] = min(
						d[i-1][j]+cost,
						d[i][j-1]+cost,
						d[i-1][j-1]+self._check_diacritics(str1[i-1],str2[j-1]),
						d[i-1][j-1]+self._check_single_ortographical_error(str1[i-1],str2[j-1])
					)
				if i > 1 and j > 0:
					d[i][j] = min(
						d[i][j],
						d[i-2][j-1]+self._check_double_ortographical_error(str1[i-2:i],str2[j-1])	
					)
				if j > 1 and i > 0:
					d[i][j] = min(
						d[i][j],
						d[i-1][j-2]+self._check_double_ortographical_error(str2[j-2:j],str1[i-1])
					)

					

		return d[len(str1)][len(str2)]

	def _check_diacritics(self,c1,c2):
		"""Check if two chars are different in terms of diacritic signs"""

		if c1 in self.diacritics:
			if c2 == self.diacritics[c1]:
				return self.cost_diacritics
			else:
				return self.cost
		if c2 in self.diacritics:
			if c1 == self.diacritics[c2]:
				return self.cost_diacritics
			else:
				return self.cost
		return self.cost

	def _check_double_ortographical_error(self,s1,s2):
		"""Checks if a differences in a common ortographical error (i.e. ch -> h)"""
		if s1 in self.ortographical_errors_double:
			if s2 == self.ortographical_errors_double[s1]:
				return self.cost_ortographical
			else:
				return self.cost


		return self.cost

	def _check_single_ortographical_error(self,c1,c2):
		if c1 in self.ortographical_errors_single:
			if c2 == self.ortographical_errors_single[c1]:
				return self.cost_ortographical
			else:
				return self.cost
		if c2 in self.ortographical_errors_single:
			if c1 == self.ortographical_errors_single[c2]:
				return self.cost_ortographical
			else:
				return self.cost
		return self.cost


		

class DamerauLevenshteinDistance(LevenshteinDistance):
	""" This class takes into account two adjacent letters transposition and presents it as a operation. Note that Damerau-Levenshtein distance
		is not a metric (i.e. it does not satisfy triangle inequality)"""

	def check_damerau(self):
		pass

	def check_damerau_iterative(self,str1,str2):
		
		d = [[0 for j in xrange(len(str2)+1)] for i in xrange(len(str1)+1)]

		for i in xrange(len(str1)+1):
			d[i][0] = i
		for j in xrange(len(str2)+1):
			d[0][j] = j

		cost = self.cost

		for j in xrange(1,len(str2)+1):
			for i in xrange(1,len(str1)+1):
				if str1[i-1] == str2[j-1]:
					d[i][j] = d[i-1][j-1]
				else:
					d[i][j] = min(
						d[i-1][j]+cost,
						d[i][j-1]+cost,
						d[i-1][j-1]+self._check_diacritics(str1[i-1],str2[j-1]),
						d[i-1][j-1]+self._check_single_ortographical_error(str1[i-1],str2[j-1])
					)
				if i > 1 and j > 0:
					d[i][j] = min(
						d[i][j],
						d[i-2][j-1]+self._check_double_ortographical_error(str1[i-2:i],str2[j-1])	
					)
				if j > 1 and i > 0:
					d[i][j] = min(
						d[i][j],
						d[i-1][j-2]+self._check_double_ortographical_error(str2[j-2:j],str1[i-1])
					)
				
				if i > 1 and j > 1 and str1[i-2] == str2[j-1] and str2[j-2] == str1[i-1]:
					d[i][j] = min(d[i][j],d[i-2][j-2]+1) 


		return d[len(str1)][len(str2)]


if __name__ == '__main__':
	distance = DamerauLevenshteinDistance()
	s1 = unicode(sys.argv[1],"utf-8")
	s2 = unicode(sys.argv[2],"utf-8")
	#print distance.check(s1,s2)
	print distance.check_iterative(s1,s2)
	print distance.check_damerau_iterative(s1,s2)