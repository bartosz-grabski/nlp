#!/usr/bin/python
# -*- coding: utf-8 -*-


import codecs, sys, re, collections

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def main():
	morfo_out_file = sys.argv[1]
	normal_out_file = sys.argv[2]
	file_split = codecs.open(morfo_out_file, encoding="utf-8").read().split('\t')

	print file_split

	



if __name__ == "__main__":
	main()

