# 顔認識 (スレッド化)

import threading
import queue
from mtcnn import MTCNN
import cv2
import os

class MTCNNThreading:

    def __init__(self, cap):
        os.system('clear || cls')           # コンソールクリア
        self.cap = cap                      # カメラインスタンス
        self.q = queue.Queue(maxsize=4096)  # キュー
        self.canseled = False               # 停止判定フラグ
        self.detector = MTCNN()             # 顔認識モデル

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

    # スレッドデータ取得
    def read(self):
        return self.q.get()

    # スレッド処理
    def run(self):
        while not self.canseled and self.cap.isOpened():    # カメラが動作中か判定
            if not self.q.full():                           # キューが一杯の場合はスキップ
                _, frame = self.cap.read()                  # キューに顔認識データ追加
                faces = self.detector.detect_faces(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 軽量化のために、RGBへ変換
                self.q.put(faces)
            else:
                os.system('reboot')