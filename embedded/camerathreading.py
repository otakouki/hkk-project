# カメラ取得 (スレッド化)

import threading
import queue
import camera

class CameraThreading(camera.Camera):

    def __init__(self, index):
        self.cap = camera.Camera(index)     # カメラインスタンス
        self.q = queue.Queue(maxsize=4096)  # キュー
        self.canseled = False               # 停止判定フラグ

    # スレッド開始
    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    # スレッド停止
    def stop(self):
        self.canseled = True

    # スレッド解放
    def release(self):
        self.canseled = True
        self.cap.release()

    # スレッドデータ取得
    def read(self):
        return self.q.get()

    # スレッド処理
    def run(self):
        while not self.canseled and self.cap.isOpened():    # カメラが動作中か判定
            if not self.q.full():                           # キューが一杯の場合はスキップ
                _, frame = self.cap.read()                  # キューにカメラ映像追加
                self.q.put((_, frame))