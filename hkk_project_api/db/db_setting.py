# -*- coding: utf-8 -*-
######DBへの接続設定ファイル######
#OSの環境変数を取得するためにインポート
from __future__ import absolute_import, unicode_literals
import os

#DB操作用にsqlalchemyライブラリインポート
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

#接続したいDBへの接続情報
user_name = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database_name = "hkk"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)

#DBとの接続
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    #自動生成されたSQLを吐き出すようにする
    echo=True
)

#Sessionの作成
session = scoped_session(
    #ORマッパーの設定。自動コミットと自動反映はオフにする
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

#model定義に使う変数
Base = declarative_base()
#DB接続用のセッションクラス、インスタンスが作成されると接続する
Base.query = session.query_property()
