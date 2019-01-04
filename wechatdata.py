# -*- coding: utf-8 -*-
'''
Created by
    author: cq.zan
    time:   2018-12-28
'''
import itchat
import re
import os
import math
import pymysql
from PIL import Image
import pandas as pd

#微信登陆
def  get_data():
    itchat.auto_login()
    friends=itchat.get_friends(update=True)
    return friends

#获取所需的数据
def parse_data(friendsdata):
    friends_list=[]
    for item in friendsdata:
        friend={
            'NickName':item['NickName'],
            #昵称
            'RemarkName':item['RemarkName'],
            #备注名
            'Sex':item['Sex'],
            #性别
            'Province':item['Province'],
            #省份
            'City':item['City'],
            #城市
            'Signature':item['Signature'].replace('\n','').replace(',',''),
            #个性签名
            'StarFriend':item['StarFriend'],
            #是否星标好友
            'ContactFlag':item['ContactFlag'],
            #好友类型及权限，1和3好友，259和3027不让他看我的朋友圈,655396不看他的朋友圈，

        }
        friends_list.append(friend)
    return friends_list

#存入mysql
def save_mysql(friends_list):
    #连接数据库，设置charst='utf8'的话有的字符不能保存
    conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='wechat',charset='utf8mb4')
    cur=conn.cursor()
    #创建表格sql语句
    sqlc = '''
         set @@global.sql_mode='';
         create table data(
         NickName varchar(50),
         RemarkName varchar(40),
         Sex char(5),
         Province varchar(50),
         City varchar(200),
         Signature varchar(100),
         StarFriend tinyint(2),
         ContactFlag int(5)
         );
         '''
    cur.execute(sqlc)
    conn.commit()
    print("数据表创建成功")
    sqla='''
          insert into data2(NickName,RemarkName,Sex,Province,City,Signature,StarFriend,ContactFlag) values(%s,%s,%s,%s,%s,%s,%s,%s);
          '''
    for i in range(len(friends_list)):
        Nick=friends_list[i]['NickName']
        #过滤掉占位符
        regex1 = re.compile('\s{1,}')
        NickName = re.sub(regex1, '<emoji>', Nick)
        NickName='nonick' if NickName=='' else NickName
        RemarkName=friends_list[i]['RemarkName']
        RemarkName="noremark" if RemarkName=='' else RemarkName
        Sex=friends_list[i]['Sex']
        Sex='nosex' if Sex=='' else Sex
        Province=friends_list[i]['Province']
        Province='nopro' if Province=='' else Province
        City=friends_list[i]['City']
        City='nocity' if City=='' else City
        Sign=friends_list[i]['Signature']
        #过滤掉表情
        regex2=re.compile('<span.*?</span>')
        Signature=re.sub(regex2, '<emoji>', Sign)
        Signature='nosig' if Signature=='' else Signature
        StarFriend=friends_list[i]['StarFriend']
        StarFriend='nostar' if Signature=='' else StarFriend
        ContactFlag=friends_list[i]['ContactFlag']
        ContactFlag='noflag' if ContactFlag=='' else ContactFlag
        print(NickName, RemarkName, Sex, Province, City, Signature, StarFriend,ContactFlag)
        cur.execute(sqla,(NickName, RemarkName, Sex, Province, City, Signature, StarFriend,ContactFlag))
        conn.commit()
        print('插入数据成功')
    cur.close()
    conn.close()
    print("数据写入完毕，已关闭连接  ")

#存入csv
def save_csv(friends_list):
    df=pd.DataFrame(friends_list)
    df.to_csv('D:\\py\\touxiang\\{}.csv'.format(input('请输入朋友圈数据csv保存文件名：')),encoding='utf-8-sig')

#获取头像存入本地
def get_image(path,friend):
    #获取头像
    img=itchat.get_head_img(userName=friend['UserName'])
    #用备注名命名，没有则用昵称命名,有的昵称含有特殊字符不能命名，正则过滤掉
    regex3 = re.compile('[\\s\\\\/:\\*\\?\\\"<>\\|]')
    friend_nick=re.sub(regex3,'',friend['NickName'])
    imgname=friend['RemarkName'] if friend['RemarkName'] != '' else friend_nick
    imgfile = os.path.join(path, imgname + '.jpg')
    #写入jpg格式头像
    with open(imgfile, 'wb') as file:
        file.write(img)


#头像拼接
def create_image(path):
    pics=os.listdir(path)
    numpic=len(pics)
    eachsize=int(math.sqrt(float(604*640)/numpic))
    numline=int(640/eachsize)
    to_image=Image.new('RGBA',(604,640))
    x=0
    y=0
    for i in pics:
        #打开图片
        img=Image.open(path+'/'+i)
        #重新设定大小，设定ANTIALIAS,抗锯齿
        img=img.resize((eachsize,eachsize),Image.ANTIALIAS)
        #粘贴图片,x*eachsize,y*eachsize,粘贴起始点的横纵坐标
        to_image.paste(img,(x*eachsize,y*eachsize))
        x+=1
        #x轴排满一排后，y坐标加一个eachsize，又从x=0开始粘贴
        if x==numline:
            x=0
            y+=1
    #存储图片
    to_image.save(path+'/'+'all.jpg')
    #将拼接图片发送给文件传输助手
    itchat.send_image(path+'/'+'all.jpg','filehelper')


if __name__=="__main__":
    friendsdata=get_data()
    friends_list=parse_data(friendsdata)
    save_csv(friends_list)
    #save_mysql(friends_list)
    while True:
        path = 'D:\\py\\touxiang\\{}\\'.format(input('请输入储存头像文件名：'))
        isExists = os.path.exists(path)
        # 判断path路径是否存在，如果不存在，则创建目录
        if isExists == False:
            os.mkdir(path)
            print("创建头像存储文件成功")
            break
        else:
            print(path + '目录已存在,请重新输入文件名：')
    for friend in friendsdata:
         get_image(path,friend)
         print(friend['NickName']+"头像下载完毕")
    create_image(path)




