import sys, json
from QiitaAPIGenerator import QiitaAPIGenerator

class QiitaAPIMain:
	PARAM_PROP_GEN='generator'
	PARAM_PROP_ACTOR='actor'
	PARAM_PROP_ITEM='item'
	PARAM_PROP_CLASS='class'
	PARAM_PROP_USAGE='usage'
	CONF_PROP_PARAM='param'

	def __init__(self,args):
		#オプション:{itemがあってもいいか？, 対応するクラス名}
		self._opt_table={
							'all'  :{
									self.PARAM_PROP_ITEM:False,
									self.PARAM_PROP_CLASS:'ActionShowAll',
									self.PARAM_PROP_USAGE:"記事情報一覧をJson形式で表示します。confファイルのdataフィールドにuserが指定されている場合はそのユーザー情報を表示します。指定がない場合は最新記事を表示します。"
							},
							'items' :{
									self.PARAM_PROP_ITEM:False,
									self.PARAM_PROP_CLASS:'ActionShowItems',
									self.PARAM_PROP_USAGE:"最新記事情報一覧をJson形式で表示します。表示対象はconfファイルに依存します。"
							},
							'user_items' :{
									self.PARAM_PROP_ITEM:False,
									self.PARAM_PROP_CLASS:'ActionShowUserItems',
									self.PARAM_PROP_USAGE:"指定ユーザーの記事情報一覧をJson形式で表示します。表示対象はconfファイルに依存します。指定がない場合はv2ではaccess_tokenの設定されたユーザーが対象になり、不正なtokenはエラー扱いです。"
							},
							'item' :{
									self.PARAM_PROP_ITEM:True,
									self.PARAM_PROP_CLASS:'ActionShowItem',
									self.PARAM_PROP_USAGE:"指定されたitem idの情報をJson形式で表示します。表示対象はconfファイルに依存します。",
							},
							'other' :{
									self.PARAM_PROP_ITEM:False,
									self.PARAM_PROP_CLASS:'ActionShowUsage',
									self.PARAM_PROP_USAGE:"利用方法(この表示)が表示されます"
							}
						}
		self._config=self._parse_arg(args)

	def action(self):
		self._config[self.PARAM_PROP_ACTOR].action(self._config[self.CONF_PROP_PARAM])

	@classmethod
	def show(self, data):
		print(json.dumps(data, ensure_ascii=False, indent=4))

	def _parse_arg(self,args):
		config={self.CONF_PROP_PARAM:{}}
		if len(args) < 3 or not args[2] in self._opt_table:
			#default
			key='other'
		else:
			#generatorの作成
			config[self.CONF_PROP_PARAM][self.PARAM_PROP_GEN]=QiitaAPIGenerator(args[1]).get_qiita_api()
			#confにuser情報があるか？

			key=args[2]
		#itemidを設定するケース
		if self._opt_table[key] and 3 < len(args):
			config[self.CONF_PROP_PARAM][self.PARAM_PROP_ITEM]=args[3]

		#help文言を設定
		if key is 'other':
			config[self.CONF_PROP_PARAM]=self._opt_table

		#クラス名からglobalsで対応するクラス定義を取得。
		classname=self._opt_table[key][self.PARAM_PROP_CLASS]
		config[self.PARAM_PROP_ACTOR]=globals()[classname]()
		return config

class ActionShowUsage:
	def action(self, parameter):
		print("Usage: python3.6 main.py conf_path [option]")
		print("option:")
		for option, data in parameter.items():
			print(f" #{option}: #{data[QiitaAPIMain.PARAM_PROP_USAGE]}")

class ActionShowAll:
	def action(self, parameter):
		api=parameter[QiitaAPIMain.PARAM_PROP_GEN]
		if api.has_user():
			QiitaAPIMain.show(api.get_user_items())
		else:
			QiitaAPIMain.show(api.get_items())

class ActionShowUserItems:
	def action(self, parameter):
		QiitaAPIMain.show(parameter[QiitaAPIMain.PARAM_PROP_GEN].get_user_items())

class ActionShowItems:
	def action(self, parameter):
		QiitaAPIMain.show(parameter[QiitaAPIMain.PARAM_PROP_GEN].get_items())

class ActionShowItem:
	def action(self, parameter):
		#itemidがあるならそのitemのみ表示
		#try:
			QiitaAPIMain.show(parameter[QiitaAPIMain.PARAM_PROP_GEN].get_item(parameter[QiitaAPIMain.PARAM_PROP_ITEM]))
		#except:
		#	print("Please set valid item")
