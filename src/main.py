#!/usr/bin/python3.6
import sys
from QiitaAPIGenerater import QiitaAPIGenerater

def main(args):
	argle = len(args)
	#print(args)
	generator = QiitaAPIGenerater("../conf/access_setting.json")
	api = generator.get_qiita_api()
	print(api.get_own_all_datas())

if __name__ == '__main__':
	main(sys.argv)
