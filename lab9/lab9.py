#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs, sys, re, collections

def process_base_forms(base_forms_file):
	f = codecs.open(base_forms_file, encoding="utf-8").readlines()
	base_forms = {}
	for line in f:
		split = line.split(',')
		if len(split) > 1:
			for el in split[1:]:
				base_forms[el.strip()] = split[0]
		else:
			base_forms[split[0]] = split[0]

	return base_forms

def process_documents(text_corpora_file, base_forms_file, k):

	base_forms = process_base_forms(base_forms_file)

	file_split = re.split(r'#[0-9]{6}',codecs.open(text_corpora_file, encoding="utf-8").read().lower());

	stopwords = u"a, aby, ach, acz, aczkolwiek, aj, albo, ale, ależ, ani, aż, bardziej, bardzo, bo, bowiem, by, byli, bynajmniej, być, był, była, było, były, będzie, będą, cali, cała, cały, ci, cię, ciebie, co, cokolwiek, coś, czasami, czasem, czemu, czy, czyli, daleko, dla, dlaczego, dlatego, do, dobrze, dokąd, dość, dużo, dwa, dwaj, dwie, dwoje, dziś, dzisiaj, gdy, gdyby, gdyż, gdzie, gdziekolwiek, gdzieś, i, ich, ile, im, inna, inne, inny, innych, iż, ja, ją, jak, jakaś, jakby, jaki, jakichś, jakie, jakiś, jakiż, jakkolwiek, jako, jakoś, je, jeden, jedna, jedno, jednak, jednakże, jego, jej, jemu, jest, jestem, jeszcze, jeśli, jeżeli, już, ją, każdy, kiedy, kilka, kimś, kto, ktokolwiek, ktoś, która, które, którego, której, który, których, którym, którzy, ku, lat, lecz, lub, ma, mają, mało, mam, mi, mimo, między, mną, mnie, mogą, moi, moim, moja, moje, może, możliwe, można, mój, mu, musi, my, na, nad, nam, nami, nas, nasi, nasz, nasza, nasze, naszego, naszych, natomiast, natychmiast, nawet, nią, nic, nich, nie, niech, niego, niej, niemu, nigdy, nim, nimi, niż, no, o, obok, od, około, on, ona, one, oni, ono, oraz, oto, owszem, pan, pana, pani, po, pod, podczas, pomimo, ponad, ponieważ, powinien, powinna, powinni, powinno, poza, prawie, przecież, przed, przede, przedtem, przez, przy, roku, również, sama, są, się, skąd, sobie, sobą, sposób, swoje, ta, tak, taka, taki, takie, także, tam, te, tego, tej, temu, ten, teraz, też, to, tobą, tobie, toteż, trzeba, tu, tutaj, twoi, twoim, twoja, twoje, twym, twój, ty, tych, tylko, tym, u, w, wam, wami, was, wasz, wasza, wasze, we, według, wiele, wielu, więc, więcej, wszyscy, wszystkich, wszystkie, wszystkim, wszystko, wtedy, wy, właśnie, z, za, zapewne, zawsze, ze, zł, znowu, znów, został, żaden, żadna, żadne, żadnych, że, żeby".split(", ");

	def process_doc(doc, k, doc_id, graph):
		words = re.sub(r'[,.]','',doc)
		words = re.sub(r'[ ]{2}',' ',words)
		words = words.split()
		words = map(lambda x: base_forms[x] if x in base_forms else x, words)
		words = filter(lambda x: x not in stopwords, words)

		for i in xrange(len(words) - k - 1):
			two_gram = words[i] + "###" + words[i+k+1] 
			if two_gram in graph:
				if doc_id in graph[two_gram]:
					graph[two_gram][doc_id] += 1
				else:
					graph[two_gram][doc_id] = 1
			else:
				graph[two_gram] = {}
				graph[two_gram][doc_id] = 1

			if doc_id in graph:
				if two_gram not in graph[doc_id]:
					graph[doc_id][two_gram] = True
			else:
				graph[doc_id] = {}
				graph[doc_id][two_gram] = True

	graph = {}
	doc_id = 1

	for doc in file_split:
		if doc != "":
			process_doc(doc,k, doc_id, graph)
			doc_id += 1

	graph["size"] = doc_id
	return graph

def find_similar(documents_ids, n, graph):
	similarities = {}
	for doc_id in documents_ids:
		d_id = int(doc_id)
		sim = {}
		for edge in graph[d_id]:
			for doc_id_vec in graph[edge]:
				if doc_id_vec in sim:
					sim[doc_id_vec] += graph[edge][doc_id_vec] * graph[edge][d_id] 
				else:
					sim[doc_id_vec] = graph[edge][doc_id_vec] * graph[edge][d_id] 

		score = []

		for doc_id in sim:
			s = 0.0
			for edge in graph[doc_id]:
				s += graph[edge][doc_id]
			final_score = sim[doc_id] / s
			score.append((doc_id,final_score))

		similarities[d_id] = sorted(score,key=lambda x: -x[1])[:n]	

	return similarities


if __name__ == "__main__":
	docs = [ x for x in xrange(1000,1010)]
		
	for k in xrange(4):
		print "####",k,"####"
		graph = process_documents(sys.argv[1], sys.argv[2],k)
		sim = find_similar(docs, 10, graph)
		print sim

	