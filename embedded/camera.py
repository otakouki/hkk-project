import cv2

class Camera:
    
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)

    # カメラの状態をBoolで返す
    # True...カメラ動作中
    # False...カメラ動作終了
    def isOpened(self):
        return self.cap.isOpened()
    
    # カメラで取得した映像を返す
    def read(self):
        return self.cap.read()

    # カメラ解放処理
    def release(self):
        return self.cap.release()