# coding: utf-8
#日付生成用に追加
import datetime

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
class Create_attendance(BaseModel):
    uid : str

dt_now = datetime.datetime.now()

###### ルーティング ######

#出席情報取得
@router.get("/api/attendances", tags=["attendances"])
async def read_attendance(date: str):
    
    #出席情報がある人を取得
    A = s.session.query(m.Users.user_id,m.Users.name).filter(
        m.Users.user_id.in_(
            s.session.query(m.Attendances.user_id).filter(
                m.Attendances.attendance_date == date
            )
        )
    ).all()
    #出席情報がない人を取得
    not_A = s.session.query(m.Users.user_id,m.Users.name).filter(
        m.Users.user_id.not_in(
            s.session.query(m.Attendances.user_id).filter(
                m.Attendances.attendance_date == date
            )
        )
    ).all()
    
    return {"attendance":A,"not_attendance":not_A}


#出席情報登録
@router.post("/api/attendances", tags=["attendances"])
async def create_attendance(data: Create_attendance):
    dt = data.uid.replace(' ', '')
    result = s.session.query(m.Users.user_id).filter(m.Users.uid==dt).all()
    #リストで返ってくるので解体
    for i in result:
        id=i.user_id
    #insert処理
    attendances = m.Attendances()
    attendances.user_id = int(id)
    sysdate = (dt_now.strftime('%Y%m%d'))
    attendances.attendance_date = sysdate
    #セッションへ追加
    s.session.add(attendances)
    #セッション完了
    s.session.commit()