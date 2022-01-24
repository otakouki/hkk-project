# coding: utf-8
#1つ前のディレクトリにあるモパッケージを読みに行くために追加
import sys
sys.path.append('../')

#FastAPIからサブモジュール用のAPIRouterインポート
from fastapi import APIRouter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


#サブモジュール用のインスタンス生成
router = APIRouter()
#firebase初期化
cred = credentials.Certificate("./firebase_key/hkk-fb.json")
firebase_admin.initialize_app(cred)

###### ルーティング ######

#通知の送信
@router.get("/api/notification", tags=["notification"])
async def notification():
    message = messaging.Message(
        notification=messaging.Notification(
            title='プログラムが人を検知しました',
            body='バスの中を確認してください。',
        ),
            topic='HKK_PUSH',
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)