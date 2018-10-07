#Qiita APIのインターフェース定義
from abc import ABCMeta

class QiitaAPI(metaclass=ABCMeta):

	#応答のオブジェクトで利用されるタグ定義
	#item向け
	ITEM_RAW='raw'
	ITEM_TITLE='title'
	ITEM_USER='user'
	ITEM_URL='url'
	ITEM_TAGS='tags'
	ITEM_MARKDOWN_DATA='markdown'
	ITEM_HTML_DATA='html'
	ITEM_CREATED_AT='created_at'
	ITEM_UPDATED_AT='update_at'
	ITEM_VIEW='views'
	ITEM_LIKE='like'
	ITEM_STOCK='stock'
	ITEM_COMMENT='comment'
	#user向け
	USER_ID='id'
	#内部向け共通定義
	#confの共通設定
	COMMON_VERSION='api_ver'
	COMMON_DATA='data'
	COMMON_USER='user'
	COMMON_MAX='max'
	
	def __init__(self, data):
		#user dataがあるかどうかは覚えておく
		self._has_user_data = 'user' in data
		self._parse_setting(data)

	#private
	#@abstractmethod
	def _parse_setting(self, data):
		pass

	#public
	def has_user(self):
		return self._has_user_data

	# itemsを取得する。
	# @ret dict of {itemid:{'titlle', other(related to conf}}
	#@abstractmethod
	def get_items(self):
		pass

	# アカウントの全情報を取得する
	# @ret dict of {itemid:{'titlle', other(related to conf}}
	#@abstractmethod
	def get_user_items(self):
		pass

	# item情報を取得する
	# @ret dict of {itemid:{'titlle', other(related to conf}
	#@abstractmethod
	def get_item(self, item):
		pass
