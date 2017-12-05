# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:39:51 2017

@author: HaibWang
生成标签，长度自己设定，不足两端补0
"""

import os

# %%
def load_bgImgs(bgImgsDir):
    """
        Load all bgImgs path in the bgImgs directory
    """

    return [bgImgsDir+bgImg for bgImg in os.listdir(bgImgsDir)]

#%%
#if (1):
#    src_dir = ['train_Plate_V1/', 
#               'train_VehicleTpye_V1/',
#               'train_Property_V1/',
#               'train_IdentyNum_V1/',
#               'train_Date_V1/',
#               'train_Title_V1/',
#               'train_Plate_V2/', 
#               'train_VehicleTpye_V2/',
#               'train_Property_V2/',
#               'train_IdentyNum_V2/',
#               'train_Date_V2/',
#               'train_Title_V2/']
#    out_put = open('train_DriveImg_V2_Label.txt', 'w')
#else:
#    src_dir = ['test_Plate_V1/', 
#               'test_VehicleTpye_V1/',
#               'test_Property_V1/',
#               'test_IdentyNum_V1/',
#               'test_Date_V1/',
#               'test_Title_V1/',
#               'test_Plate_V2/', 
#               'test_VehicleTpye_V2/',
#               'test_Property_V2/',
#               'test_IdentyNum_V2/',
#               'test_Date_V2/',
#               'test_Title_V2/']
#    out_put = open('test_DriveImg_V2_Label.txt', 'w')

    
if (0):
    src_dir = ['train_Img_V1/']
    out_put = open('train_Img_V1_Label.txt', 'w')
else:
    src_dir = ['test_Img_V1/']
    out_put = open('test_Img_V1_Label.txt', 'w')

#%%

# 输出标签化的结果长度，不足在两端补0
const_length = 33

# 标签集（识别的时候一定要和此对应起来）
label_map = '_ABCDEFGHJKLMNPQRSTUVWXYZ0123456789'

# 标签去重
label = []
for id in label_map:
    if id not in label:
        label.append(id)
        
# 去重的标签和原标签对比，找出多余标签，以便人工去除
for i in range(len(label_map)):
    if (label_map[i] != label[i]):
        print (i, label_map[i], label[i])
        break

# 核心（添加标签处理）
for id in range(len(src_dir)):
    
    ImgPathList = load_bgImgs(src_dir[id])
    
    for i in range(len(ImgPathList)):
#        print (ImgPathList[i])
        imgName = ImgPathList[i].split("/")[-1]
#        print (imgName)
        img = imgName.split("_")[0]
#        print (img)
        out_put.write(ImgPathList[i])
        out_put.write(' ')

        offsets = (int)((const_length - len(img))/2)
        for m in range(const_length):
            if(m > offsets - 1 and m < len(img) + offsets):
                for n in range(len(label_map)):
                    if(label_map[n] == img[m-(offsets)]):
                        out_put.write(str(n))
                        if(m != (const_length - 1)):
                            out_put.write(' ') 
            else:
                out_put.write(str(0))
                if(m != (const_length - 1)):
                    out_put.write(' ')
        out_put.write('\n')
        
out_put.close()