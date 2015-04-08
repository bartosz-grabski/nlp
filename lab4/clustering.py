#!/usr/bin/python
from metrics import Metrics
import collections
import re


class Preprocessor(object):

	def __init__(self):
		self.stop_list = """ph,inc,inc,limited,tel,fax,sp,j,mob,mr,attn,ul,st,co,ltd,z.o.o,t:,telephone,country,telefon,zip,zipcode,llc,code,phone,city,town,kod,pocztowy,contact,building,budynek,person,street,ctc,app,apartment,apartament""".split(",")
		self.replace_regex = r'[^a-z0-9]+'

	def preprocess(self,str1):

		#return re.sub(self.replace_regex,'',str1.lower())
		for stop_word in self.stop_list:
			split = split.replace(stop_word,'')
		return split.replace(':','').replace('+','').replace('-','').replace(',','').replace('/','').replace('.','')

class Clusterer(object):

	def __init__(self,filename,metric,ngram_generator):
		self.filename = filename
		self.metric = metric
		self.ngram_generator = ngram_generator
		self.threshold = 0.3

	def _preprocess(self,filename):
		preprocessor = Preprocessor()
		f = file(filename).readlines()

		preprocessed = []
		clusters = 0


		for line in f:
			pr = preprocessor.preprocess(line)
			preprocessed.append([line,pr,self.ngram_generator(pr),clusters])
			clusters += 1
		
		self.preprocessed = preprocessed
		print "Processing finished..."

	def clusterize(self):
		self._preprocess(self.filename)
		clusters = []
		#print self.preprocessed
		i = 0
		for x in self.preprocessed:
			#print i
			closest_cluster = None
			closest = 1.0
			for y in clusters:
				dist = self.metric(x[2],y[0][2])
				if dist < closest and dist < self.threshold:
					closest = dist
					closest_cluster = y
			if closest_cluster == None:
				clusters.append([x,[]])
			else:
				closest_cluster[1].append(x)

		self.clusters = clusters
		return clusters

	def print_to_file(self):
		out = open('my_clusters.txt','w')

		for cluster in self.clusters:
			out.write(cluster[0][0])
			for elements in cluster[1]:
				out.write(elements[0])
			out.write("\n")


	def _reassign(self,source_cluster,target_cluster):
		for x in self.preprocessed:
			if x[2] == source_cluster:
				x[2] = target_cluster

if __name__ == "__main__":
	metrics = Metrics(3)
	c = Clusterer("lines.txt",metrics.ngram_dice,metrics.generate_ngrams)
	c.clusterize()
	c.print_to_file()
	
