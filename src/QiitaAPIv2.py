#Qiita API v2対応
import sys, json, requests
from QiitaAPI import *

class QiitaAPIv2(QiitaAPI):

	#v2 APIのベースURL
	BASEURL='https://qiita.com/api/v2/'
	#V2 APIの要素定義
	API_PROP_TITLE='title'
	API_PROP_ITEMID='id'
	API_PROP_URL='url'
	API_PROP_TAGS='tags'
	API_PROP_USER='user'
	API_PROP_VIEW='page_views_count'
	API_PROP_LIKE='likes_count'
	API_PROP_HTML='rendered_body'
	API_PROP_MARKDOWN='body'
	API_PROP_CREATE_TIME='created_at'
	API_PROP_UPDATE_TIME='updated_at'
	API_PROP_PAGE='page'
	API_PROP_PER_PAGE='per_page'
	#stockだけはstockersの要素数をカウントする
	API_PROP_STOCK='stock'

	#V2のアクセス仕様上限
	API_PAGE_MAX=100
	API_PAGE_ITEM_MAX=100

	#内部で使うタグ
	#conf設定。ここ以外の各要素はoutputに使うので、QiitaAPIと合わせる
	CONF_PROP_SHOW='show'
	CONF_PROP_ITEM='item'
	CONF_PROP_USER=QiitaAPI.COMMON_USER
	CONF_PROP_TOKEN='access_token'
	#内部情報管理用
	MNG_PROP_SHOW='show'
	MNG_PROP_HAVE_LIST='have_list'
	MNG_PROP_API_PROP='property'
	#http header parse
	HTTP_PROP_HEADER='header'
	HTTP_PROP_LINK='Link'
	HTTP_PROP_COUNT='Total-Count'
	HTTP_PROP_BODY='body'

	#private
	def _parse_setting(self, data):
		#デフォルトを設定
		self._set_default()
		print(json.dumps(self._item_config, ensure_ascii=False, indent=4))

		#認証設定
		if self.CONF_PROP_TOKEN in data:
			token=data[self.CONF_PROP_TOKEN]
			self._headers['Authorization']=f'Bearer {token}'

		#ユーザー名設定
		if QiitaAPI.ITEM_USER in data:
			self._user=data[QiitaAPI.ITEM_USER]

		#show関連のデータがないならデフォルトをそのまま使う
		if not self.MNG_PROP_SHOW in data:
			return

		#item関連の設定更新
		self._set_item_config(data[self.MNG_PROP_SHOW])

		#user関連の設定更新
		self._set_user_config(data[self.MNG_PROP_SHOW])

		print(json.dumps(self._item_config, ensure_ascii=False, indent=4))

	#デフォルト設定を行う
	def _set_default(self):
		#デフォルトを設定
		self._headers={}
		#item関連
		self._item_config={
				self.API_PROP_PAGE:1,
				self.API_PROP_PER_PAGE:100,
				QiitaAPI.ITEM_RAW:False,
				#itemは{responseキー:{表示するか, 一覧取得で取得可能か, IDの対応}}
				self.CONF_PROP_ITEM:{
					self.API_PROP_TITLE:	{self.MNG_PROP_SHOW:True , self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_TITLE},
					self.API_PROP_URL:		{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_URL},
					self.API_PROP_TAGS:		{self.MNG_PROP_SHOW:True , self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_TAGS},
					self.API_PROP_MARKDOWN :{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_MARKDOWN_DATA},
					self.API_PROP_HTML:		{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_HTML_DATA},
					self.API_PROP_CREATE_TIME:	{self.MNG_PROP_SHOW:False , self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_CREATED_AT},
					self.API_PROP_UPDATE_TIME:	{self.MNG_PROP_SHOW:False , self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_UPDATED_AT},
					self.API_PROP_UPDATE_TIME:	{self.MNG_PROP_SHOW:False , self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_UPDATED_AT},
					self.API_PROP_VIEW:		{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:False, self.MNG_PROP_API_PROP:QiitaAPI.ITEM_VIEW},
					self.API_PROP_USER:		{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:True, self.MNG_PROP_API_PROP:QiitaAPI.ITEM_USER},
					self.API_PROP_LIKE:		{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:True , self.MNG_PROP_API_PROP:QiitaAPI.ITEM_LIKE},
					self.API_PROP_STOCK:	{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:False, self.MNG_PROP_API_PROP:QiitaAPI.ITEM_STOCK}
				}
		}

		#user関連
		self._user_config={
				self.API_PROP_PAGE:1,
				self.API_PROP_PER_PAGE:100,
				QiitaAPI.ITEM_RAW:False,
				self.CONF_PROP_USER:{
					#itemは{responseキー:{表示するか, IDの対応}}
					self.API_PROP_ITEMID:	{self.MNG_PROP_SHOW:True, self.MNG_PROP_API_PROP:QiitaAPI.USER_ID}
				}
		}

	#item周りの設定更新を行う
	def _set_item_config(self, show_data):
		#itemがないならデフォルトで
		if not self.CONF_PROP_ITEM in show_data:
			return

		for key, value in show_data[self.CONF_PROP_ITEM].items():
			#item要素以外はそのまま代入
			if key in self._item_config:
				if key != self.CONF_PROP_ITEM:
					self._item_config[key]=value
			#それ以外はconfigテーブルの表示に関して更新する	
			else:
				self._update_item_config(key, value)

	#item_configの更新を行う
	def _update_item_config(self, key, value):
		self._update_show_config(key, value, self._item_config[self.CONF_PROP_ITEM])

	#user周りの更新を行う
	def _set_user_config(self, show_data):
		#userがないならデフォルトで
		if not self.CONF_PROP_USER in show_data:
			return

		for key, value in show_data[self.CONF_PROP_USER].items():
			#item要素はそのまま代入
			if key in self._user_config:
				if key != self.CONF_PROP_USER:
					self._user_config[key]=value
			#それ以外はconfigテーブルの表示に関して更新する	
			else:
				self._update_user_config(key, value)

	#user_configの更新を行う
	def _update_user_config(self, key, value):
		self._update_show_config(key, value, self._user_config[self.CONF_PROP_USER])

	#item_configの更新を行う
	def _update_show_config(self, key, value, config):
		#正しいkey, valueじゃないなら無視
		if type(value) is not bool:
			return

		for index, tables in config.items():
			if tables[self.MNG_PROP_API_PROP] == key:
				#アップデート
				config[index][self.MNG_PROP_SHOW]=value
				break

	#get response body
	def _get_api_response_body(self, extraurl):
		res=self._callapi(extraurl)
		#print(res.headers)
		res_body=json.loads(res.text)
		return res_body

	#get response all
	def _get_api_response_all(self, extraurl):
		res=self._callapi(extraurl)
		res_all={self.HTTP_PROP_HEADER:res.headers}
		res_all[self.HTTP_PROP_BODY]=json.loads(res.text)
		return res_all

	#qiita api call
	def _callapi(self, extraurl):
		url=self.BASEURL+extraurl
		try:
			print(url)
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

	#get user raw result
	def _get_user_items_by_api(self):
		query=f'page={self._item_config[self.API_PROP_PAGE]}&per_page={self._item_config[self.API_PROP_PER_PAGE]}'
		if hasattr(self, '_user'): 
			url=f'users/{self._user}/items?{query}'
		else :
			url=f'authenticated_user/items?{query}'
		#view, likeはitemsの情報内から取得可能
		return self._get_api_response_body(url)

	#get items raw result
	def _get_items_by_api(self):
		#view, likeはitemsの情報内から取得可能
		return self._get_api_response_body('items')

	#get_itemの生データ取得
	def _get_item_by_api(self, item):
		return self._get_api_response_body(f'items/{item}')

	#viewはitemsから取得するしかない
	def _get_views(self, item):
		#ヘッダにtokenが設定されていないと意味ないのでチェック
		if not 'Authorization' in self._headers:
			return None

		#viewはitemsの情報内から取得可能
		res=self._get_api_response_body(f'items/{item}')
		return res[self.API_PROP_VIEW]

	def _get_stock(self, item):
		#stockはstockersから
		#stockのqueryはユーザー情報に依存
		query=f'page={self._user_config[self.API_PROP_PAGE]}&per_page={self._user_config[self.API_PROP_PER_PAGE]}'
		res=self._get_api_response_all(f'items/{item}/stockers?${query}')
		return res[self.HTTP_PROP_HEADER][self.HTTP_PROP_COUNT]

	def _get_extra_item_data(self, item_config, item):
		if item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_VIEW:
			return self._get_views(item)
		elif item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_STOCK:
			return self._get_stock(item)

	def _parse_result(self, item_config, raw_result):
		if item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_USER:
			return self._parse_raw_user(raw_result)
		else:
			return raw_result

	def _does_show_item(self, key, config):
		if not key in config:
			return False

		return config[key][self.MNG_PROP_SHOW]

	def _parse_raw_item(self, itemid, itemdetail):
		response={}
		for key, value in itemdetail.items():
			#非表示データはスキップ
			if not self._does_show_item(key, self._item_config[self.CONF_PROP_ITEM]):
				continue

			this_item_config=self._item_config[self.CONF_PROP_ITEM][key]
			#user一覧にある情報はそのままparse
			if this_item_config[self.MNG_PROP_HAVE_LIST]:
				response[this_item_config[self.MNG_PROP_API_PROP]]=self._parse_result(this_item_config, value)
			#それ以外は取得しなおし
			else:
				response[this_item_config[self.MNG_PROP_API_PROP]]=self._get_extra_item_data(this_item_config, itemid)
		return response

	def _parse_raw_user(self, raw_data):
		if self._user_config[QiitaAPI.ITEM_RAW]:
			return raw_data

		response={}
		for key, value in raw_data.items():
			#非表示データはスキップ
			if not self._does_show_item(key, self._user_config[self.CONF_PROP_USER]):
				continue

			#今は特にデータ編集もいらないのでそのまま代入
			this_config=self._user_config[self.CONF_PROP_USER][key]
			response[this_config[self.MNG_PROP_API_PROP]]=value

		return response

	#parse raw items
	def _parse_raw_items(self, raw_data):
		#データを加工して返却
		response={}
		for itemdetail in raw_data:
			itemid=itemdetail[self.API_PROP_ITEMID]
			#stock情報を追加しておく
			if self._item_config[self.CONF_PROP_ITEM][self.API_PROP_STOCK][self.MNG_PROP_SHOW]:
				itemdetail[self.API_PROP_STOCK]=0
			response[itemid]=self._parse_raw_item(itemid, itemdetail)
		return response

	#public
	# itemsを取得する。
	# @ret dict of {itemid:{'titlle', other(related to conf}}
	# @note __init__データにでユーザー指定がある場合は、そのユーザー情報を利用します
	def get_items(self):
		#u記事一覧の取得
		raw_data = self._get_items_by_api()
		#raw指定ならそのまま返却
		if self._item_config[QiitaAPI.ITEM_RAW]:
			return raw_data
		#データを加工して返却
		else:
			return self._parse_raw_items(raw_data)

	# アカウントの全情報を取得する
	# @ret dict of {itemid:{'titlle', other(related to conf}}
	def get_user_items(self):
		#userの記事一覧の取得
		raw_data = self._get_user_items_by_api()
		#raw指定ならそのまま返却
		if self._item_config[QiitaAPI.ITEM_RAW]:
			return raw_data
		#データを加工して返却
		else:
			return self._parse_raw_items(raw_data)

	# item情報を取得する
	# @ret dict of {itemid:{'titlle', other(related to conf}
	def get_item(self, item):
		#userの記事一覧の取得
		raw_data = self._get_item_by_api(item)
		#raw指定ならそのまま返却
		if self._item_config[QiitaAPI.ITEM_RAW]:
			return raw_data
		#データを加工して返却
		else:
			return self._parse_raw_item(item, raw_data)
