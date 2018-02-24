import tkinter as tk
import requests
from PIL import Image, ImageTk, ImageFilter
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
def get_cnt():
    try:
        with open('count.txt','r') as f:
            cnt = f.readline()
            cnt = eval(cnt)
        return cnt
    except:
        with open('count.txt','w') as f:
            f.write('0')
        return 0

def update_cnt(cnt):
    with open('count.txt', 'w+') as f:
        f.write(str(cnt))

def get_checkcode(i):
    r = requests.get('http://jwsys.ctbu.edu.cn/CheckCode.aspx?')
    picname = str(i) + '.png'
    with open(picname, 'wb') as f:
        f.write(r.content)

def process_pic(i):
    picname = str(i) + '.png'
    im = Image.open(picname)
    im = im.point(lambda i: i != 43, mode='1')
    y_min, y_max = 0, 22  # im.height - 1 # 26
    split_lines = [5, 17, 29, 41, 53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    return ims

def get_pic_for_display(i):
    picname = str(i) + '.png'
    im = Image.open(picname)
    w, h = im.size
    w_box = 300
    h_box = 200
    im_resized = resize(w, h, w_box, h_box, im)
    tk_image = ImageTk.PhotoImage(im_resized)
    return tk_image

def resize(w, h, w_box, h_box, pil_image):
    f1 = w_box / w
    f2 = h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def display_pic():
    global im
    tmp = get_cnt() + 1
    get_checkcode(tmp)
    im = tk.PhotoImage(file= str(tmp)+'.png')
    im = get_pic_for_display(tmp)
    picLabel['image'] = im
    cntLabel['text'] = '总计: ' + str(tmp-1) + '/1000'


def save_imgs():
    tmp = get_cnt() + 1
    ims = process_pic(tmp)
    code = var.get()
    for i in range(4):
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(BASE_DIR, 'sets', code[i])
        if os.path.exists(path):
            filepath = os.path.join(path, 'count.txt')
            with open(filepath, 'r') as f:
                char_cnt = eval(f.readline())
        else:
            os.makedirs(path)
            filepath = os.path.join(path, 'count.txt')
            with open(filepath, 'w') as f:
                f.write('0')
                char_cnt = 0
        charname = os.path.join(path, str(char_cnt + 1) + '.png')
        ims[i].save(charname)
        filepath = os.path.join(path, 'count.txt')
        with open(filepath,'w+') as f:
            f.write(str(char_cnt + 1))
    update_cnt(tmp)

def submit():
    save_imgs()
    display_pic()
    var.set('')

def init():
    display_pic()

global im
app = tk.Tk()
app.title('Labeller')
app.geometry('500x260')
picLabel = tk.Label(app)
picLabel.pack()
var = tk.StringVar()
textInput = tk.Entry(app, textvariable = var)
textInput.pack(expand = 'yes', fill = 'both', padx = 100, side = 'top', pady = 10)
submitButton = tk.Button(app, text = "提交", width = '10', command = submit)
submitButton.pack()
cntLabel = tk.Label(app)
cntLabel.pack(pady = 20)
init()
app.mainloop()


