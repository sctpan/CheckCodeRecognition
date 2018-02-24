# 正方教务系统验证码识别工具

## 概述

人工标记了2000个正方教务系统登录网站的验证码，利用其训练支持向量机（SVM）模型，训练后单字符识别精度达98%，验证码整体识别精度达94%。将其封装成库 ZFCheckCode，提供简单易用的验证码识别API，从而方便爬取教务网站信息。

## 安装和使用

下载 ZFCheckCode-0.0.1.tar.gz文件
用pip工具进行安装

```python
pip install ZFCheckCode-0.0.1.tar.gz
```

### API

```python
recognizer.recognize_checkcode('验证码图片所在路径') #识别验证码，返回一个包含四个字符的字符串
from ZFCheckCode import labeller #开始人工标记
trainner.update_model() #更新模型（加入更多标记后）
```

### 注意事项

1. 验证码图片为正方教务系统网站的CheckCode.aspx，将其下载为.png格式文件，不要修改大小或任何其他属性信息
2. 要使用人工标记功能直接添加一行import即可，自动运行图形界面程序帮助标记

### 例子

```python
from ZFCheckCode import recognizer
from ZFCheckCode import labeller #generate a gui program to help you label more checkcodes
from ZFCheckCode import trainner 
trainner.update_model() 
code = recognizer.recognize_checkcode('./checkcode.png')
print(code)
```






