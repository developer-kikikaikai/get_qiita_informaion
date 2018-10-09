from QiitaAPI import *

class QiitaAPINull(QiitaAPI):
	def _parse_setting(self, data):
		print("{'err':'This version is not support!'}")
		return

	def get_items(self):
		return {}
	def get_user_items(self):
		return {}
	def get_item(self, item):
		return {}
