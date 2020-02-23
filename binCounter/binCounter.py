import cv2
import numpy as np
import copy
import os
from os.path import basename, dirname, splitext, exists, join
import tkinter
import tkinter.filedialog as tkdialog
import csv
from tqdm import tqdm

# 測定値をリストにappendしていくと.csvの整形が面倒
# なので1データずつcsv.writerで書き込んでいる

root = tkinter.Tk()
fTyp = [('画像ファイル', '*')]
iDir = '/home/ユーザ名/'


# 閾値を入力させるダイアログ生成
def dialog():

    # ボタン押下時の処理
    def bfunc1():
        global threshold
        threshold = int(e1.get())
        root.destroy()

    def bfunc2():
        global threshold
        threshold = -1
        root.destroy()

    l1 = tkinter.Label(root, text="Threshold(0~255)")
    l1.grid(column=0, row=0)
    e1 = tkinter.Entry(root, bd=1)
    e1.grid(column=1, row=0)
    b1 = tkinter.Button(text='next', command=bfunc1)
    b1.grid(column=2, row=0)
    b2 = tkinter.Button(text='Otsu binarization', command=bfunc2)
    b2.grid(column=1, row=1)

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


# 二値化処理
def binarization(path, datalist):
    datalist.clear()

    src = imread(path)  # 画像の絶対パス
    fname, ext = splitext(basename(path))  # ファイル名
    fext = splitext(basename(path))[1][0:]  # ファイル拡張子
    folder = str(dirname(path))+'/'+'binary_images'  # 保存用ディレクトリ

    height, width, channels = src.shape[:3]  # 画像のサイズとチャンネル数を取得
    dst = copy.copy(src)  # 出力画像を格納するdst画像メモリを確保
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # グレースケール化

    # 画像の二値化処理
    if threshold in range(0, 256):
        ret, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    else:
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    nlabels, labelimage, contours, gocs = cv2.connectedComponentsWithStats(binary)  # ラべリング処理

    colors = []
    for i in range(1, nlabels + 1):
        colors.append(np.array([0, 0, 255]))

    for y in range(0, height):
        for x in range(0, width):
            if labelimage[y, x] > 0:
                dst[y, x] = colors[labelimage[y, x]]
            else:
                dst[y, x] = [0, 0, 0]

    # 保存用ディレクトリがない場合，作成
    if not exists(folder):
        os.mkdir(folder)

    # リストにファイル名と測定値を投げる
    area = int(contours[[0], [4]])
    width = int(contours[[0], [2]])
    length = int(contours[[0], [3]])
    datalist.append(str(fname)+str(fext))
    datalist.append(area)
    datalist.append(width)
    datalist.append(length)

    # 結果保存
    imwrite(join(folder, str(fname)+'_bin'+str(fext)), dst)


# メイン処理
def mainfunc():
    dialog()
    value = []  # ファイル名と測定値入れるリスト
    fnames = tkdialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)  # ファイル名取得

    for file in tqdm(fnames):
        binarization(file, value)
        with open(str(dirname(file)) + '/' + 'binary_images' + '/' + 'result.csv', 'a', newline="") as g:
            writer = csv.writer(g)
            writer.writerow(value)

    print('finished!')


if __name__ == '__main__':
    mainfunc()
