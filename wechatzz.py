#coding=utf-8
'''
Created by
    author: cq.zan
    time:   2018-1-4
'''

import math
import os
from PIL import Image

#需要粘贴的图形的地址
path = 'D:\\py\\touxiang\\zhu3.jpg'
#粘贴的头像地址
path1='D:\\py\\touxiang\\1\\'

#获取每个头像的大小
def get_eachsize():
    im_zhu = Image.open(path)
    im_size = im_zhu.size
    width = im_size[0]
    height = im_size[1]
    pics = os.listdir(path1)
    numpic = len(pics)
    #根据需要粘贴的图形占整张图的面积百分比，大致估算出每个头像的长度
    eachsize=int(math.sqrt(float(width*height*0.75)/numpic))
    global im_zhu,width,pics,numpic
    return eachsize

#获取拼接的x,y坐标
def get_xy(eachsize):
    x = 0
    y = 0
    list_x = []
    list_y = []
    #从图片原点(0,0)开始遍历，找出小于255的点，也就图片中不是白色的部分
    while y <= width-1:
        a = im_zhu.getpixel((x, y))
        #a是一个含有RGB参数的元组，只要第一个元素小于255就可以
        if a[0] < 255:
            list_x.append(x)
            list_y.append(y)
            #粘贴一张图片后，x坐标往后移一个eachsize的距离
            x += eachsize
            #一排满了后y坐标也要往下移一个eachsize的距离
            if x >= width-1:
                x = 0
                y += eachsize
        #如果是a[0]=255（也就是白色像素点），则x+1继续遍历
        else:
            x += 1
            if x >= width-1:
                x = 0
                y += eachsize
    return list_x,list_y

#拼接图像
def get_img(eachsize,list_x,list_y):
    #新建一个和原图像一样大小的白色图像
    im_new=Image.new('RGB',(width,width),(255,255,255))
    #从头像文件里往新图像开始粘贴
    for i in range(len(list_x)):
        im_tx = Image.open(path1 + '/' + pics[i])
        #将图像大小改为计算的大小
        img = im_tx.resize((eachsize, eachsize), Image.ANTIALIAS)
        #开始往坐标粘贴
        x=list_x[i]
        y=list_y[i]
        im_new.paste(img, (x, y))
        print('已粘贴第'+str(i)+"张，头像名字为："+pics[i])
    #保存粘贴好的图片
    im_new.save(path1 + '/' + '666.jpg')

if __name__== "__main__":
    eachsize=get_eachsize()
    xy=get_xy(eachsize)
    list_x=xy[0]
    list_y=xy[1]
    get_img(eachsize,list_x,list_y)








