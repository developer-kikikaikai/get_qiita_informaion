#Qiita API v2対応
import sys, json, requests
from QiitaAPI import *

class QiitaAPIv2(QiitaAPI):

	#v2 APIのベースURL
	BASEURL='https://qiita.com/api/v2/'
	#V2 APIの要素定義
	API_PROP_TITLE='title'
	API_PROP_ITEMID='id'
	API_PROP_VIEW='page_views_count'
	API_PROP_LIKE='likes_count'
	#stockだけはstockersの要素数をカウントする

	#内部で使うタグ
	TAG_HEADES='headers'
	TAG_BODY='body'

	def __init__(self, data):
		self._parse_setting(data)

	#private
	def _parse_setting(self, data):
		self._access_token = data['access_token']
		self._owndata={}
		self._headers={}
		if not 'get_owndata' in data or data['get_owndata'] != "yes":
			#自情報がいらないなら終了
			return

		#基本情報(自身の記事のitem, title)は取得してしまう
		self._headers['Authorization']=f'Bearer {data["access_token"]}'
		page=data['item_count']
		owndata=self._get_api_response_body(f'authenticated_user/items?page=1&per_page={page}')
		#必要な要素だけ取り出す。
		for itemdetail in owndata:
			#id毎に{'titlle', 'view', 'like', 'stock'}を設定する準備をしておく
			itemid=itemdetail[self.API_PROP_ITEMID]
			self._owndata[itemid]={}
			#titleはここで設定
			self._owndata[itemid][DEF_TITLE]=itemdetail[self.API_PROP_TITLE]
			#他の情報を取得
			self._set_own_item(itemid)

	#get response body
	def _get_api_response_body(self, extraurl):
		res=self._callapi(extraurl)
		res_body=json.loads(res.text)
		return res_body

	#qiita api call
	def _callapi(self, extraurl):
		url=self.BASEURL+extraurl
		try:
			res=requests.get(url, headers=self._headers)
			#正しい結果か？
			if not self._is_valid_response(res):
				sys.exit()

			return res
		except:
			print(f'Failed to get {url}')
			traceback.print_exc()
			sys.exit()

	#check response data
	def _is_valid_response(self, res):
		return res.status_code is 200
	
	def _get_view_and_like(self, item):
		result={}
		#view, likeはitemsの情報内から取得可能
		res=self._get_api_response_body(f'items/{item}')
		result[DEF_TITLE]=res[self.API_PROP_TITLE]
		result[DEF_VIEW]=res[self.API_PROP_VIEW]
		result[DEF_LIKE]=res[self.API_PROP_LIKE]
		return result

	def _get_stock(self, item):
		#stockはstockersから
		res=self._get_api_response_body(f'items/{item}/stockers')
		return len(res)

	#set own item information
	def _set_own_item(self, item):
		#view, いいねの取得
		view_and_like=self._get_view_and_like(item)
		self._owndata[item].update(view_and_like)

		#stock数の取得
		self._owndata[item][DEF_STOCK]=self._get_stock(item)

	def _get_data_after_init(self, item, key):
		#自分の記事は取得しているのでそこから
		if item in self._owndata:
			return {DEF_TITLE:self._owndata[item][DEF_TITLE], key:self._owndata[item][key]}

		#他の人の記事は取得だけ
		result=self._get_view_and_like(item)
		if key == DEF_STOCK:
			return {DEF_TITLE:result[DEF_TITLE], key:self._get_stock(item)}
		else:
			return {DEF_TITLE:result[DEF_TITLE], key:result[key]}

	#public
	# 自分のアカウントのitemsを取得する。
	# @ret list of items
	def get_own_items(self):
		return self._owndata.keys()	

	# 自分のアカウントの全情報を取得する
	# @ret dist of {itemid:{タイトル, 閲覧数, いいね数, ストック数}}
	def get_own_all_data(self):
		return self._owndata

	# itemの閲覧数を取得する
	# @ret {title, 閲覧数}
	def get_view(self, item):
		return self._get_data_after_init(item, DEF_VIEW)

	# ストック数を取得する
	# @ret {title, ストック数}
	def get_stock(self, item):
		return self._get_data_after_init(item, DEF_STOCK)

	# いいね数を取得する
	# @ret {title, いいね数}
	def get_like(self, item):
		return self._get_data_after_init(item, DEF_LIKE)

	# 特定記事の全情報を取得する
	# @ret {title, いいね数, ストック数, 閲覧数}
	def get_all_data_related_to_item(self, item):
		#自分の記事は取得しているのでそこから
		if item in self._owndata:
			return self._owndata[item]

		#他の人の記事は取得だけ
		result=self._get_view_and_like(item)
		result[DEF_STOCK]=self._get_stock(item)
		return result
