#!/usr/bin/python3.6
#QiitaAPIをロード
import sys, os, re, nltk
sys.path.append('../../src') 
from QiitaAPIMain import *

def replase_name(ustr):
	#記号、改行排除
	text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', ustr)
	text = re.sub(r'[\n|\r|\t]', '', text)

	#日本語以外の文字も排除
	jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([a-z]+|[A-Z]+|[ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')
	text = "".join(jp_chartype_tokenizer.tokenize(text))

	return text

def writeFile(name, mddata):
	with open(name, 'w') as f:
		f.write(mddata)

def main(args):
	markdowns=QiitaAPIMain(['backup','only_markdown.json','user_items']).action()
	for item, result in markdowns.items():
		name=replase_name(result['title'])[:30]+"_"+str(item)+".md"
		#ファイル名長制限
		writeFile(name, result['markdown'])

if __name__ == '__main__':
	main(sys.argv)
