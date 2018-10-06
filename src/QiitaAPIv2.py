#Qiita API v2対応
import sys, json, requests
from QiitaAPI import QiitaAPI

BASEURL='https://qiita.com/api/v2/'
class QiitaAPIv2(QiitaAPI):

	def __init__(self, data):
		self._parse_setting(data)

	#private
	def _parse_setting(self, data):
		self._access_token = data['access_token']
		if not 'get_owndata' in data or data['get_owndata'] != "yes":
			#自情報がいらないなら終了
			return

		#基本情報(自身の記事のitem, title)は取得してしまう
		self._headers={'Authorization': f'Bearer {data["access_token"]}'}
		page=data['item_count']
		owndata=self._get_api_response_body(f'authenticated_user/items?page=1&per_page={page}')
		self._owndata={}
		#必要な要素だけ取り出す。
		for itemdetail in owndata:
			#id毎に{'titlle', 'view', 'like', 'stock'}を設定する準備をしておく
			itemid=itemdetail['id']
			self._owndata[itemid]={}
			#titleはここで設定
			self._owndata[itemid]['title']=itemdetail['title']
			#他の情報を取得
			self._set_own_item(itemid)

	#get response body
	def _get_api_response_body(self, extraurl):
		res=self._callapi(extraurl)
		return res['body']

	#get response header
	def _get_api_response_headers(self, extraurl):
		res=self._callapi(extraurl)
		return res['headers']

	#qiita api call
	def _callapi(self, extraurl):
		url=BASEURL+extraurl
		try:
			res=requests.get(url, headers=self._headers)
			#正しい結果か？
			if not self._is_valid_response(res):
				sys.exit()

			res_body=json.loads(res.text)
			return {'headers':res.headers, 'body':res_body}
		except:
			print(f'Failed to get {url}')
			traceback.print_exc()
			sys.exit()

	#check response data
	def _is_valid_response(self, res):
		return res.status_code is 200
	
	def _get_view_and_like(self, item):
		result={}
		res=self._get_api_response_body(f'items/{item}')
		result['view']=res['page_views_count']
		result['like']=res['likes_count']
		return result

	def _get_stock(self, item):
		res=self._get_api_response_headers(f'items/{item}/stockers')
		return res.get('Total-Count')

	#set own item information
	def _set_own_item(self, item):
		#view, いいねの取得
		view_and_like=self._get_view_and_like(item)
		self._owndata[item].update(view_and_like)

		#stock数の取得
		self._owndata[item]['stock']=self._get_stock(item)

	def _get_data_after_init(self, item, key):
		#自分の記事は取得しているのでそこから
		if item in self._owndata:
			return self._owndata[item][key]
		#他の人の記事は取得だけ
		if key == 'stock':
			return self._get_stock(item)
		else:
			return self._get_view_and_like[key]

	#public
	# 自分のアカウントのitemsを取得する。
	# @ret list of items
	def get_own_items(self):
		return self._owndata.keys()	

	# 自分のアカウントの全情報を取得する
	# @ret {itemid:{タイトル, 閲覧数, いいね数, ストック数}}
	def get_own_all_datas(self):
		return self._owndata

	# itemの閲覧数を取得する
	# @ret 閲覧数
	def get_view(self, item):
		self._get_data_after_init(item, 'view')

	# ストック数を取得する
	# @ret ストック数
	def get_stock(self, item):
		self._get_data_after_init(item, 'stock')

	# いいね数を取得する
	# @ret いいね数
	def get_like(self, item):
		self._get_data_after_init(item, 'like')
