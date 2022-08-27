# -*- coding: utf-8 -*-

import cv2
from PIL import Image
import time
import matplotlib.pyplot as plt
import camera_config
import numpy as np

CAMWIDTH = 2560
CAMHEIGHT = 720

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAMWIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAMHEIGHT)

def display(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.imshow(image)
    plt.show()
# 视差计算
def stereoMatchSGBM(left_image, right_image, down_scale=False):
    # SGBM匹配参数设置
    if left_image.ndim == 2:
        img_channels = 1
    else:
        img_channels = 3
    blockSize = 9
    paraml = {'minDisparity': 0,
             'numDisparities': 128,
             'blockSize': blockSize,
             'P1': 8 * img_channels * blockSize ** 2,
             'P2': 32 * img_channels * blockSize ** 2,
             'disp12MaxDiff': 1,
             'preFilterCap': 63,
             'uniquenessRatio': 15,
             'speckleWindowSize': 100,
             'speckleRange': 1,
             'mode': cv2.STEREO_SGBM_MODE_SGBM_3WAY
             }
 
    # 构建SGBM对象
    left_matcher = cv2.StereoSGBM_create(**paraml)
 
    # 计算视差图
    size = (left_image.shape[1], left_image.shape[0])
    if down_scale == False:
        disparity_left = left_matcher.compute(left_image, right_image)
 
    else:
        left_image_down = cv2.pyrDown(left_image)
        right_image_down = cv2.pyrDown(right_image)
        factor = left_image.shape[1] / left_image_down.shape[1]
 
        disparity_left = left_matcher.compute(left_image_down, right_image_down)
        disparity_left = factor * disparity_left
 
    # 真实视差（因为SGBM算法得到的视差是×16的）
    trueDisp_left = disparity_left.astype(np.float32) / 16.
 
    return trueDisp_left

def getDepthMapWithQ(disparityMap : np.ndarray, Q : np.ndarray) -> np.ndarray:
    points_3d = cv2.reprojectImageTo3D(disparityMap, Q)
    depthMap = points_3d[:, :, 2]
    reset_index = np.where(np.logical_or(depthMap < 0.0, depthMap > 65535.0))
    depthMap[reset_index] = 0
 
    return depthMap.astype(np.float32)


def rectifyImage(image1, image2):
    rectifyed_img1 = cv2.undistort(image1, camera_config.left_camera_matrix, camera_config.left_distortion)
    rectifyed_img2 = cv2.undistort(image2, camera_config.right_camera_matrix, camera_config.right_distortion)
    
    rectifyed_img1 = cv2.remap(rectifyed_img1, camera_config.left_map1, camera_config.left_map2, cv2.INTER_AREA)
    rectifyed_img2 = cv2.remap(rectifyed_img2, camera_config.right_map1, camera_config.right_map2, cv2.INTER_AREA)
 
    return rectifyed_img1, rectifyed_img2

while cap.isOpened():
    ret, frame = cap.read()
    left_img = frame[:, 0:1280]
    right_img = frame[:, 1280:2560]

    left_img = cv2.medianBlur(left_img, 7)
    right_img = cv2.medianBlur(right_img, 7)
    
    left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
    right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    
    left_img = cv2.equalizeHist(left_img)
    right_img = cv2.equalizeHist(right_img)
    
    left_img, right_img = rectifyImage(left_img, right_img)
        
    left_disp = stereoMatchSGBM(left_img, right_img, down_scale= True)
    
    left_disp = cv2.medianBlur(left_disp, 5)
    
    left_disp = cv2.morphologyEx(left_disp, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)), iterations=3)
        
    left_disp = left_disp[:, 128:]
    
    # 显示点云
    #right_depth = getDepthMapWithQ(right_disp, camera_config.Q)
    
    #plt.imshow(cv2.resize(left_disp, (22, 8), interpolation=cv2.INTER_AREA))
    plt.imshow(left_disp)
    plt.show()
    
    #plt.imshow(depthMap)
    #plt.show()

    
cap.release()