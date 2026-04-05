import tkinter as tk # GUIライブラリ（ウィンドウ表示）
from PIL import Image, ImageTk # OpenCV画像 → Tkinter表示用に変換
import cv2 # カメラ・画像処理ライブラリ

class UpdateFrame:
    """
    フレーム処理
    """

    def __init__(self, main):
        self.main = main
        pass

    def update_frame(self):
        """
        カメラから1フレーム取得して処理する
        ・顔検出
        ・枠描画
        ・画面表示
        """

        main = self.main

        # カメラから画像取得
        ret, frame = main.cap.read()

        if ret:
            # 正常に取得できた場合のみ処理

            # 顔検出用にグレースケール化
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔検出
            faces = main.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,   # 検出の細かさ（小さいほど細かい）
                minNeighbors=5     # ノイズ除去（大きいほど厳しい）
            )

            # 検出した顔に矩形を描画
            for (x, y, w, h) in faces:
                cv2.rectangle(
                    frame,
                    (x, y),           # 左上
                    (x + w, y + h),   # 右下
                    (0, 255, 0),      # 色（緑）
                    2                 # 線の太さ
                )

            # Tkinterで表示できる形式に変換

            # BGR → RGB（OpenCVとPILの色順の違い対応）
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # サイズをウィンドウに合わせる
            frame = cv2.resize(frame, (main.screen_width, main.screen_height))

            # numpy配列 → PIL画像
            img = Image.fromarray(frame)

            # PIL画像 → Tkinter用画像
            imgtk = ImageTk.PhotoImage(image=img)

            # 画像をラベルに設定
            # （参照を保持しないと画像が消えるので注意）
            main.label.imgtk = imgtk
            main.label.configure(image=imgtk)
