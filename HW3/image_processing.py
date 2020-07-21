#!/usr/bin/env python

"""This is a library of functions for performing color-based image segmentation of an image."""

import cv2
import numpy as np
import rospy

def img_patch(img,box):
    """ Returns a region of interest of img specified by box """
    #check box against the boundaries of the image
    if box[0]<0:
        box[0]=0
    if box[1]<0:
        box[1]=0
    if box[2]>img.shape[0]:
        box[2]=img.shape[0]
    if box[3]>img.shape[1]:
        box[3]=img.shape[1]
    
    return img[box[0]:box[2],box[1]:box[3],:]

def img_patch_show(img,box,window_name):
    """ Show a region of interest of img specified by box """
    region=img_patch(img,box)
    cv2.imshow(window_name,region)

def img_patch_save_csv(img,box,file_name):
    region=img_patch(img,box)
 #   region=np.array(region)
    r=region.shape[0]
    c=region.shape[1]
    with open(file_name,'w+') as file_id:
        for x in range(0,c):
            for y in range(0,r):
                file_id.write('%f,%f,%f\n'%(region[y,x][0],region[y,x][1],region[y,x][2])) 

def segmentation_prepare_dataset():
    img=cv2.imread('../pics/1.jpg',cv2.IMREAD_COLOR)
   # r=img.shape[0]
   # c=img.shape[1]
   # print(r)
   # print("\n")
   # print(c)
   #[y1,x1,y2,x2]
    img_patch_save_csv(img,[0,665,150,800],'training_positive.csv')
    img_patch_save_csv(img,[150,695,350,810],'test_positive.csv')
    img_patch_save_csv(img,[0,400,150,600],'training_negative.csv')
    img_patch_save_csv(img,[150,400,350,600],'test_negative.csv')
    #show the patches
    img_patch_show(img,[0,665,150,800],'region1')
    img_patch_show(img,[150,695,350,810],'region2')
    img_patch_show(img,[0,400,150,600],'region3')
    img_patch_show(img,[150,400,350,600],'region4')

def pixel_classify(p):
    """ Classify a pixel as background or foreground accoriding to a set of predefined rules """
    #This implementation is a stub. You should implement your own rules here.
    if p[0]>30:
        if p[2]>40:
            score=-1
        else:
            score=1.0
    else:
        score=1.0

    return score

def pixel_classify_testing():
    numberpt=0
    numberpositive=0
    numbernegative=0
    with open('test_positive.csv','r') as file_id:
        data=np.genfromtxt(file_id,delimiter=',')
        for row in data:
            if pixel_classify(row)==1.0:
                numberpt+=1
            else:
                numberpt+=1
                numbernegative+=1
    print("number of points %f" %numberpt)
    print("number of false positives %f" %numberpositive)
    print("number of flase negatives %f" %numbernegative)

    numberpt=0
    numberpositive=0
    numbernegative=0

    with open('test_negative.csv','r') as file_id:
        data=np.genfromtxt(file_id,delimiter=',')
        for row in data:
            if pixel_classify(row)==1.0:
                numberpt+=1
                numberpositive+=1
            else:
                numberpt+=1
    print("number of points %f" %numberpt)
    print("number of false positives %f" %numberpositive)
    print("number of flase negatives %f" %numbernegative)


    
def img_classify(img):
    """ Classify each pixel in an image, and create a black-and-white mask """
    img_segmented=img.copy()
    for r in xrange(0,img.shape[0]):
        for c in xrange(0,img.shape[1]):
            p=img[r,c,:]
            if pixel_classify(p)<0:
                img_segmented[r,c,:]=0
            else:
                img_segmented[r,c,:]=255
    return img_segmented

def img_line_vertical(img,x):
    """ Adds a green 3px vertical line to the image """
    img_line=img.copy()
    cv2.line(img_line, (x, 0), (x, img.shape[1]), (0,255,0), 3)
    return img_line

def img_centroid_horizontal(img):
    whitelist=[]
    for r in range(0,img.shape[0]):
        for c in range(0,img.shape[1]):
            if img[r,c,0]==255:
                if img[r,c,1]==255:
                    if img[r,c,2]==255:
                        whitelist.append(c)
    whitelist=sorted(whitelist)
   # if not whitelist:
    #    medianval=0
   # else:
    medianval= np.median(whitelist)
    return medianval


if __name__ == '__main__':
    #load sample image
   # img=cv2.imread('../data/BU_logo.png',cv2.IMREAD_COLOR)
    #show sample region
  #  img_patch_show(img,[50,20,70,40],'region')
    #run classifier to segment image
   # img_segmented=img_classify(img)
    #add a line at 10px from the left edge
   # img_segmented_line=img_line_vertical(img,10)
    #writing to csv
   # img_patch_save_csv(img,[50,20,70,40],'home3_1.2.csv')
    #1.4
    segmentation_prepare_dataset()
    #1.7
   # pixel_classify_testing()
    #1.12
#    img=cv2.imread('../pics/5.jpg',cv2.IMREAD_COLOR)
#    imgfirst= img_classify(img)
#    val= int(img_centroid_horizontal(imgfirst))
#    newimg= img_line_vertical(img,val)
#    newimg2=img_line_vertical(imgfirst,val)
#    cv2.imshow('color',newimg)
#    cv2.imshow('segmented',newimg2)
    #show results
 #   cv2.imshow('segmented',img_segmented_line)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()
