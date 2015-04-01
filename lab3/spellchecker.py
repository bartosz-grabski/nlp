#!/usr/bin/python
# -*- coding: utf-8 -*-
from levenshtein_distance import DamerauLevenshteinDistance
import collections, re
import sys
import codecs

alphabet = u'ąśćńółężźabcdefghijklmnopqrstuvwxyz'

def _words(text): 
	return re.findall('\w+', text.lower(), re.UNICODE) 

def _train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def create_dictionary():
	return _train(_words(codecs.open('popul.iso.utf8',encoding="utf-8").read() + codecs.open('publ.iso.utf8',encoding="utf-8").read() + codecs.open('proza.iso.utf8',encoding="utf-8").read() + codecs.open('dramat.iso.utf8',encoding="utf-8").read() + codecs.open('wp.iso.utf8',encoding="utf-8").read()))

NWORDS = create_dictionary();

def known_edits1(word):
	return set(e1 for e1 in edits1(word) if e1 in NWORDS)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known_edits3(word):
	return set(e2 for e1 in known_edits2(word) for e2 in edits1(e1) if e2 in NWORDS)

def build_statistics():
	distance = DamerauLevenshteinDistance()
	f = codecs.open('bledy.txt',encoding="utf-8")
	model = collections.defaultdict(lambda: 1)
	for a in f:
		s = a.split(u';');
		dist = distance.check_damerau_iterative(s[0],s[1])
		model[dist] += 1
		model['all'] += 1.0

	return model

stats = build_statistics()
edits = [ (1,known_edits1),(2,known_edits2),(3,known_edits3)]
edits = sorted(edits, key=lambda x: stats[x[0]], reverse=True)

print stats
print edits

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)



def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word])
    if (len(candidates) != 0):
    	return word
    else:
    	for el in edits:
    		candidates = candidates.union(map(lambda x: (el[0],x),el[1](word)))
    if (len(candidates) == 0):
    	candidates = [(0,word)]
    #print candidates
    return max(candidates,key=lambda x: stats[x[0]]/stats['all'] * NWORDS[x[1]])[1]

#print(correct('asd'))
#print NWORDS['chalogenoxa']


#errs = codecs.open('bledy.txt',encoding="utf-8")
#for l in errs.readlines():
#	s = l.split(u';')
#	print s[0], correct(s[0])[1]

print correct(raw_input('>>>'))
