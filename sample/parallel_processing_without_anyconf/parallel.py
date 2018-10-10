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

def call_items(obj):
	result=QiitaAPIMain(['html',obj,'items']).action()
	writeFile(f"page_{obj['data']['show']['item']['page']}.txt", json.dumps(result, ensure_ascii=False, indent=4))

#5プロセスで5000item取得を目指す。
def main(args):
	with open('pagenation_parallel.json') as f:
		conf=json.loads(f.read())
	print(conf)
	for n in range(0,5):
		multiprocessing.Process(target=call_items,args=([conf])).start()
		conf['data']['show']['item']['page']+=10

if __name__ == '__main__':
	main(sys.argv)
