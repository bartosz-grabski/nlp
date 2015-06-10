#!/usr/bin/python
# -*- coding: utf-8 -*-


import codecs, sys, re, collections

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def main():
	text_corpora_file = sys.argv[1]
	prepositions = sys.argv[2:]
	file_split = re.split(r' ',codecs.open(text_corpora_file, encoding="utf-8").read().lower());

	prep_words = {}

	for preposition in prepositions:
		prep_words[preposition] = {}

		for i in xrange(len(file_split) - 1):
			if file_split[i] == preposition:
				next = file_split[i+1]
				if next in prep_words[preposition]:
					prep_words[preposition][next] += 1
				else:
					prep_words[preposition][next] =1

	for preposition in prep_words:
		words = prep_words[preposition]
		words = sorted(words,key=lambda x: prep_words[preposition][x], reverse=True)[:10]

		print preposition, ' '.join(words)



if __name__ == "__main__":
	main()

