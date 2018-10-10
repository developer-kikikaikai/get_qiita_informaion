# get_qiita_informaion
qiita記事のMarkdownや閲覧、いいね、ストック数等の各種情報を取得するツール

### 使い方

Usage: python3.6 main.py conf_path [option]

|option|説明|
|:---|:---|
option:
|all|記事情報一覧をJson形式で表示します。confファイルのdataフィールドにuserが指定されている場合はそのユーザー情報を表示します。指定がない場合は最新記事を表示します。
|items|最新記事情報一覧をJson形式で表示します。表示対象はconfファイルに依存します。|
|user_items|指定ユーザーの記事情報一覧をJson形式で表示します。表示対象はconfファイルに依存します。指定がない場合はv2ではaccess_tokenの設定されたユーザーが対象になり、不正なtokenはエラー扱いです。|
|item|指定されたitem idの情報をJson形式で表示します。表示対象はconfファイルに依存します。|
|other|利用方法(この表示)が表示されます|

### 使い方2

内部で使用しているQiitaMainをimportして使用すれば、取得したjson形式のデータをpythonで好きに加工できます。
使い方は以下です。

```python:
result=QiitaAPIMain(['dummy_data', 'conf_path', 'option', 'option2(あれば)']().action()
```

※conf_pathはファイル名だけでなく、dict形式にロード済みのjsonデータも指定可能にしました。
なので、pythonコード内で動的にパラメーター変更が可能になります。

### 設定値

conf/access_setting.json_sampleを参照ください。

### 取得結果

1つの記事情報は、設定値"item"要素内データのうち、page, per_page, rawを除いたもの&&設定がtrueのものがdict型の要素として取得できます。

```json:記事情報
{
	'title':"タイトル",
	'url':"URL",
	'html':"html形式のデータ",
	'markdown':"Markdown形式のデータ",
	'tags':"タグ一覧",
	'like':"いいね数"
}
```

といった感じ

また、一覧取得の場合は、

```json:記事一覧
{
	"記事のitemid":{記事情報}
}
```

## サンプル

以下を作成しました。詳細は各READMEを参照ください。
APIの使い方サンプルにもなるかと

1. 指定ユーザー記事のMarkdown形式バックアップを取得
sample/backup_markdown

2. ごくごくシンプルなhtml形式で記事を最新20件ローカルに出力
sample/get_html_items/

3. 自分の記事のviews, いいね数, ストック数, コメント数を取得する。
sample/get_own_items/

4.  QiitaAPIv2 itemsの生データを取得
sample/get_raw_qiitav2_items

5.  並列処理での5000件の記事を一気に取得
sample/parallel_processing/

## その他

###  動作確認環境

Linux (Ubuntu 18.04 x python3.6)
Windows 10 ( x python3.7, こちらには以下パッケージ追加が必要でした。)

```:Windowsのパッケージ追加
python -m pip install --upgrade pip
pip install requests
```

### 詳細

[Qiita記事のいいね・Views・ストック数を取得するツールを作った](https://qiita.com/developer-kikikaikai/items/b0a70362386698a1ea2d)
=>記事作成中

### 課題

- ユーザー情報、コメント情報が活かせていない(どう出力できるようになったら嬉しいんだろう？がまとまっていない)
- views, stock, commentを取得するのが重い。
1記事毎に取得が必要なため、内部で上手に排他をかけて並列化すればなんとかなる？

