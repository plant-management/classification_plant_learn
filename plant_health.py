from typing import AsyncIterable
from PIL import Image
import glob
import os
from tqdm import tqdm
import numpy as np
import cv2

num = input('user name?(Ayabe→1,Ichiuji→2,Yokoyama→3)→')
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
print('Preparation: Create a folder called "raw_data" in the directory where you put this code and put the plant images you have taken.')
while(r==False):
    b=input('y/n→')
    if(b=='y'):
        break
    elif(b=='n'):
        if not os.path.exists('raw_data/'):
                os.mkdir('raw_data/')
        print('Please put the plant images you took in raw_data.')
        exit()

path='raw_data/'
savedir='resize_data_2/'
count=0

for file in tqdm(os.listdir(path)):
    front,extension=os.path.splitext(file)
    print(front+extension)
    if(extension == '.jpg' or extension == '.JPG'):
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
        health_ok=False
                    
        while  health_ok == False:
            val = input('What is health level of plant?(1~3), no plant(n)→')
            if(val == 'n'):
                cv2.destroyAllWindows()
                break
            try:
                int(val)
            except ValueError:
                print('The input seems to be different.')
                health_ok = False
            else:
                if(1 <= int(val) <= 3):
                    health=val
                    health_ok=True
                else:
                    print('Out of range input.')
                    health_ok = False

        if(health_ok == True):
            if not os.path.exists(savedir):
                os.mkdir(savedir)
            resize.save(savedir+name+'_'+str(count)+'.jpg')
            count += 1
            cv2.destroyAllWindows()

            with open(name + '_health_2.dat', 'a') as h:
                h.write(health)
            
print('Thanks for your help.')