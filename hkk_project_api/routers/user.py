# coding: utf-8

#FastAPIからサブモジュール用のAPIRouterとエラーハンドリング用のstatusインポート
from fastapi import APIRouter, status, Query
#FastAPIでは型ヒントを使用するため、型ヒントを行えるpydanticをインポート
from pydantic import BaseModel
#レスポンス返却用にインポート
from fastapi.responses import JSONResponse

#作成したdbモジュールからモデル定義ファイルと設定ファイルをインポート
from db import db_model as m
from db import db_setting as s

#サブモジュール用のインスタンス生成
router = APIRouter()

###### データクラス定義 ######
#新規登録用のデータクラス
class Create_user(BaseModel):
    name : str
    uid : str

###### ルーティング ######

#ユーザー情報取得
@router.get("/api/users", tags=["users"])
async def read_users():
    #DBからユーザ情報を取得
    result = s.session.query(m.Users.user_id,m.Users.name,m.Users.uid).all()
    return result

#ユーザー新規登録
@router.post("/api/users", tags=["users"])
async def create_user(data: Create_user):
    #db_modelのUsers()クラスを利用
    user = m.Users()
    #リクエストbodyで受け取ったデータを流し込む
    user.name = data.name
    user.uid = data.uid
    #セッションへ追加
    s.session.add(user)
    #セッション完了
    s.session.commit()
    