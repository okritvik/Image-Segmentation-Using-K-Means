"""
Created on Wed Mar 16 12:03:48 2022

@author: okritvik
"""
import cv2
import numpy as np

image = cv2.imread("./images/Q4image.png")

#Stacking all the pixels into BGR format
arr = np.resize(image,(-1,3))

#Taking four random BGR means 
m1 = [0,0,0]
m2 = [80,80,80]
m3 = [160,160,160]
m4 = [240,240,240]

#To check if the means are converged
m1_prev = [0,0,0]
m2_prev = [80,80,80]
m3_prev = [160,160,160]
m4_prev = [240,240,240]
i = 1
while True:
    #Clusters
    c1 = np.empty((0,3),dtype=np.uint8)
    c2 = np.empty((0,3),dtype=np.uint8)
    c3 = np.empty((0,3),dtype=np.uint8)
    c4 = np.empty((0,3),dtype=np.uint8)
    #Calculating the Manhattan Distance
    for j in range(0,len(arr)):
        d1 = np.abs(arr[j][0] - m1[0]) + np.abs(arr[j][1] - m1[1]) + np.abs(arr[j][2] - m1[2])
        d2 = np.abs(arr[j][0] - m2[0]) + np.abs(arr[j][1] - m2[1]) + np.abs(arr[j][2] - m2[2])
        d3 = np.abs(arr[j][0] - m3[0]) + np.abs(arr[j][1] - m3[1]) + np.abs(arr[j][2] - m3[2])
        d4 = np.abs(arr[j][0] - m4[0]) + np.abs(arr[j][1] - m4[1]) + np.abs(arr[j][2] - m4[2])
        
        dmin = min(d1,d2,d3,d4)
        # print(dmin)
        # Appending the pixel to the corresponding cluster
        if d1==dmin:
            c1 = np.append(c1,np.array([[arr[j][0],arr[j][1],arr[j][2]]]),axis=0)
        elif d2==dmin:
            c2 = np.append(c2,np.array([[arr[j][0],arr[j][1],arr[j][2]]]),axis=0)
        elif d3==dmin:
            c3 = np.append(c3,np.array([[arr[j][0],arr[j][1],arr[j][2]]]),axis=0)
        elif d4==dmin:
            c4 = np.append(c4,np.array([[arr[j][0],arr[j][1],arr[j][2]]]),axis=0)
    
    # Recomputing the Means from the cluster
    for k in range(0,3):
        m1[k] = int(np.mean(c1[:,k]))
        m2[k] = int(np.mean(c2[:,k]))
        m3[k] = int(np.mean(c3[:,k]))
        m4[k] = int(np.mean(c4[:,k]))
    
    #Checking if the means are converged
    if((tuple(m1)==tuple(m1_prev)) and (tuple(m2)==tuple(m2_prev)) and (tuple(m3)==tuple(m3_prev)) and (tuple(m4)==tuple(m4_prev))):
        print("Number of iterations to converge: ",i)
        break
    else:
        m1_prev = m1.copy()
        m2_prev = m2.copy()
        m3_prev = m3.copy()
        m4_prev = m4.copy()
    i += 1

#Changing the pixel BGR to the respective cluster values
print("Clusters Mean BGR Values: ")
print(m1,m2,m3,m4)    
for a in range(image.shape[0]):
    for b in range(image.shape[1]):
        d1 = np.abs(image[a][b][0] - m1[0]) + np.abs(image[a][b][1] - m1[1]) + np.abs(image[a][b][2] - m1[2])
        d2 = np.abs(image[a][b][0] - m2[0]) + np.abs(image[a][b][1] - m2[1]) + np.abs(image[a][b][2] - m2[2])
        d3 = np.abs(image[a][b][0] - m3[0]) + np.abs(image[a][b][1] - m3[1]) + np.abs(image[a][b][2] - m3[2])
        d4 = np.abs(image[a][b][0] - m4[0]) + np.abs(image[a][b][1] - m4[1]) + np.abs(image[a][b][2] - m4[2])
      
        dmin = min(d1,d2,d3,d4)
        # print(dmin)
        if d1==dmin:
            image[a][b] = m1
        elif d2==dmin:
            image[a][b] = m2
        elif d3==dmin:
            image[a][b] = m3
        elif d4==dmin:
            image[a][b] = m4
cv2.imshow("Segmented",image)
cv2.imwrite("Q4_Segmented.png",image)
cv2.waitKey(0)
cv2.destroyAllWindows()