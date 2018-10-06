from QiitaAPIGenerator import QiitaAPIGenerator

class MainAction:
	PARAM_TAG_GEN='generator'
	PARAM_TAG_ACTOR='actor'
	PARAM_TAG_ITEM='item'
	PARAM_TAG_CLASS='class'

	def __init__(self,args):
		#オプション:{itemがあってもいいか？, 対応するクラス名}
		self._opt_table={
							'all'  :{self.PARAM_TAG_ITEM:True, self.PARAM_TAG_CLASS:'ActionShowAll'},
							'html' :{self.PARAM_TAG_ITEM:False,self.PARAM_TAG_CLASS:'ActionOutputHtml'},
							'view' :{self.PARAM_TAG_ITEM:True, self.PARAM_TAG_CLASS:'ActionShowView'},
							'stock':{self.PARAM_TAG_ITEM:True, self.PARAM_TAG_CLASS:'ActionShowStock'},
							'like' :{self.PARAM_TAG_ITEM:True, self.PARAM_TAG_CLASS:'ActionShowLike'},
							'default' :{self.PARAM_TAG_ITEM:False,  self.PARAM_TAG_CLASS:'ActionShowUsage'}
						}
		self._config=self._parse_arg(args)

	def action(self):
		self._config[self.PARAM_TAG_ACTOR].action(self._config['param'])

	def _parse_arg(self,args):
		config={'param':{}}
		if len(args) < 3 or not args[2] in self._opt_table:
			#default
			key='default'
		else:
			#generatorの作成
			config['param'][self.PARAM_TAG_GEN]=QiitaAPIGenerator(args[1]).get_qiita_api()
			key=args[2]
	
		if self._opt_table[key] and 3 < len(args):
			config['param'][self.PARAM_TAG_ITEM]=args[3]

		classname=self._opt_table[key][self.PARAM_TAG_CLASS]
		#globalsでクラス名と対応するクラス定義を取得。
		config[self.PARAM_TAG_ACTOR]=globals()[classname]()
		return config

class ActionShowUsage:
	def action(self, parameter):
		print("Usage: python3.6 main.py conf_path [option]")
		print("option:")
		print(" all: 自身の記事情報一覧をJson形式で表示します。")
		print(" html: html形式で、自身の記事情報一覧を出力します。")
		print(" view itemid: 指定されたitem idの閲覧数を表示します。")
		print(" stock itemid: 指定されたitem idのストック数を表示します。")
		print(" like itemid: 指定されたitem idのいいね数を表示します。")
		print(" all itemid: 指定されたitem idの閲覧数、ストック数、いいね数を表示します。")
		print(" その他: 利用方法(この表示)がされます")

class ActionShowAll:
	def action(self, parameter):
		#itemidがあるならそのitemのみ表示
		if MainAction.PARAM_TAG_ITEM in parameter:
			print(parameter[MainAction.PARAM_TAG_GEN].get_all_data_related_to_item(parameter[MainAction.PARAM_TAG_ITEM]))
		#他は全表示
		else:
			print(parameter[MainAction.PARAM_TAG_GEN].get_own_all_data())

class ActionOutputHtml:
	def action(self, generator):
		print("Not implement yet")

class ActionShowView:
	def action(self, parameter):
		print(parameter[MainAction.PARAM_TAG_GEN].get_view(parameter[MainAction.PARAM_TAG_ITEM]))

class ActionShowStock:
	def action(self, parameter):
		print(parameter[MainAction.PARAM_TAG_GEN].get_stock(parameter[MainAction.PARAM_TAG_ITEM]))

class ActionShowLike:
	def action(self, parameter):
		print(parameter[MainAction.PARAM_TAG_GEN].get_like(parameter[MainAction.PARAM_TAG_ITEM]))
