import traceback, sys, json
from QiitaAPINull import QiitaAPINull
from QiitaAPIv2 import QiitaAPIv2
from QiitaAPI import QiitaAPI

class QiitaAPIGenerator:
	#コンストラクタ。設定ファイルからversionとdata情報を読み込む
	def __init__(self,confpath):
		try:
			with open(confpath) as f:
				setting = json.loads(f.read())
			#confはjson形式。versionとversion依存のdataを取得する
			version=setting[QiitaAPI.COMMON_VERSION]
			data=setting[QiitaAPI.COMMON_DATA]
			#API IF側に渡すため、user情報もdataに詰める
			if QiitaAPI.COMMON_USER in setting:
				data[QiitaAPI.COMMON_USER]=setting[QiitaAPI.COMMON_USER]
			self._qiita_api = self._generate_api(version, data)
		except:
			print("Failed to read conf file!")
			traceback.print_exc()
			sys.exit()

	#public
	#APIの取得
	def get_qiita_api(self):
		return self._qiita_api

	#private
	#APIのインスタンスを生成
	def _generate_api(self, version, data):
		if version is 2:
			return QiitaAPIv2(data)
		else:
			return QiitaAPINull(data)
