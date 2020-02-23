import cv2
import numpy as np
import os
from os.path import splitext, basename, dirname, join, exists
import tkinter
import tkinter.filedialog as tkdialog
from tqdm import tqdm

xmin = xmax = ymin = ymax = "global"
root = tkinter.Tk()
fTyp = [('画像ファイル', '*')]
iDir = '/home/ユーザ名/'


# クロップ範囲を入力させるダイアログ生成
def dialog():

    # ボタン押下時の処理
    def bfunc():
        global xmin, xmax, ymin, ymax
        xmin = e1.get()
        xmax = e2.get()
        ymin = e3.get()
        ymax = e4.get()
        root.destroy()

    l1 = tkinter.Label(root, text="Xmin")
    l1.grid(column=0, row=0)
    e1 = tkinter.Entry(root, bd=1)
    e1.grid(column=1, row=0)
    l2 = tkinter.Label(root, text="Xmax")
    l2.grid(column=0, row=1)
    e2 = tkinter.Entry(root, bd=1)
    e2.grid(column=1, row=1)
    l3 = tkinter.Label(root, text="Ymin")
    l3.grid(column=0, row=2)
    e3 = tkinter.Entry(root, bd=1)
    e3.grid(column=1, row=2)
    l4 = tkinter.Label(root, text="Ymax")
    l4.grid(column=0, row=3)
    e4 = tkinter.Entry(root, bd=1)
    e4.grid(column=1, row=3)
    b1 = tkinter.Button(text='next', command=bfunc)
    b1.grid(column=2, row=4)

    root.mainloop()


# cv2.imreadの日本語対応
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


# cv2.imwriteの日本語対応
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# 画像クロップ
def crop(path, x1, x2, y1, y2):
    src = imread(path)
    fname, ext = splitext(basename(path))
    fext = splitext(basename(path))[1][0:]
    folder = str(dirname(path)) + '/' + 'croped_images'

    # クロップ処理
    dst = src[int(y1):int(y2), int(x1):int(x2)]

    # 保存用ディレクトリがない場合，作成
    if not exists(folder):
        os.mkdir(folder)

    imwrite(join(folder, str(fname) + str(fext)), dst)


# メイン処理
def mainfunc():
    dialog()
    fnames = tkdialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)

    for f in tqdm(fnames):
        crop(f, xmin, xmax, ymin, ymax)
    print('finished!')


if __name__ == '__main__':
    mainfunc()
