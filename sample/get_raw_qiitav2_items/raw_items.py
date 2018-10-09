#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, json
sys.path.append('../../src') 
from QiitaAPIMain import *

def main(args):
	print(json.dumps(QiitaAPIMain(['raw','raw_data.json','items']).action(), ensure_ascii=False, indent=4)) 

if __name__ == '__main__':
	main(sys.argv)
