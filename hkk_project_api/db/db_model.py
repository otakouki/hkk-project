# -*- coding: utf-8 -*-
######モデル定義ファイル######

#sqlalchemyライブラリから使用する型などをインポート
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, text
#CURRENT_TIMESTAMP関数を利用するためにインポート
from sqlalchemy.sql.functions import current_timestamp
#外部キー制約と複合UNIQUE制約を設定するためにインポート
from sqlalchemy.schema import ForeignKey, UniqueConstraint

#接続設定ファイルをインポート
from .db_setting import Base
from .db_setting import ENGINE

#usersテーブルのモデルUserを定義
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    uid = Column(String(16),nullable=False)
    #複合uniqueの設定
    __table_args__=(UniqueConstraint('name', 'uid'),)

#ttendancesテーブルのモデルAttendancesを定義
class Attendances(Base):
    __tablename__ = 'attendances'
    user_id = Column(Integer, ForeignKey('users.user_id'),primary_key=True)
    attendance_date = Column(DateTime, primary_key=True, server_default=current_timestamp())
