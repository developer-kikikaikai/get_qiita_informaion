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

### 設定値

conf/access_setting.json_sampleを参照ください。

### 動作確認環境

Linux (Ubuntu 18.04 x python3.6)
Windows 10 ( x python3.7, こちらには以下パッケージ追加が必要でした。)

```:Windowsのパッケージ追加
python -m pip install --upgrade pip
pip install requests
```

### 詳細

[Qiita記事のいいね・Views・ストック数を取得するツールを作った](https://qiita.com/developer-kikikaikai/items/b0a70362386698a1ea2d)

### 更新ポイント

- 汎用ツールに変えたので、ツールを利用したサンプルとして閲覧、ストック数収集やページバックアップ等のスクリプトを用意する。
- ページ指定時の挙動がおかしい。仕様調査・テストが必要
- テストコード作成
