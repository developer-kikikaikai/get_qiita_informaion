#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, json
sys.path.append('../../src') 
from QiitaAPIMain import *
#multi process
import multiprocessing

def writeFile(name, mddata):
	with open(name, 'w') as f:
		f.write(mddata)

def call_items(index):
	result=QiitaAPIMain(['html',f'pagenation_parallel_{index}.json','items']).action()
	writeFile(f'page_{index}_plus_10.txt', json.dumps(result, ensure_ascii=False, indent=4))

#5プロセスで5000item取得を目指す。
def main(args):
	for n in range(1,6):
		multiprocessing.Process(target=call_items,args=([n])).start()

if __name__ == '__main__':
	main(sys.argv)
