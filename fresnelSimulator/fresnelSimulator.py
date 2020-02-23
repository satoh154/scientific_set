import numpy as np
from scipy.special import fresnel
import matplotlib.pyplot as plt
import tkinter


# GUIを表示して数値を投げる
def interface():
    root = tkinter.Tk()

    # ボタン押下時の処理
    def bnfunc():
        global WL, gap, X1, X2, Dx, Y1, Y2, Dy, Px1, Px2, Py1, Py2
        WL = float(e1.get())
        gap = float(e2.get())
        X1 = float(e3.get())
        X2 = float(e4.get())
        Dx = float(e5.get())
        Y1 = float(e6.get())
        Y2 = float(e7.get())
        Dy = float(e8.get())
        Px1 = float(e9.get()) / -2
        Px2 = float(e9.get()) / 2
        Py1 = float(e10.get()) / -2
        Py2 = float(e10.get()) / 2
        root.destroy()

    l1 = tkinter.Label(root, text="光の波長(μm)")
    l1.grid(column=0, row=0)
    e1 = tkinter.Entry(root, bd=1)
    e1.grid(column=1, row=0)
    e1.insert(tkinter.END, 0.365)
    l2 = tkinter.Label(root, text="スリット-スクリーン間の距離(μm)")
    l2.grid(column=0, row=1)
    e2 = tkinter.Entry(root, bd=1)
    e2.grid(column=1, row=1)
    l3 = tkinter.Label(root, text="計算領域のX方向最小値(μm)")
    l3.grid(column=0, row=2)
    e3 = tkinter.Entry(root, bd=1)
    e3.grid(column=1, row=2)
    l4 = tkinter.Label(root, text="計算領域のX方向最大値(μm)")
    l4.grid(column=0, row=3)
    e4 = tkinter.Entry(root, bd=1)
    e4.grid(column=1, row=3)
    l5 = tkinter.Label(root, text="X方向の単位長さ(μm)")
    l5.grid(column=0, row=4)
    e5 = tkinter.Entry(root, bd=1)
    e5.grid(column=1, row=4)
    l6 = tkinter.Label(root, text="計算領域のY方向最小値(μm)")
    l6.grid(column=0, row=5)
    e6 = tkinter.Entry(root, bd=1)
    e6.grid(column=1, row=5)
    l7 = tkinter.Label(root, text="計算領域のY方向最大値(μm)")
    l7.grid(column=0, row=6)
    e7 = tkinter.Entry(root, bd=1)
    e7.grid(column=1, row=6)
    l8 = tkinter.Label(root, text="Y方向の単位長さ(μm)")
    l8.grid(column=0, row=7)
    e8 = tkinter.Entry(root, bd=1)
    e8.grid(column=1, row=7)
    l9 = tkinter.Label(root, text="矩形パターンのX方向長さ(μm)")
    l9.grid(column=0, row=8)
    e9 = tkinter.Entry(root, bd=1)
    e9.grid(column=1, row=8)
    l10 = tkinter.Label(root, text="矩形パターンのY方向長さ(μm)")
    l10.grid(column=0, row=9)
    e10 = tkinter.Entry(root, bd=1)
    e10.grid(column=1, row=9)
    bn = tkinter.Button(text='start', command=bnfunc)
    bn.grid(column=2, row=10)

    root.mainloop()


# 計算領域の作成
def create_area(xmin, xmax, dx, ymin, ymax, dy):
    xaxis = np.arange(xmin, xmax, dx)
    ysaxis = np.arange(ymin, ymax, dy)
    yaxis = np.c_[ysaxis]
    return xaxis, yaxis


# 光強度の計算
def calc_int(xaxis, yaxis):

    # フレネル積分
    def calc_fresnel(t1, t2):
        s1, c1 = fresnel(t1)
        s2, c2 = fresnel(t2)
        dif_s = s2 - s1
        dif_c = c2 - c1
        return dif_s, dif_c

    pr = 1
    pi = 0

    def calc_fx1(xposition):
        fx1 = np.sqrt(2 / (WL * gap)) * (Px1 - xposition)
        return fx1

    def calc_fx2(xposition):
        fx2 = np.sqrt(2 / (WL * gap)) * (Px2 - xposition)
        return fx2

    def calc_fy1(yposition):
        fy1 = np.sqrt(2 / (WL * gap)) * (Py1 - yposition)
        return fy1

    def calc_fy2(yposition):
        fy2 = np.sqrt(2 / (WL * gap)) * (Py2 - yposition)
        return fy2

    vfx1 = np.vectorize(calc_fx1)
    vfx2 = np.vectorize(calc_fx2)
    vfy1 = np.vectorize(calc_fy1)
    vfy2 = np.vectorize(calc_fy2)
    vf_int = np.vectorize(calc_fresnel)

    asv, acv = vf_int(vfx1(xaxis), vfx2(xaxis))
    asw, acw = vf_int(vfy1(yaxis), vfy2(yaxis))

    ar = (acv * asw + asv * acw) / 2
    ai = (asv * asw - acv * acw) / 2

    ur = pr * ar - pi * ai
    ui = pr * ai + pi * ar
    li = (np.power(ur, 2) + np.power(ui, 2))
    return li


def draw_graph(field):
    plt.rcParams['font.size'] = 20
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.tight_layout()

    plt.imshow(field, extent=[X1, X2, Y1, Y2], aspect='auto', interpolation='nearest', cmap='jet')
    plt.xlabel('x(μm)')
    plt.ylabel('y(μm)')
    plt.colorbar()
    plt.clim(0, 1.0)
    plt.grid(True)

    plt.show()


def mainfunc():
    interface()
    xaxis, yaxis = create_area(X1, X2, Dx, Y1, Y2, Dy)
    intensity = calc_int(xaxis, yaxis)
    draw_graph(intensity)


if __name__ == '__main__':
    mainfunc()
