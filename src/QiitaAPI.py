#Qiita APIのインターフェース定義
from abc import ABCMeta

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
	def get_own_all_datas(self):
		pass

	# itemの閲覧数を取得する
	# @ret 閲覧数
	#@abstractmethod
	def get_view(self, item):
		pass

	# ストック数を取得する
	# @ret ストック数
	#@abstractmethod
	def get_stock(self, item):
		pass

	# いいね数を取得する
	# @ret いいね数
	#@abstractmethod
	def get_like(self, item):
		pass
