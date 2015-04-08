#!/usr/bin/python

#ugly as hell calculating of recall,precision and f1
class Comparator(object):

	def load_clusters(self,filename1,filename2):
		file1 = open(filename1)
		file2 = open(filename2)
		cluster = 0
		clusters1 = {}
		clusters2 = {}
		for line in file1.readlines():
			line = line.strip()
			if line.startswith('#####'):
				cluster += 1
			elif line != "":
				clusters1[line] = cluster
				if cluster in clusters1:
					clusters1[cluster].append(line)
				else:
					clusters1[cluster] = []
					clusters1[cluster].append(line)
		cluster = 0
		for line in file2.readlines():
			line = line.strip()
			if line == "":
				cluster += 1
			else:
				clusters2[line] = cluster
				if cluster in clusters2:
					clusters2[cluster].append(line)
				else:
					clusters2[cluster] = []
					clusters2[cluster].append(line)
		
		self.clusters1 = clusters1
		self.clusters2 = clusters2
		return clusters1, clusters2

	def calculate_recall(self):
		true_positives = 0.0
		denominator = 0.0
		counted = []

		for key in self.clusters2:
			if type(key) is not int:
				cluster2number = self.clusters2[key]
				cluster1number = self.clusters1[key]
				if cluster2number not in counted:
					for element2 in self.clusters2[cluster2number]:
						if self.clusters1[element2] == cluster1number:
							true_positives += 1
					counted.append(cluster2number)
					denominator += len(self.clusters1[cluster1number])

		self.recall = true_positives/denominator
		return self.recall

	def calculate_precision(self):
		true_positives = 0.0
		denominator = 0.0
		counted = []
		for key in self.clusters2:
			if type(key) is not int:
				cluster2number = self.clusters2[key]
				cluster1number = self.clusters1[key]
				if cluster2number not in counted:
					for element2 in self.clusters2[cluster2number]:
						if self.clusters1[element2] == cluster1number:
							true_positives += 1
					counted.append(cluster1number)
					denominator += len(self.clusters2[cluster2number])
		self.precision = true_positives/denominator
		return self.precision



	def calculate_f1(self):
		self.f1 = 2 * (self.recall * self.precision)/(self.recall + self.precision)
		return self.f1



if __name__ == "__main__":
	c = Comparator()
	c.load_clusters('clusters.txt','my_clusters.txt')
	print c.calculate_precision()
	print c.calculate_recall()
	print c.calculate_f1()