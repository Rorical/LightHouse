# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 左相机内参
left_camera_matrix = np.array([[7.216987022051170e+02,0,0],[3.466376196582395,7.188767549508146e+02,0], [6.328122439619060e+02,3.349082691017522e+02,1]]).T

# 左相机畸变系数:[k1, k2, p1, p2, k3]
left_distortion = np.array([0.180817003973084,-0.171892130815455,0.006207366728294,0.005996992048846,0.012391028975860])

# 右相机内参
right_camera_matrix = np.array([[7.204489785546152e+02,0,0],[1.930216961988856,7.190706178251551e+02,0],[6.860954736611834e+02,3.458067898119065e+02,1]]).T
# 右相机畸变系数:[k1, k2, p1, p2, k3]                                          
right_distortion = np.array([0.170398668594305,-0.146835121746364,0.006835052952965,0.001608196032301,-0.009241431006683])

# 旋转向量到旋转矩阵
R = np.array([[0.997539300562206,2.873692138695482e-05,-0.070109507258677],[-8.501269288510177e-06,0.999999958224291,2.889275757103662e-04],[0.070109512632692,-2.876205919863617e-04,0.997539259133595]]
).T

# 平移向量
T = np.array([-57.601374824298766,-0.024503491907330,1.460150141266724])

size = (1280, 720)

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)

left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)

