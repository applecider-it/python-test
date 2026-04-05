from PIL import Image, ImageTk # OpenCV画像 → Tkinter表示用に変換
import cv2 # カメラ・画像処理ライブラリ

def framecap_to_imgtk(framecap):
    """
    キャプチャー画像をTkinter用画像に変換
    """

    # BGR → RGB（OpenCVとPILの色順の違い対応）
    frametk = cv2.cvtColor(framecap, cv2.COLOR_BGR2RGB)

    # numpy配列 → PIL画像
    img = Image.fromarray(frametk)

    # PIL画像 → Tkinter用画像
    imgtk = ImageTk.PhotoImage(image=img)

    return imgtk
