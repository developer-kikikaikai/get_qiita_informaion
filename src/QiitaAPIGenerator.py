#直接APIを使いたい場合のGenerator
import traceback, sys, json
from QiitaAPINull import QiitaAPINull
from QiitaAPIv2 import QiitaAPIv2
from QiitaAPI import QiitaAPI

class QiitaAPIGenerator:
	#public
	#APIの取得
	@classmethod
	def get_qiita_api(self, confpath):
		return self._generate_api(confpath)

	#privateもどき。
	#設定ファイルからversionとdata情報を読み込み、QiitaAPIを生成
	@classmethod
	def _generate_api(self, confpath):
		try:
			if type(confpath) == dict:#already parsed
				setting=confpath
			else:
				with open(confpath) as f:
					setting = json.loads(f.read())
			#confはjson形式。versionとversion依存のdataを取得する
			version=setting[QiitaAPI.COMMON_VERSION]
			data=setting[QiitaAPI.COMMON_DATA]
			#API IF側に渡すため、user情報もdataに詰める
			if QiitaAPI.COMMON_USER in setting:
				data[QiitaAPI.COMMON_USER]=setting[QiitaAPI.COMMON_USER]
			#maxも同様
			if QiitaAPI.COMMON_MAX in setting:
				data[QiitaAPI.COMMON_MAX]=setting[QiitaAPI.COMMON_MAX]

			return self._get_api_instance(version, data)
		except:
			print("Failed to read conf file!")
			traceback.print_exc()
			sys.exit()

	#APIのインスタンスを生成
	@classmethod
	def _get_api_instance(self, version, data):
		if version is 2:
			return QiitaAPIv2(data)
		else:
			return QiitaAPINull(data)
