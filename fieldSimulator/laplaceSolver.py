import numpy as np
from scipy.sparse import csc_matrix
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import tkinter
import tkinter.filedialog as tkdialog
import time


# GUIを表示してパスと数値を投げる
def interface():
    root = tkinter.Tk()
    ftyp = [('バイナリ画像ファイル', '*')]
    idir = '/home/ユーザ名/'

    # ボタン押下時の処理
    def blfunc():
        global imgpath_l
        imgpath_l = tkdialog.askopenfilename(filetypes=ftyp, initialdir=idir)

    def brfunc():
        global imgpath_r
        imgpath_r = tkdialog.askopenfilename(filetypes=ftyp, initialdir=idir)

    def bnfunc():
        global volt_l, volt_r, tolerance
        volt_l = float(e1.get())
        volt_r = float(e2.get())
        tolerance = float(e3.get())
        root.destroy()

    l1 = tkinter.Label(root, text="電極Aの電圧")
    l1.grid(column=0, row=0)
    e1 = tkinter.Entry(root, bd=1)
    e1.grid(column=1, row=0)
    l2 = tkinter.Label(root, text="電極Bの電圧")
    l2.grid(column=0, row=1)
    e2 = tkinter.Entry(root, bd=1)
    e2.grid(column=1, row=1)
    l3 = tkinter.Label(root, text="計算精度(標準値:1e-4)")
    l3.grid(column=0, row=2)
    e3 = tkinter.Entry(root, bd=1)
    e3.grid(column=1, row=2)
    l4 = tkinter.Label(root, text="電極Aの画像パス")
    l4.grid(column=0, row=3)
    bl = tkinter.Button(text='参照', command=blfunc)
    bl.grid(column=1, row=3)
    l5 = tkinter.Label(root, text="電極Bの画像パス")
    l5.grid(column=0, row=4)
    bl = tkinter.Button(text='参照', command=brfunc)
    bl.grid(column=1, row=4)
    bn = tkinter.Button(text='start', command=bnfunc)
    bn.grid(column=2, row=5)

    root.mainloop()


# 画像の読込みと計算領域の作製
def create_calc_area(value_l, value_r, path_l, path_r):
    electrode_l = np.array(Image.open(path_l), 'object')
    electrode_r = np.array(Image.open(path_r), 'object')
    electrode = electrode_l + electrode_r
    electrode[electrode > 254] = 'a'
    electrode_l[electrode_l > 254] = value_l
    electrode_r[electrode_r > 254] = value_r
    area = electrode_l + electrode_r
    return area, electrode


# Jacobi法の疎行列の計算
def calc_sparse_matrix(boundary):

    # 疎行列用のインデックス計算
    def index(size, x, y):
        return x * size + y

    row_index = []
    col_index = []
    value = []
    s = (boundary.size, boundary.size)

    for i in range(boundary.shape[1]):
        for j in range(boundary.shape[0]):
            k = index(boundary.shape[1], i, j)

            if boundary[j, i] == 'a':
                row_index.append(k)
                col_index.append(k)
                value.append(1.0)

            else:
                if i == 0 and j == 0:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.5)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.5)

                elif i == boundary.shape[1] - 1 and j == 0:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.5)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.5)

                elif i == 0 and j == boundary.shape[0] - 1:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.5)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.5)

                elif i == boundary.shape[1] - 1 and j == boundary.shape[0] - 1:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.5)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.5)

                elif i == 0 and j in range(1, boundary.shape[0] - 1):
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.5)

                elif i == boundary.shape[1] - 1 and j in range(1, boundary.shape[0] - 1):
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.5)

                elif i in range(1, boundary.shape[1] - 1) and j == 0:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.5)

                elif i in range(1, boundary.shape[1] - 1) and j == boundary.shape[0] - 1:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.5)

                else:
                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i + 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i - 1, j))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j + 1))
                    value.append(0.25)

                    row_index.append(k)
                    col_index.append(index(boundary.shape[1], i, j - 1))
                    value.append(0.25)

    return csc_matrix((value, (row_index, col_index)), s)


# Laplace方程式の計算
def solve_laplace(area, boundary, allowable):
    jacobi_mat = calc_sparse_matrix(boundary)
    delta = 1.0
    n_iter = 0
    phi = area.astype(np.float64)
    phi_1d = phi.reshape(phi.size, 1, order='F')
    start_time = time.time()

    while delta > allowable:
        if n_iter % 1000 == 0:
            print("iteration No =", n_iter, "delta =", '{:.15e}'.format(delta))
        phi_1d_new = jacobi_mat.dot(phi_1d)
        delta = np.max(abs(phi_1d_new - phi_1d))
        phi_1d, phi_1d_new = phi_1d_new, phi_1d
        n_iter += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("max iteration reached")
    print("iteration No =", n_iter, "delta =", '{:.15e}'.format(delta))
    print("elapsed time =", str(elapsed_time) + "sec", "(" + str(elapsed_time / 60) + "min" + ")")

    phi_2d = phi_1d.reshape(phi.shape[1], phi.shape[0], order='F')

    return phi_2d


# グラフの描画
def draw_graph(field):
    plt.rcParams['font.size'] = 20
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams["mathtext.fontset"] = 'stix'

    # 電位分布
    plt.imshow(field, aspect='equal', interpolation='nearest', cmap='jet')
    plt.colorbar().set_label('$phi$')
    plt.xlabel('$x$(pixel)')
    plt.ylabel('$y$(pixel)')
    plt.clim(min(volt_l, volt_r), max(volt_l, volt_r))
    plt.show()

    # 電位分布(3D)
    x, y = np.meshgrid(np.arange(0, field.shape[1], 1), np.arange(0, field.shape[0], 1))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(x, y, field, cmap='jet', vmin=min(volt_l, volt_r), vmax=max(volt_l, volt_r))
    ax.set_zlim(min(volt_l, volt_r), max(volt_l, volt_r))
    ax.set_xlabel('$x$(pixel)', labelpad=15)
    ax.set_ylabel('$y$(pixel)', labelpad=15)
    ax.set_zlabel('$phi$')
    plt.show()

    # 電界の絶対値の自乗
    (Ey, Ex) = np.gradient(field, .2, .2)
    square_ex = np.power(np.abs(Ex), 2)
    square_ey = np.power(np.abs(Ey), 2)
    square_e = square_ex + square_ey
    plt.imshow(square_e, aspect='equal', interpolation='nearest', cmap='jet')
    plt.colorbar().set_label('$|E|^2$')
    plt.xlabel('$x$(pixel)')
    plt.ylabel('$y$(pixel)')
    plt.clim(0, max(abs(volt_l), abs(volt_r)))
    plt.show()

    # 電界の絶対値の自乗(3D)
    x, y = np.meshgrid(np.arange(0, field.shape[1], 1), np.arange(0, field.shape[0], 1))
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(x, y, square_e, cmap='jet', vmin=0, vmax=max(abs(volt_l), abs(volt_r)))
    ax.set_zlim(0, max(abs(volt_l), abs(volt_r)))
    ax.set_xlabel('$x$(pixel)', labelpad=15)
    ax.set_ylabel('$y$(pixel)', labelpad=15)
    ax.set_zlabel('$|E|^2$')
    plt.show()


# メイン処理
def mainfunc():
    interface()
    area, electrode = create_calc_area(volt_l, volt_r, imgpath_l, imgpath_r)
    result = solve_laplace(area, electrode, tolerance)
    draw_graph(result)


if __name__ == '__main__':
    mainfunc()
