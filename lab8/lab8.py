#!bin/python
# -*- coding: utf-8 -*-

import codecs, sys, re, math, random, logging, gensim, bz2
from collections import defaultdict
from gensim import corpora, models, similarities
from pprint import pprint

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

def process_documents(text_corpora_file, base_forms):
	file_split = re.split(r'#[0-9]{6}',codecs.open(text_corpora_file, encoding="utf-8").read().lower());

	stopwords = u"a, aby, ach, acz, aczkolwiek, aj, albo, ale, ależ, ani, aż, bardziej, bardzo, bo, bowiem, by, byli, bynajmniej, być, był, była, było, były, będzie, będą, cali, cała, cały, ci, cię, ciebie, co, cokolwiek, coś, czasami, czasem, czemu, czy, czyli, daleko, dla, dlaczego, dlatego, do, dobrze, dokąd, dość, dużo, dwa, dwaj, dwie, dwoje, dziś, dzisiaj, gdy, gdyby, gdyż, gdzie, gdziekolwiek, gdzieś, i, ich, ile, im, inna, inne, inny, innych, iż, ja, ją, jak, jakaś, jakby, jaki, jakichś, jakie, jakiś, jakiż, jakkolwiek, jako, jakoś, je, jeden, jedna, jedno, jednak, jednakże, jego, jej, jemu, jest, jestem, jeszcze, jeśli, jeżeli, już, ją, każdy, kiedy, kilka, kimś, kto, ktokolwiek, ktoś, która, które, którego, której, który, których, którym, którzy, ku, lat, lecz, lub, ma, mają, mało, mam, mi, mimo, między, mną, mnie, mogą, moi, moim, moja, moje, może, możliwe, można, mój, mu, musi, my, na, nad, nam, nami, nas, nasi, nasz, nasza, nasze, naszego, naszych, natomiast, natychmiast, nawet, nią, nic, nich, nie, niech, niego, niej, niemu, nigdy, nim, nimi, niż, no, o, obok, od, około, on, ona, one, oni, ono, oraz, oto, owszem, pan, pana, pani, po, pod, podczas, pomimo, ponad, ponieważ, powinien, powinna, powinni, powinno, poza, prawie, przecież, przed, przede, przedtem, przez, przy, roku, również, sama, są, się, skąd, sobie, sobą, sposób, swoje, ta, tak, taka, taki, takie, także, tam, te, tego, tej, temu, ten, teraz, też, to, tobą, tobie, toteż, trzeba, tu, tutaj, twoi, twoim, twoja, twoje, twym, twój, ty, tych, tylko, tym, u, w, wam, wami, was, wasz, wasza, wasze, we, według, wiele, wielu, więc, więcej, wszyscy, wszystkich, wszystkie, wszystkim, wszystko, wtedy, wy, właśnie, z, za, zapewne, zawsze, ze, zł, znowu, znów, został, żaden, żadna, żadne, żadnych, że, żeby".split(", ");

	def process_doc(doc):
		words = re.sub(r'[,.]','',doc)
		words = re.sub(r'[ ]{2}',' ',words)
		words = words.split()
		words = map(lambda x: base_forms[x] if x in base_forms else x, words)
		return words

	documents = [ process_doc(doc) for doc in file_split if doc != "" ]

	frequency = defaultdict(int)
	for doc in documents:
		for token in doc:
			frequency[token] += 1

	doc_words = [[token for token in doc if frequency[token] > 1 and token not in stopwords] for doc in documents]

	dictionary = corpora.Dictionary(doc_words)
	corpus = [dictionary.doc2bow(doc) for doc in documents]

	return (corpus, dictionary)


def build_LSA_model(corpus, dictionary,num_topics):
	lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=dictionary, num_topics=num_topics)
	return lsi

def build_LDA_model(corpus, dictionary,num_topics):
	lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=num_topics, update_every=0, passes=5)
	return lda

def find_N_docs_M_topics(index,doc,lsa,lda,corpora,N,M):
	doc_lsa = lda[doc] #lsa or lda
	sims = index[doc_lsa]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	sims = sims[:N]
	for s in sims:
		print "#### DOC ", s[0], "####"
		topics =  sorted(lsa[corpora[s[0]]], key=lambda item: -item[1])[:M]
		for t in topics:
			print lsa.show_topic(t[0])
		print "------------------------"




if __name__ == "__main__":
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	if (len(sys.argv) < 6):
		print sys.argv[0] + " BASE_FORMS_FILE TEXT_CORPORA_FILE NUM_DOCS NUM_TOPICS DOC_ID"
	else:
		#base_forms = process_base_forms(sys.argv[1])
		#corpus, dictionary = process_documents(sys.argv[2], base_forms)
		#dictionary.save('dict.dict')
		#corpora.MmCorpus.serialize('corpora.mm', corpus)
		mm = gensim.corpora.MmCorpus('corpora.mm')
		dictionary = corpora.Dictionary.load('dict.dict')
		#lsa = build_LSA_model(mm, dictionary, 100)
		#lda = build_LDA_model(mm, dictionary, 100)
		lsa = gensim.models.lsimodel.LsiModel.load('lsa.model');
		lda = gensim.models.ldamodel.LdaModel.load('lda.model');

		index = similarities.MatrixSimilarity(lda[mm])
		#index.save('lda.index');
		index = similarities.MatrixSimilarity.load('lsa.index')
		#lsa.save('lsa.model');
		#lda.save('lda.model');
		
		N = int(sys.argv[3])
		M = int(sys.argv[4])
		doc_id = int(sys.argv[5])
		doc = mm[doc_id]
		find_N_docs_M_topics(index,doc,lsa,lda,mm,N,M)

		
		#doc_id = 0
		#doc_bow = mm[0]

		#print lsa[doc_bow]
		#print lda[doc_bow]
		#lda.print_topics(10)
