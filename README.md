# get_qiita_informaion
qiitaの自記事に関する閲覧、いいね、ストック数を取得するツール

### 使い方

Usage: python3.6 main.py conf_path [option]

|option|説明|
|:---|:---|
|all|自身の記事情報一覧をJson形式で表示します。|
|view itemid|指定されたitem idの閲覧数を表示します。|
|stock itemid|指定されたitem idのストック数を表示します。|
|like itemid|指定されたitem idのいいね数を表示します。|
|all itemid|指定されたitem idの閲覧数、ストック数、いいね数を表示します。|
|その他|利用方法(この表示)がされます|

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

- アクセストークン取得前提だけど、閲覧数以外は別の手段でも取得可能。
- APIで欲しい情報を抜き出しているのはいいけど、文章本文等無駄にしている情報が沢山あるのがもったいない
