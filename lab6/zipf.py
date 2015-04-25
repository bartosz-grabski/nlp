#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs, collections, re

class ZipfMandelbrot():


	def __init__(self):
		pass

	def process_text_corpus(self,base_forms_file, text_corpus_file):
		"""UTF-8"""
		f = codecs.open(base_forms_file, encoding="utf-8").readlines()
		base_forms = {}
		for line in f:
			split = line.split(',')
			if len(split) > 1:
				for el in split[1:]:
					base_forms[el.strip()] = split[0]
			else:
				base_forms[split[0]] = split[0]

		f = codecs.open(text_corpus_file, encoding="utf-8").read().lower()
		text = re.sub(u'[^a-zA-Z0-9ąęćńółżź]+', " ", f)
		split = text.split()
		stats = collections.defaultdict(lambda : 0)
		for el in split:
			if (el in base_forms):
				stats[base_forms[el]] += 1
			else:
				stats[el] += 1

		stats_list = []
		for el in stats:
			stats_list.append((el,stats[el]))

		stats_list = sorted(stats_list, key=lambda x: x[1], reverse=True)
		return stats_list

	def create_graph_data(self,sorted_list):
		graph_data_file = codecs.open('graph_data.csv','w', encoding="utf-8");
		rank = 1
		for el in sorted_list:
			csv = u",".join([str(rank), el[0], unicode(str(el[1]),"utf-8")])
			graph_data_file.write(csv+"\n")
			rank += 1

	def count_hapax_legomena(self,sorted_list):
		return reduce(lambda x,y: x+y[1],filter(lambda x: x[1] == 1,sorted_list),0)

	def count_50_percent(self,stats):
		allwords = reduce(lambda x,y: x + y[1], stats,0.0)
		percent = 0.0
		included = 0.0
		base_forms_included = 0
		while percent < 0.5:
			included += stats[base_forms_included][1]
			base_forms_included += 1
			percent = included / allwords

		return base_forms_included
			




z = ZipfMandelbrot()
rank = z.process_text_corpus('odm.txt','potop.txt')
z.create_graph_data(rank)
print z.count_hapax_legomena(rank)
print z.count_50_percent(rank)



