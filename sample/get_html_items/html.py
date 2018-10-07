#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, re
sys.path.append('../../src') 
from QiitaAPIMain import *

def replase_name(ustr):
	#記号、改行排除
	text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', ustr)
	text = re.sub(r'[\n|\r|\t]', '', text)

	return text

def writeFile(name, mddata):
	with open(name, 'w') as f:
		f.write(mddata)

def main(args):
	#headerを適当に
	htmls=QiitaAPIMain(['html','only_html.json','items']).action()
	for item, result in htmls.items():
		html_str='<!DOCTYPE html><html><meta charset="utf-8" />'
		title_res=replase_name(result['title'])
		html_str+=f'<head><title>{title_res}'
		html_str+='</title></head><body>'
		html_str+=f'<h1 class="it-Header_title" itemprop="headline">{title_res}</h1>'
		#ファイル名長制限
		html_str+=result['html']
		html_str+='</body></html>'
		writeFile(f"qiita_{item}.html", html_str)

if __name__ == '__main__':
	main(sys.argv)
