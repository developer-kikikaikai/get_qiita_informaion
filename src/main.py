#!/usr/bin/python3.6
import sys, json
from QiitaAPIMain import QiitaAPIMain

def show(data):
	print(json.dumps(data, ensure_ascii=False, indent=4))

def main(args):
	main_instance=QiitaAPIMain(args)
	show(main_instance.action())

if __name__ == '__main__':
	main(sys.argv)
