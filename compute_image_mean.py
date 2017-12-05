# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageDraw, ImageFont,ImageStat,ImageFilter,ImageChops,ImageEnhance
import cv2
import numpy as np

# %%
def load_bgImgs(bgImgsDir):
    """
        Load all bgImgs path in the bgImgs directory
    """

    return [bgImgsDir+bgImg for bgImg in os.listdir(bgImgsDir)]  

# %%
class generateTrainImgsMeans:
   
    def start(self, n):
        
        bgImgsDir = 'train_Img_V1/'
        
        redMeanSum = 0
        greenMeanSum = 0
        blueMeanSum = 0
        
        bgImgPathList=load_bgImgs(bgImgsDir)
        print(bgImgsDir)
        print("calculateMeanValueOfImgs Img nums:  ",end=' '), print(len(bgImgPathList))
        
        for i in range(len(bgImgPathList)):     
            bgImg = Image.open(bgImgPathList[i])
            stat = ImageStat.Stat(bgImg)
            r,g,b = stat.mean
            redMeanSum = redMeanSum + r
            greenMeanSum = greenMeanSum + g
            blueMeanSum = blueMeanSum + b
            
            if(((i+1)%5000) == 0):
                print(i)
                print(redMeanSum/i)
                print(greenMeanSum/i)
                print(blueMeanSum/i)
                
        print("r: ", redMeanSum/len(bgImgPathList))
        print("g: ", greenMeanSum/len(bgImgPathList))
        print("b: ", blueMeanSum/len(bgImgPathList))
        
#%%
testgenerateTrainImgsMeans = generateTrainImgsMeans()
testgenerateTrainImgsMeans.start(1)