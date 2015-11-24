# Ticketor

[![Build Status](https://travis-ci.org/kaakaa/ticketor.svg)](https://travis-ci.org/kaakaa/ticketor) [![Coverage Status](https://coveralls.io/repos/kaakaa/ticketor/badge.svg?branch=master&service=github)](https://coveralls.io/github/kaakaa/ticketor?branch=master)

* 機能一覧
  * Tracで複数人への同一チケットを発行する
  * 複数のチケットのステータスを同時に変更する
  * マイルストーン毎のバーンダウンチャートを生成する（削除予定）
  * 接続するTracの情報を設定する

# Usage

## 実行

```
$ git clone htttps://github.com/kaakaa/ticketor.git
$ cd ticketor
$ pip install -r requirements.txt
$ vim conf/config.json			// 接続するTracの情報を入力する
$ chmod +x ./start.sh
$ ./start.sh
```

