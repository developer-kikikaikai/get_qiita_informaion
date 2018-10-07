#!/usr/bin/python3.6
import sys
from QiitaAPIMain import QiitaAPIMain

def main(args):
	main_instance=QiitaAPIMain(args)
	main_instance.action()

if __name__ == '__main__':
	main(sys.argv)
