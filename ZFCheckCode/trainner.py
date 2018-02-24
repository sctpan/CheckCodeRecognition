# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:56:06 2018

@author: pan
"""
from PIL import Image  
import numpy as np 
import os  
from sklearn import svm
from sklearn.externals import joblib
  
def load_image(path):   
    im = Image.open(path)  
    data = np.array(im.getdata()).reshape(1,-1)
    data = process(data)
    return data

def process(data):
    for i in range(0,len(data)):
        if(data[0][i] > 0):
            data[0][i] = 1
    return data

def get_count(path, char):
    filepath = os.path.join(path, char, 'count.txt')
    with open(filepath, 'r') as f:
        cnt = eval(f.readline())
    return cnt

def get_label(char):
    global char_list
    for i in range(0, len(char_list)):
        if char_list[i] == char:
            return i
   
                
def build_char_set(path, char):
    cnt = get_count(path, char)
    x = np.zeros((cnt, 264))
    y = np.zeros((cnt, 1))
    for i in range(1, cnt+1):
        filepath = os.path.join(path, char, str(i)+'.png')
        x[i-1,:] = load_image(filepath)
        y[i-1] = get_label(char)
    char_set = np.hstack((x,y))
    return char_set

def build_sets(path):
    global char_list
    sets = build_char_set(path, char_list[0])
    for i in range(1, len(char_list)):
        char_set = build_char_set(path, char_list[i])
        sets = np.vstack((sets,char_set))
    return sets

def build_training_sets(sets, percent):
    length = int(len(sets) * percent)
    return sets[0:length,:]

def build_test_sets(sets, percent):
    length = int(len(sets) * (1 - percent))
    return sets[length:len(sets),:]

def train(training_sets):
    x = training_sets[:,0:264]
    y = training_sets[:,264].reshape(-1,1)
    clf = svm.LinearSVC()
    clf.fit(x, y)
    return clf

def recognize(y):
    global char_list  
    return char_list[y]
    
def predict(clf,x):
    return recognize(int(clf.predict(x)[0]))

def accuracy(pred,real):
    cnt = 0
    for i in range(len(pred)):
        if pred[i] == real[i]:
            cnt = cnt + 1
    return cnt/len(pred)
    
def test(clf,test_sets):
    x = test_sets[:,0:264]
    y = test_sets[:,264].reshape(-1,1)
    length = x.shape[1]
    pred = []
    real = []
    for i in range(0,length):
        pred.append(predict(clf,x[i,:].reshape(1,-1)))
        real.append(recognize(int(y[i])))
    return accuracy(pred, real)

def update_model():
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(BASE_DIR, 'sets')
    model_path = os.path.join(BASE_DIR, 'model','svm.model')
    sets = build_sets(data_path)
    for i in range(5):
        np.random.shuffle(sets)
    training_sets = build_training_sets(sets, 0.9)
    test_sets = build_test_sets(sets, 0.1)
    model = train(training_sets)
    res = test(model, test_sets)
    joblib.dump(model, model_path)
    print('Model updated! The accuracy on test sets: ' + str(res))



global char_list  
char_list = list("0123456789abcdefghijklmnopqrstuvwxy")

