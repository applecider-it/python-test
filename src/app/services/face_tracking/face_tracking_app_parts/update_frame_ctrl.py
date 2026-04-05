import cv2 # カメラ・画像処理ライブラリ

from app.services.camera.capture import imgcap_to_imgtk

class UpdateFrameCtrl:
    """
    フレーム処理

    self.main: メインクラスインスタンス
    """

    def __init__(self, main):
        self.main = main
        pass

    def update_frame(self):
        """
        フレーム処理実行
        """

        # カメラから画像取得
        ret, frame = self.main.cap.read()

        if ret:
            # 正常に取得できた場合のみ処理

            # 顔検出用にグレースケール化
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 顔検出
            faces = self.main.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,   # 検出の細かさ（小さいほど細かい）
                minNeighbors=5     # ノイズ除去（大きいほど厳しい）
            )

            self.draw_rectangle(frame, faces)

            # サイズをウィンドウに合わせる
            frame = cv2.resize(frame, (self.main.screen_width, self.main.screen_height))

            imgtk = imgcap_to_imgtk(frame)

            # 画像をラベルに設定
            # （参照を保持しないと画像が消えるので注意）
            self.main.label.imgtk = imgtk
            self.main.label.configure(image=imgtk)

    def draw_rectangle(self, frame, faces):
        """
        検出した顔に矩形を描画
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),           # 左上
                (x + w, y + h),   # 右下
                (0, 255, 0),      # 色（緑）
                2                 # 線の太さ
            )
