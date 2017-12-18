#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import os
import sys
from PIL import Image, ImageDraw, ImageFont,ImageStat,ImageFilter,ImageChops,ImageEnhance
import cv2
import numpy as np
#from math import *


 # %%
#ref:https://github.com/opencv/opencv/blob/75eeb25c1ed0fdd3c915858431b236bbdbf4fc15/samples/python/video.py        
def addNoiseByCV2(orgPILimg,randnSigma):
    """
        Create a background with Gaussian noise (to mimic paper)
    """
    im_array = np.array(orgPILimg)
    # We add gaussian noise   
    #noise = np.zeros((h, w, 3), np.int8)
    w,h = orgPILimg.size
    noise = np.zeros((h, w, 3), np.int8)
    cv2.randn(noise, np.zeros(3), np.ones(3)*randnSigma)
    im_array = cv2.add(im_array, noise, dtype=cv2.CV_8UC3)
    return Image.fromarray(im_array).convert('RGB')
    
# %%
def aveBlurImgByCV2(orgPILimg, blurSize):
    im_array = np.array(orgPILimg)
    im_array = cv2.blur(im_array , (blurSize, blurSize))
    return Image.fromarray(im_array).convert('RGB')
    
# %%
def gaussianBlurImgByCV2(orgPILimg, blurSize, sigma):
    im_array = np.array(orgPILimg)
    im_array = cv2.GaussianBlur(im_array, (blurSize,blurSize) , sigma)
    return Image.fromarray(im_array).convert('RGB')
    
 # %%
def load_fonts(fontsDir):
    """
        Load all fonts in the fonts directory
    """

    return [fontsDir+font for font in os.listdir(fontsDir)]

# %%
def load_bgImgs(bgImgsDir):
    """
        Load all bgImgs path in the bgImgs directory
    """

    return [bgImgsDir+bgImg for bgImg in os.listdir(bgImgsDir)]

# %%
class generateDigitalCharacterSample:   

    def generateBitsNum(self):

        n = random.randint(1,100)
            
        if(n < 8):
            bitsNum = int(n/2) + 1
        elif(n >= 8 and n < 38):
            bitsNum = 4 + int((n - 8)/5) + 1
        else:
            bitsNum = 10 + int((n - 38)/6) + 1
        
#        print(bitsNum)
        
        return bitsNum
    
    def imageProcessing(self, final_image):
        
        # http://blog.csdn.net/icamera0/article/details/50753705
        # 对比度或者亮度
        if( random.randint(1, 100) <= 40):
            if( random.randint(1, 100) <= 75):
                contrastIntense = 10 - random.randint(1, 4)
                final_image = ImageEnhance.Contrast(final_image).enhance(contrastIntense/10.0)
            else:
                brightIntense = 10 - random.randint(1, 6)
                final_image = ImageEnhance.Brightness(final_image).enhance(brightIntense/10.0)
      
        # 噪声
        if( random.randint(1, 100) <= 40):
            randnSigma = random.randint(10, 15)     #均值:0,δ:10~15  10 -18
            final_image = addNoiseByCV2(final_image, randnSigma) 
        
        # 旋转
        if( random.randint(1, 100) <= 40):
            skewing_angle = 2.5
            random_angle = random.uniform(0 - skewing_angle, skewing_angle)
            final_image = final_image.rotate(random_angle, Image.BICUBIC)
            
        # 模糊
        if( random.randint(0, 100) <= 90):
            thresh = random.randint(0, 100)
            if(thresh <= 35):      #一部分高斯模糊，一部分blur
                blurSize = random.randint(1, 2) * 2 + 1
                sigma = random.randint(0, 30)/20.0
                final_image_blur = gaussianBlurImgByCV2(final_image, blurSize, sigma)
            elif(thresh > 35 and thresh < 70):
                blurSize =random.randint(1, 2) * 2 + 1
                final_image_blur= aveBlurImgByCV2(final_image, blurSize)
            else:
                final_image_blur = final_image.resize((int(215), int(28)), Image.ANTIALIAS)
                final_image_blur = final_image_blur.resize((int(430), int(56)), Image.ANTIALIAS)
                
            output_img = final_image_blur
        else:
            output_img = final_image
    
        return output_img
            
    #绘制虚线 @2017-10-13 
    def drawDottedLineInImg(self, bgImg, fillRed, fillGreen, fillBlue, textYPosition): 
        
        #draw.line((0,im01.size[1], im.size[0], 0), fill = 128) 
        imgW, imgH = bgImg.size
        drawer = ImageDraw.Draw(bgImg)  
        
        #虚线单元宽度
        dotWidth = random.randint(2,4)
       
        #90%在文字下方
        if(random.randint(0,100)<90):
            dottedLineY = textYPosition + random.randint(-1*int(imgH/10),int(imgH/10))
        else:   #10% 的其他情况  #虚线Y坐标 在 下方居多
            if(random.randint(0,100)<90):   
                #底下1/4的概率最大
                if(random.randint(0,100)<75): 
                    dottedLineY = random.randint(int(imgH*3/4),imgH)
                else:
                    dottedLineY = random.randint(int(imgH/2),int(imgH*3/4))
            else:
                dottedLineY = random.randint(1,int(imgH/2))
            
        #每n间隔绘制一个线段
        n=2
        
        if(random.randint(0,100)<75):
            n=2
        else:
            n=3        
        
        lineWidth = random.randint(1,2)
        for dotNum in range(int(imgW/dotWidth)):
            #每
            if (dotNum%n == 0):
                drawer.line((dotNum*dotWidth,dottedLineY, (dotNum+1)*dotWidth,dottedLineY), width=lineWidth,fill = (fillRed,fillGreen,fillBlue))
    
    
    def randomInsertBlankInNums(self,maxInsertNum,cardNumArr):
        insertNum=random.randint(0,maxInsertNum)
        allInsertGap = 0
        for i in range(insertNum):
            if (allInsertGap<(len(cardNumArr)-1)):
                #randint(1 改成2 就会报错
                insertGap=random.randint(1,(len(cardNumArr)-allInsertGap)-1)
                #print('insertGap: ',end=''),print(insertGap)
                allInsertGap = allInsertGap+insertGap
                cardNumArr.insert(allInsertGap,' ')  
        
        return cardNumArr

    def generate19BitsCardNumLayout(self, cardNumArr):
        
        if(len(cardNumArr) != 19):
            return cardNumArr
        
        n = random.randint(1,100)
        
        # 6-13         较多25%
        if(n<=25):
            cardNumArr.insert(6,' ')            

        # 4-4-4-4-3    较多25%
        if(n>25 and n<=50):
            cardNumArr.insert(4,' ')
            cardNumArr.insert(8+1,' ')
            cardNumArr.insert(12+2,' ')
            cardNumArr.insert(16+3,' ') #前面加个三个空格

        # 4-4-4-7      挺有15%
        if(n>50 and n<=65):
            cardNumArr.insert(4,' ')
            cardNumArr.insert(8+1,' ')
            cardNumArr.insert(12+2,' ')

        # 19           也有15%
        if(n>65 and n<=80):
            pass
#            doNothing = 0    #就19位啥也不做

        # 5-4-5-5      也有5
        if(n>80 and n<=85):
            cardNumArr.insert(5,' ')
            cardNumArr.insert(9+1,' ')
            cardNumArr.insert(14+2,' ')

        # 6-12-1     
        if(n>85 and n<=90):
            cardNumArr.insert(6,' ')
            cardNumArr.insert(18+1,' ')

        # (6-4-5-4) (3-4-4-4-4)等情况
        if(n>90):             
            maxInsertNum = 4
            cardNumArr = self.randomInsertBlankInNums(maxInsertNum,cardNumArr)
            
        return cardNumArr

    # 根据位数生成对应的布局
    def generateStrLayout(self, cardNumArr):
        pass
    
    # 产生区域
    def generateArea(self):
        
        bitsNum = self.generateBitsNum()   # 随机产生位数
        
        AreaArr = []
        
        ListCharAndNum = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
                          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                            0,   1,   2,   3,   4,   5,   6,   7,   8,   9]
        
        for i in range(bitsNum):
                ch = random.randint(0, len(ListCharAndNum) - 1)
                AreaArr.append(ListCharAndNum[ch])                # 数字或者字符

        if(random.randint(0,100) < 15):
            if(bitsNum > 4):
                num = random.randint(0, bitsNum - 4)
                AreaArr[num + 1] = AreaArr[num]
                AreaArr[num + 2] = AreaArr[num]      
        
        # 保存图像的文件名，如果直接用赋值，修改Area的同时也会修改AreaFileName的
        AreaFileName=[]
        for num in AreaArr:
            AreaFileName.append(num)
            
        # 字符分布（中间插空）
        if(0):
            AreaArr = self.generateStrLayout(AreaArr)
            
        AreaStr = ''.join(str(i) for i in AreaArr)   
        AreaFileNameStr = ''.join(str(i) for i in AreaFileName)
        
#        print ("AreaStr", AreaStr)
#        print ("AreaFileNameStr: ", AreaFileNameStr)
        
        return AreaStr, AreaFileNameStr
    

    def drawAreaInBgImg(self, chooseFont, bgImg, AreaStr, AreaFileNameStr, imgIndx, output_dir):
        
        #背景图像都归一化到同一个尺寸【最好是8的倍数】
        normBgImgWidth = 430
        normBgImgHeight = 56
        imgW, imgH = bgImg.size
        if (imgW != normBgImgWidth or imgH != normBgImgHeight):
             bgImg = bgImg.resize((int(normBgImgWidth), int(normBgImgHeight)), Image.ANTIALIAS)
        imgW, imgH = bgImg.size  # 归一化后背景大小
        
        # 字体大小确认、字体类别设置、获得文本大小
#        fontSize = 20 + random.randint(-8,4)
        
        if (len(AreaStr) < 5):
            fontSize = 20 + random.randint(-3,8)
        elif (len(AreaStr) >= 5 and len(AreaStr) < 11):
            fontSize = 20 + random.randint(-5,15)
        else:
            fontSize = 20 + random.randint(-3,4)
#        print (fontSize)
        image_str = ImageFont.truetype(chooseFont, size=fontSize)
        text_str_width, text_str_height = image_str.getsize(AreaStr)
#        print('text_width text_height: %sx%s' % (text_str_width, text_str_height))
        text_width = text_str_width
        text_height = text_str_height
        
        # 设置文本在背景图片上的起点位置
        if(text_width > 306 or text_height > 40):
            return 0
        textOffsetX = 62 + random.randint(0, 306 - text_width)
        textOffsetY = 8 + random.randint(0, 40 - text_height)
#        print("起点：", textOffsetX, textOffsetY)
        
        # 将文本和虚线绘制在背景图像上
        drawer = ImageDraw.Draw(bgImg)
        stat = ImageStat.Stat(bgImg)
        if (len(stat.mean) == 1):
            return 0
        r, g, b = stat.mean
        meanGrayValue = int(0.3 * r + 0.59 * g + 0.11 * b)
        fillRed = 0
        fillGreen = 0
        fillBlue = 0
        if(meanGrayValue < 80):
            fillRed = 255 - int(r)
            fillGreen = 255 - int(g)
            fillBlue = 255 - int(b)
        else:
            fillRed = 0 + random.randint( 0, int((255-int(r))/4) )
            fillGreen = 0 + random.randint( 0, int((255-int(g))/4) )
            fillBlue = 0 + random.randint( 0, int((255-int(b))/4) )
        
        drawer.text(xy=(textOffsetX, textOffsetY), 
                    text=AreaStr, font=image_str, 
                    fill=(fillRed,fillGreen,fillBlue)) 

        image_name = AreaFileNameStr+'_'+str(imgIndx)+'_sr'+'.jpg'
        
        output_img = self.imageProcessing(bgImg)
        
        output_img.save(os.path.join(output_dir, image_name))
        
        return 0
    
    # 产生样本核心函数
    def generateSample(self, Fonts, bgImgsDir, totalImgNum, output_dir):
        
        # 如果目标文件夹不存在，则创建对应的文件夹
        if os.path.exists(output_dir) == False:
            os.makedirs(output_dir)
        
        # 格式：'bgImg/***.jpg'
        bgImgPathList = load_bgImgs(bgImgsDir)
        fontsList = load_fonts(Fonts)

        for i in range(totalImgNum):
            try:
                print(i)
               
                # 随机选择一个背景图片
                bgImg = Image.open(bgImgPathList[random.randint(0, len(bgImgPathList) - 1)])
                
                # 产生模拟区域
                AreaStr, AreaFileNameStr = self.generateArea()
                
                # 将模拟区域放入在背景图之中
                self.drawAreaInBgImg(fontsList[random.randint(0, len(fontsList) - 1)],
                                     bgImg,
                                     AreaStr,
                                     AreaFileNameStr,
                                     i,
                                     output_dir)
                
            except Exception as err:     
                print("generateSample产生错误: ",end=''),print(err);                
                continue

        return 0
    
    # 针对特定字符串产生每个字体所对应的样本
    def generateSpecialSample(self, Fonts, bgImgsDir, totalImgNum, output_dir):
        
        # 如果目标文件夹不存在，则创建对应的文件夹
        if os.path.exists(output_dir) == False:
            os.makedirs(output_dir)
        
        # 格式：'bgImg/***.jpg'
        bgImgPathList = load_bgImgs(bgImgsDir)
        fontsList = load_fonts(Fonts)

        for i in range(1):
            try:
                print(i)
               
                # 随机选择一个背景图片
                bgImg = Image.open(bgImgPathList[random.randint(0, len(bgImgPathList) - 1)])
                
                # 产生模拟区域
                AreaStr = '21686771'
                AreaFileNameStr = '21686771'
                
                # 将模拟区域放入在背景图之中
                for j in range(len(fontsList)):
                    self.drawAreaInBgImg(fontsList[j], bgImg, AreaStr, AreaFileNameStr, j, output_dir)
                
            except Exception as err:     
                print("generateSample产生错误: ",end=''),print(err);                
                continue

        return 0
    
    def start(self, n):
        
        # 背景和字体路径
        bgImgsDir = 'bgImg/'
        Fonts = 'Fonts/'
        
        # 测试字体
#        output = 'test'
#        self.generateSpecialSample(Fonts, bgImgsDir, 15000, output)
        
        if (0):
            # 保存训练集
            output_dir = 'train_Img_V1/'
            self.generateSample(Fonts, bgImgsDir, 200000, output_dir)
        else:
            # 保存测试集
            output_dir = 'test_Img_V1/'
            self.generateSample(Fonts, bgImgsDir, 15000, output_dir)
        
# %%
testDigitalCharacterSample = generateDigitalCharacterSample()
testDigitalCharacterSample.start(1)