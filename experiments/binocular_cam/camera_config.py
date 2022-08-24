# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 左相机内参
left_camera_matrix = np.array([[641.4689700069257, 0.0, 662.2753068644041], [0.0, 638.9739178584061, 296.0550973741885], [0.0, 0.0, 1.0]])

# 左相机畸变系数:[k1, k2, p1, p2, k3]
left_distortion = np.array([[0.10719845744766131, -0.19999598847349845, -0.0003934551200849855, 0.0030972538138788076, 0.06498063510669717]])

# 右相机内参
right_camera_matrix = np.array([[758.9663139867057, 0.0, 623.7173616030315], [0.0, 758.8564859650013, 297.76245111693294], [0.0, 0.0, 1.0]])
# 右相机畸变系数:[k1, k2, p1, p2, k3]                                          
right_distortion = np.array([[0.18006327018729287, -0.27208552809829406, -0.0003880416956234727, -0.0026394994017809683, 0.07057973183871555]])

# 旋转向量到旋转矩阵
om = np.array([[0.20064572578879664], [0.019834039153350913], [-1.3812400384661592]])
R = cv2.Rodrigues(om)[0]

# 平移向量
T = np.array([[-5.432582358717901], [3.3062328636571627], [36.23161465269812]])

size = (1280, 720)

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)

left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)

