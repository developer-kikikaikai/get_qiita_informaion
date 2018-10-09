#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, json
sys.path.append('../../src') 
from QiitaAPIMain import *

def main(args):
	print(json.dumps(QiitaAPIMain(['own','item_infos.json','user_items']).action(), ensure_ascii=False, indent=4)) 

if __name__ == '__main__':
	main(sys.argv)
