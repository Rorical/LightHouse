import cv2 as cv
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
 
images_folder = 'right_calib/*'
images_names = sorted(glob.glob(images_folder))
images = []
for imname in images_names:
    im = cv.imread(imname, 1)
    images.append(im)


#criteria used by checkerboard pattern detector.
#Change this if the code can't find the checkerboard
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
rows = 6 #number of checkerboard rows.
columns = 9 #number of checkerboard columns.
world_scaling = 1. #change this to the real world square size. Or not.
 
#coordinates of squares in the checkerboard world space
objp = np.zeros((rows*columns,3), np.float32)
objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
objp = world_scaling* objp
 
 
#frame dimensions. Frames should be the same size.
width = images[0].shape[1]
height = images[0].shape[0]
 
#Pixel coordinates of checkerboards
imgpoints = [] # 2d points in image plane.
 
#coordinates of the checkerboard in checkerboard world space.
objpoints = [] # 3d point in real world space
 
 
for frame in images: 
    #find the checkerboard
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    ret, corners = cv.findChessboardCorners(frame, (rows, columns), cv.CALIB_CB_ADAPTIVE_THRESH)
    
    print(ret)
 
    if ret == True:
 
        #Convolution size used to improve corner detection. Don't make this too large.
        conv_size = (11, 11)
 
        #opencv can attempt to improve the checkerboard coordinates
        corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
        cv.drawChessboardCorners(frame, (rows,columns), corners, ret)
        
        image = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        plt.imshow(image)
        plt.show()
 
        objpoints.append(objp)
        imgpoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
print(ret)
print(mtx.tolist())
print(dist.tolist())
print(np.array(rvecs).tolist())
print(np.array(tvecs).tolist())