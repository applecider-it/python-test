import tkinter as tk # GUIライブラリ（ウィンドウ表示）
from PIL import Image, ImageTk # OpenCV画像 → Tkinter表示用に変換
import cv2 # カメラ・画像処理ライブラリ

class FaceTrackingApp:
    """
    カメラ映像を取得して顔検出し、
    Tkinterのウィンドウにリアルタイム表示する

    ■ self

    self.screen_width: 画面の横幅
    self.screen_height: 画面の縦幅
    self.cap: カメラ
    self.label: 画像を表示するラベル（ここに映像を表示）
    self.face_cascade: 顔検出モデル

    ■ 処理の流れ

    run()
      ↓
    update_frame()（繰り返し呼ばれる）
      ↓
    顔検出 → 描画 → 表示

    ■ 全体イメージ

    [カメラ] → [OpenCV処理] → [PIL変換] → [Tkinter表示]

    ============================================
    """

    def __init__(self):
        """
        初期化処理
        ・カメラの設定
        ・顔検出モデルの読み込み
        ・ウィンドウの作成
        """

        self.screen_width = 320
        self.screen_height = 240

        # =========================
        # カメラ初期化
        # =========================
        # 0 = デフォルトカメラ（内蔵カメラ）
        self.cap = cv2.VideoCapture(0)

        # カメラ解像度を設定（軽量化のため低め）
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.screen_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen_height)

        # =========================
        # 顔検出モデル読み込み
        # =========================
        # OpenCVに付属している学習済みデータを使用
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # =========================
        # Tkinterウィンドウ作成
        # =========================
        self.root = tk.Tk()
        self.root.title("カメラ + 顔検出")   # タイトルバー
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")       # ウィンドウサイズ

        # 画像を表示するラベル（ここに映像を表示）
        self.label = tk.Label(self.root)
        self.label.pack()   # 配置して表示する

        # =========================
        # ウィンドウを閉じたときの処理登録
        # =========================
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        """
        カメラから1フレーム取得して処理する
        ・顔検出
        ・枠描画
        ・画面表示
        """

        # カメラから画像取得
        ret, frame = self.cap.read()

        # 正常に取得できた場合のみ処理
        if ret:
            # =========================
            # 顔検出用にグレースケール化
            # =========================
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # =========================
            # 顔検出
            # =========================
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,   # 検出の細かさ（小さいほど細かい）
                minNeighbors=5     # ノイズ除去（大きいほど厳しい）
            )

            # =========================
            # 検出した顔に矩形を描画
            # =========================
            for (x, y, w, h) in faces:
                cv2.rectangle(
                    frame,
                    (x, y),           # 左上
                    (x + w, y + h),   # 右下
                    (0, 255, 0),      # 色（緑）
                    2                 # 線の太さ
                )

            # =========================
            # Tkinterで表示できる形式に変換
            # =========================

            # BGR → RGB（OpenCVとPILの色順の違い対応）
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # サイズをウィンドウに合わせる
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))

            # numpy配列 → PIL画像
            img = Image.fromarray(frame)

            # PIL画像 → Tkinter用画像
            imgtk = ImageTk.PhotoImage(image=img)

            # 画像をラベルに設定
            # （参照を保持しないと画像が消えるので注意）
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        # =========================
        # 一定時間後に再度この関数を呼ぶ（ループ）
        # =========================
        # 200ms = 約5FPS
        self.root.after(200, self.update_frame)

    def on_close(self):
        """
        ウィンドウを閉じるときの処理
        ・カメラ解放
        ・アプリ終了
        """

        # カメラを解放（重要）
        self.cap.release()

        # ウィンドウを閉じる
        self.root.destroy()

    def run(self):
        """
        アプリ起動
        """

        # フレーム更新開始
        self.update_frame()

        # イベントループ開始（これがないとウィンドウが動かない）
        self.root.mainloop()

