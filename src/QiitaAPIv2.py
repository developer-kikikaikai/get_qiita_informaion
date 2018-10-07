#Qiita API v2対応
import sys, json, requests, re
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
	#stockはstockersの要素数をカウントする
	API_PROP_STOCK='stock'
	#stockはcommentsの要素数をカウントする
	API_PROP_COMMENT='comment'

	#1回の取得データ最大数の制限
	DEFAULT_RESULT_MAX=5000

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

		#認証設定
		if self.CONF_PROP_TOKEN in data:
			token=data[self.CONF_PROP_TOKEN]
			self._headers['Authorization']=f'Bearer {token}'

		#ユーザー名設定
		if QiitaAPI.COMMON_USER in data:
			self._user=data[QiitaAPI.COMMON_USER]

		#最大数設定
		if QiitaAPI.COMMON_MAX in data:
			self._result_max=data[QiitaAPI.COMMON_MAX]

		#show関連のデータがないならデフォルトをそのまま使う
		if not self.MNG_PROP_SHOW in data:
			return

		#item関連の設定更新
		self._set_item_config(data[self.MNG_PROP_SHOW])

		#user関連の設定更新
		self._set_user_config(data[self.MNG_PROP_SHOW])

	#デフォルト設定を行う
	def _set_default(self):
		#デフォルトを設定
		self._headers={}
		self._result_max=self.DEFAULT_RESULT_MAX

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
					self.API_PROP_STOCK:	{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:False, self.MNG_PROP_API_PROP:QiitaAPI.ITEM_STOCK},
					self.API_PROP_COMMENT:	{self.MNG_PROP_SHOW:False, self.MNG_PROP_HAVE_LIST:False, self.MNG_PROP_API_PROP:QiitaAPI.ITEM_COMMENT}
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
		res_body=json.loads(res.text)
		return res_body

	#get response all
	def _get_api_response_all(self, extraurl, has_baseurl):
		if has_baseurl:
			res=self._send_get_req(extraurl)
		else:
			res=self._callapi(extraurl)
		res_all={self.HTTP_PROP_HEADER:res.headers}
		res_all[self.HTTP_PROP_BODY]=json.loads(res.text)
		return res_all

	def _get_next_link(self, header):
		#Linkタグがないならreturn
		if not self.HTTP_PROP_LINK in header:
			return ""

		#format:
		#{'Link': '<url>; rel="first",<url>; rel="prev" , <url>; rel="next", <url>; rel="last"'}
		linklist=re.split(r',', header[self.HTTP_PROP_LINK])
		#<url>; rel="xxx"で分割
		for link_raw in linklist:
			#無駄文字を削除後;で分割
			link_split=re.split(r';', re.sub(r"[<>\" ]", "", link_raw))
			# rel="next"を採用
			if link_split[1] == 'rel=next':
				return link_split[0]

		#nextが無かった
		return ""

	#update response, parse header, and return next
	def _update_response_and_get_next_link(self, url, response_all):
		#responseを取得
		response=self._get_api_response_all(url, True)

		#最大数を超えてしまいそうならそこでstop
		merged_count=len(response[self.HTTP_PROP_BODY])+len(response_all)
		if self._result_max < merged_count:
			return ""

		#responseを追加。listなのでextendだけでOK
		response_all.extend(response[self.HTTP_PROP_BODY])

		#最大値に行ったら終了
		if self._result_max == merged_count:
			return ""
		else:
			#次のURLを返却
			return self._get_next_link(response[self.HTTP_PROP_HEADER])

	#get response with link 1st
	def _get_api_response_with_link(self, extraurl, response):
		next_url=self.BASEURL+extraurl
		#nextがなくなるまでgetの繰り返し
		while len(next_url) is not 0:
			next_url=self._update_response_and_get_next_link(next_url, response)

		return response

	#qiita api call
	def _callapi(self, extraurl):
		url=self.BASEURL+extraurl
		return self._send_get_req(url)

	#get request direct
	def _send_get_req(self, url):
		try:
			#print(url)
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

	def _get_page_query(self):
		return f'page={self._item_config[self.API_PROP_PAGE]}&per_page={self._item_config[self.API_PROP_PER_PAGE]}'

	#get user raw result
	def _get_user_items_by_api(self):
		query=self._get_page_query()
		if hasattr(self, '_user'): 
			url=f'users/{self._user}/items?{query}'
		else :
			url=f'authenticated_user/items?{query}'
		#user itemsはlink系
		response=[]
		self._get_api_response_with_link(url, response)
		return response

	#get items raw result
	def _get_items_by_api(self):
		query=self._get_page_query()
		response=[]
		self._get_api_response_with_link(f'items?{query}', response)
		return response

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
		#stockのqueryはユーザー情報に依存(いらないかも)
		query=f'page={self._user_config[self.API_PROP_PAGE]}&per_page={self._user_config[self.API_PROP_PER_PAGE]}'
		res=self._get_api_response_all(f'items/{item}/stockers?${query}', False)
		return res[self.HTTP_PROP_HEADER][self.HTTP_PROP_COUNT]

	def _get_comment(self, item):
		#commentはcommentsから
		#commentのqueryはユーザー情報に依存(いらないかも)
		query=f'page={self._user_config[self.API_PROP_PAGE]}&per_page={self._user_config[self.API_PROP_PER_PAGE]}'
		res=self._get_api_response_all(f'items/{item}/comments?${query}', False)
		return res[self.HTTP_PROP_HEADER][self.HTTP_PROP_COUNT]

	def _get_extra_item_data(self, item_config, item):
		if item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_VIEW:
			return self._get_views(item)
		elif item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_STOCK:
			return self._get_stock(item)
		elif item_config[self.MNG_PROP_API_PROP] == QiitaAPI.ITEM_COMMENT:
			return self._get_comment(item)
		else:
			return None

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
		#stock情報を追加しておく
		if self._item_config[self.CONF_PROP_ITEM][self.API_PROP_STOCK][self.MNG_PROP_SHOW]:
			itemdetail[self.API_PROP_STOCK]=None
		#comment情報を追加しておく
		if self._item_config[self.CONF_PROP_ITEM][self.API_PROP_COMMENT][self.MNG_PROP_SHOW]:
			itemdetail[self.API_PROP_COMMENT]=None

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
				#Noneなら取り直し、それ以外はそのまま
				if value == None:
					response[this_item_config[self.MNG_PROP_API_PROP]]=self._get_extra_item_data(this_item_config, itemid)
				else:
					response[this_item_config[self.MNG_PROP_API_PROP]]=value
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
