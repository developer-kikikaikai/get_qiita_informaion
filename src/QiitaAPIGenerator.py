import traceback, sys, json
from QiitaAPINull import QiitaAPINull
from QiitaAPIv2 import QiitaAPIv2

class QiitaAPIGenerator:
	#コンストラクタ。設定ファイルからversionとdata情報を読み込む
	def __init__(self,confpath):
		try:
			with open(confpath) as f:
				setting = json.loads(f.read())
			#confはjson形式。versionとversion依存のdataを取得する
			self._version=setting['api_ver']
			self._data=setting['data']
		except:
			traceback.print_exc()
			sys.exit()

	#public
	#APIの取得
	def get_qiita_api(self):
		#version情報から生成するinstanceを判断
		if not hasattr(self, '_qiita_api'):
			self._qiita_api = self._generate_api()
		return self._qiita_api

	#private
	#APIのインスタンスを生成
	def _generate_api(self):
		if self._version == 2:
			return QiitaAPIv2(self._data)
		else:
			return QiitaAPINull(self._data)
