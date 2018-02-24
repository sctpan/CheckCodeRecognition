# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:30:13 2018

@author: pan
"""
import requests
from PIL import Image
import numpy as np
from sklearn.externals import joblib
def process_pic(path):
    im = Image.open(path)
    im = im.point(lambda i: i != 43, mode='1')
    y_min, y_max = 0, 22  # im.height - 1 # 26
    split_lines = [5, 17, 29, 41, 53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    return ims

def process(data):
    for i in range(0,len(data)):
        if(data[0][i] > 0):
            data[0][i] = 1
    return data   

def recognize_checkcode(path):
    model_path = r'./model/svm.model'
    model = joblib.load(model_path)
    char_list = list("0123456789abcdefghijklmnopqrstuvwxy")
    ims = process_pic(path)
    code = []
    for j in range(4):
        data = np.array(ims[j].getdata()).reshape(1,-1)
        data = process(data)
        code.append(predict(model,data))
    return code[0] + code[1] + code[2] + code[3]
        
def recognize(y):
    char_list = list("0123456789abcdefghijklmnopqrstuvwxy")  
    return char_list[y]
    
def predict(clf,x):
    return recognize(int(clf.predict(x)[0]))





