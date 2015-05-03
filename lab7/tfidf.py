#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections, codecs, sys, re, math, random

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

def create_tfidf_dict(base_forms,text_corpora_file):
	file_split = re.split(r'#[0-9]{6}',codecs.open(text_corpora_file, encoding="utf-8").read().lower());
	tf = collections.defaultdict(lambda : collections.defaultdict(lambda: 0))
	df = collections.defaultdict(lambda: 0)
	doc_lengths_squared = collections.defaultdict(lambda: 0)
	tfidf = collections.defaultdict(lambda : collections.defaultdict(lambda: 0))
	document_count = 0
	doc_id = 0;
	for doc in file_split:
		if doc != "":
			doc_id += 1
			document_count += 1
			words = re.sub(r'[,.]','',doc)
			words = re.sub(r'[ ]{2}',' ',words)
			words = words.split()
			words = map(lambda x: base_forms[x] if x in base_forms else x, words)
			words = collections.Counter(words)
			for word in words:
				tf[word][doc_id] += words[word]
				df[word] += 1

	document_count -= 1

	for term in tf:
		for doc in tf[term]:
			tfidf[term][doc] = tf[term][doc] * math.log(float(document_count)/df[term])
			doc_lengths_squared[doc] += tfidf[term][doc] * tfidf[term][doc] 

	return (tfidf, document_count, df, doc_lengths_squared) 

def generate_keywords(tfidf, threshold, file_out, document_count):
	print "Generating keywords", threshold
	doc_count = len(tfidf[random.choice(tfidf.keys())])
	f_out = codecs.open(file_out,"w",encoding="utf-8");
	for doc in xrange(1,document_count+1):
		f_out.write("#"+str(doc)+"\n")
		max_tfidf_doc_value = 0
		for term in tfidf:
			if tfidf[term][doc] > max_tfidf_doc_value:
				max_tfidf_doc_value = tfidf[term][doc]

		for term in tfidf:
			if tfidf[term][doc] > threshold * max_tfidf_doc_value:
				f_out.write(term+"\n")

	f_out.close()

def find_matching_by_words(tfidf, base_forms, words, document_count, df, doc_lengths_squared):
	words = re.sub(r'[,.]','',words.lower())
	words = re.sub(r'[ ]{2}',' ',words)
	words = words.split()
	words = map(lambda x: base_forms[x] if x in base_forms else x, words)
	words = collections.Counter(words)
	max_value_doc_id = -1
	max_value = 0.0
	for doc_id in xrange(1,document_count+1):
		value = 0.0
		squared_weights = 0.0
		for word in words:
			weight = words[word] * math.log(float(document_count)/(df[word] if df[word] > 0 else 1))
			value += tfidf[word][doc_id] * weight
			squared_weights += weight*weight
		
		value /= math.sqrt(doc_lengths_squared[doc_id])*math.sqrt(squared_weights)
		if value > max_value:
			max_value = value
			max_value_doc_id = doc_id

	return (max_value_doc_id, max_value)


def find_similar_doc(tfidf, chosen_doc_id, doc_lengths_squared):

	words = []
	for term in tfidf:
		if tfidf[term][chosen_doc_id] > 0.0:
			words.append(term)
	max_value = 0.0
	max_value_doc_id = -1
	doc_squared_length = doc_lengths_squared[chosen_doc_id]
	for doc_id in xrange(1,document_count+1):
		if doc_id != chosen_doc_id:
			value = 0.0
			for word in words:
				value += tfidf[word][doc_id] * tfidf[word][chosen_doc_id]
			
			value /= math.sqrt(doc_lengths_squared[doc_id])*math.sqrt(doc_squared_length)
			if value > max_value:
				max_value = value
				max_value_doc_id = doc_id

	return (max_value_doc_id, max_value)

if __name__ == "__main__":
	if (len(sys.argv) < 3):
		print sys.argv[0] + " BASE_FORMS_FILE TEXT_CORPORA_FILE"
	base_forms = process_base_forms(sys.argv[1])
	tfidf, document_count, df, doc_lengths = create_tfidf_dict(base_forms,sys.argv[2])
	t = "words"
	#generate_keywords(tfidf, 0.9, "keywords.txt", document_count);
	s = raw_input('>>>'+t+':')
	while s != "":
		if s == "words":
			t = "words"
		elif s == "docs":
			t = "docs"
		else:
			if t == "docs":
				try:
					print find_similar_doc(tfidf,int(s),doc_lengths)
				except ValueError:
					print "Doc id should be an integer"
			else:
				print find_matching_by_words(tfidf, base_forms, s, document_count, df, doc_lengths)
		s = raw_input('>>>'+t+':')
		
