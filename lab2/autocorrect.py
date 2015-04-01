#!/usr/bin/python
# -*- coding: utf-8 -*-
from levenshtein_distance import DamerauLevenshteinDistance


def build_dictionary():
	f = open('pocz.dat').read().split();
	f = map(lambda x : x.split(':') if ":" in x else [x,0]  ,f)
	f = sorted(f, key=lambda x: int(x[1]))


def check_smart():
	to_correct = raw_input('>>>')
	


def check_brute():
	d = DamerauLevenshteinDistance()
	to_correct = raw_input('>>>')
	f = open('formy.txt').read().split()
	min_dist = 10000.0
	w = ''
	for word in f:
		val = d.check_damerau_iterative(word,to_correct)
		if val < min_dist:
			min_dist = val
			w = word

	print min_dist,w


if __name__ == "__main__":
	build_dictionary()
	#check_brute()
	check_smart()
	