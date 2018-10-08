#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, json, time
sys.path.append('../../src') 
from QiitaAPIMain import *

def main(args):
	starttime=time.perf_counter()
	print(json.dumps(QiitaAPIMain(['own','item_infos.json','user_items']).action(), ensure_ascii=False, indent=4)) 
	endtime=time.perf_counter()
	print("End to get items: time={:.7f}".format(endtime - starttime))

if __name__ == '__main__':
	main(sys.argv)
