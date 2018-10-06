#!/usr/bin/python3.6
import sys
from MainAction import MainAction

def main(args):
	main_instance=MainAction(args)
	main_instance.action()

if __name__ == '__main__':
	main(sys.argv)
