from typing import AsyncIterable
from PIL import Image
import glob
import os
from tqdm import tqdm
import numpy as np
import cv2

num = input('user name?(綾部→1,一氏→2,横山→3)→')
try:
    int(num)
except ValueError:
    print('no user')
    exit()
else:
    if(int(num)==1):
        name='A1'
        print('Hello AYABE!')
    elif(int(num)==2):
        name='I1'
        print('Hello ICHIUJI!')
    elif(int(num)==3):
        name='Y1'
        print('Hello YOKOYAMA!')
    else:
        print('no user...')
        exit()
r=False
print('事前準備：撮影した植物画像をこのコードを置いているディレクトリ内にraw_dataというフォルダを作成して入れてください．')
while(r==False):
    b=input('y/n→')
    if(b=='y'):
        break
    elif(b=='n'):
        print('上記指示に従って再度実行してください')
        exit()

        
print('必要なモノ1.充分な時間')
while(r==False):
    b=input('y/n→')
    if(b=='y'):
        break
    elif(b=='n'):
        print('時間は作るものです')
        break

print('必要なモノ2.集中力・忍耐力')
while(r==False):
    b=input('y/n→')
    if(b=='y'):
        break
    elif(b=='n'):
        print('休憩を取ってまた今度')
        exit()

print('必要なモノ3.飲み物，糖分，作業用BGM')
while(r==False):
    b=input('y/n→')
    if(b=='y'):
        break
    elif(b=='n'):
        print('今すぐ用意するのです')
        exit()       



#写真を葉損しているディレクトリ
path='raw_data/'
savedir='resize_data/'
count=0
#JPGのファイル名を取得し，配列に入れる
for file in tqdm(os.listdir(path)):
    front,extension=os.path.splitext(file)
    print(front+extension)
    if(extension == '.jpg'):
        img = Image.open(path+front+extension)
        img_width , img_height = img.size
        cut_width=min(img.size)
        cut_height=min(img.size)
        cut=img.crop(((img_width - cut_width) // 2, (img_height - cut_height) // 2, (img_width + cut_width) // 2, (img_height + cut_height) // 2))
        resize = cut.resize((224,224), resample=Image.LANCZOS, reducing_gap=3)
        display=np.asarray(resize)
        display_cv=display[:,:,::-1]
        cv2.imshow('image',display_cv)
        cv2.waitKey(10)
        #resize.show()
        growth_ok=False
        health_ok=False

        while growth_ok == False:
            val1=input('成長度は？(0~5),植物なし→(n)→')
            if(val1 == 'n'):
                cv2.destroyAllWindows()
                break
            try:
                int(val1)
            except ValueError:
                print('入力が違うようです')
                growth_ok = False
            else:
                if(0 <= int(val1) <= 5):
                    growth=val1
                    growth_ok=True
                else:
                    print('範囲外の入力です')
                    growth_ok = False
                    

        while growth_ok == True and health_ok == False:
            val2 = input('健康度は？(0~5)→')
            try:
                int(val2)
            except ValueError:
                print('入力が違うようです')
                health_ok = False
            else:
                if(0 <= int(val2) <= 5):
                    health=val2
                    health_ok=True
                else:
                    print('範囲外の入力です')
                    health_ok = False

        if(growth_ok == True and health_ok == True):
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            resize.save(savedir+name+'_'+str(count)+'.jpg')
            count += 1
            cv2.destroyAllWindows()

            with open(name + '_health.dat', 'a') as h:
                h.write(health)
            with open(name + '_growth.dat', 'a') as g:
                g.write(growth)
print('お疲れ様でした．')