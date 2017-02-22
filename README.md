# Naive_Bayes_Classifier_test
ナイーブベイズを使った記事分類器＋ウェブインターフェース
##実行環境
Anaconda-
Django-
##依存パッケージ

natto-py
readability-lxml

##使い方
まずクローラーを走らせる
    python clawler.py
続いて学習用データを生成する。
    python data_process.py　[保存ファイル名]
生成された dictionary{hogehoge} のパスを/classify/views.py のpathに追加する。

あとはDjangoのDBを初期化するなどして、/classifyにアクセスすれば使える。Accuracyを求めたい場合は、classify.pyに
dictioanry{hogehoge}のパスを追加してやり、
    python classify.py
を実行すると、testが走ると同時にaccuracyも計算される。
##学習データ
今回はGunosyからスクレイピングすることで以下の8つの分類を学習する。
[エンタメ,スポーツ,おもしろ,国内,海外,コラム,IT・科学,グルメ]
##スクレイピングデータの格納方法
title,source,sentence,labelなる順番でCSVに格納している。


##原理
今回の記事分類はナイーブベイズ法に基づいて行う。

###スクレイピング詳細
beautifulsoup4を使用している。未知の記事に対してはreadability-lxmlを用いて本文記事を推定している