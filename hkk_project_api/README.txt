#DB関連
mysql -u <ユーザ> -p
source <パス>/hkk.sql

sqlalchemyからmysqlに接続するには環境変数に値をセットする、もしくは
hkk_project_api/db/db_setting.pyの13-15行目を各自の接続情報に書き換えてください。

環境変数のセット
export DB_USER=<USER>
export DB_PASSWORD=<PASSWORD>
export DB_HOST=<HOSTNAME>

#Firebase関連
firebaseコンソール→設定→サービスアカウント→秘密鍵の発行　から必要なjsonを発行してください。
ダウンロード後　hkk_project_api/firebase_key/hkk-fb.json　として配置してください


#ビルド
pip install firebase-admin
pip install fastapi
pip install uvicorn
pip install sqlalchemy


#起動
cd hkk_project_api
uvicorn main:app --reload


#エンドポイント
ユーザーAPI
localhost:8000/api/users
出席情報API
localhost:8000/api/attendances
通知送信API
localhost:8000/api/notification
ドキュメント
localhost:8000/docs




#ユーザAPIについて
GET ユーザ情報を返す
POST ユーザの登録

POSTのリクエストボディ(JSON)
例
{
    "name": "Aさん",
    "uid": "xxxxaaaaddddvvvv"
}



#出席情報APIについて
GET 指定された日付の出席情報を返す
POST 出席情報の登録

GET時のリクエストURL
localhost:8000/api/attendances?date={日付}
例 2022/1/16の場合
localhost:8000/api/attendances?date=2022-01-16


POSTのリクエストボディ(JSON)
例


{
    "uid": "xxxxaaaaxxxxdddd"
}



#通知送信APIについて
GET 通知の送信



