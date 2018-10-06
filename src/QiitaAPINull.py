from QiitaAPI import QiitaAPI

class QiitaAPINull(QiitaAPI):
	def _parse_setting(self, data):
		print("Version is not support!")
		return
	def get_own_items(self):
		return []
	def get_own_all_datas(self):
		return {}
	def get_view(self, item):
		return 0
	def get_stock(self, item):
		return 0
	def get_like(self, item):
		return 0
