#Qiita APIのインターフェース定義
from abc import ABCMeta

DEF_TITLE='title'
DEF_VIEW='view'
DEF_LIKE='like'
DEF_STOCK='stock'

class QiitaAPI(metaclass=ABCMeta):

	def __init__(self, data):
		self._parse_setting(data)

	#private
	#@abstractmethod
	def _parse_setting(self, data):
		pass

	#public
	# 自分のアカウントのitemsを取得する。
	# @ret list of items
	#@abstractmethod
	def get_own_items(self):
		pass

	# 自分のアカウントの全情報を取得する
	# @ret dict of {itemid:{'titlle', 'view', 'like', 'stock'}}
	#@abstractmethod
	def get_own_all_data(self):
		pass

	# itemの閲覧数を取得する
	# @ret {title, 閲覧数}
	#@abstractmethod
	def get_view(self, item):
		pass

	# ストック数を取得する
	# @ret {title, ストック数}
	#@abstractmethod
	def get_stock(self, item):
		pass

	# いいね数を取得する
	# @ret {title, いいね数}
	#@abstractmethod
	def get_like(self, item):
		pass

	# 特定記事の全情報を取得する
	# @ret {title, いいね数, ストック数, 閲覧数}
	#@abstractmethod
	def get_all_data_related_to_item(self, item):
		pass
