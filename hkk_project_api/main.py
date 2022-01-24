#FastAPIインポート
from fastapi import FastAPI
#作成したAPIRouterインスタンスがあるファイルをインポート
from routers import user, notification, attendance
#FastAPIのインスタンス作成
app = FastAPI()

#APIRouterインスタンスで作成したエンドポイントを追加
app.include_router(user.router)
app.include_router(notification.router)
app.include_router(attendance.router)