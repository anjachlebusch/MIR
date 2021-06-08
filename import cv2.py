from cv2 import cv2
import numpy as np
import itertools
from matplotlib import pyplot as plt
import image_slicer

example=cv2.imread("1880.png")
#print(example)

    
#cv2.imshow("Anja",example)
#cv2.waitKey(0)

height= 30#int(example.shape[0]*0.5)
width = 30#int(example.shape[1]*0.5)
dim=(width,height)
resized_img=cv2.resize(example,dim,interpolation=cv2.INTER_AREA)
a=list(resized_img)
# Define the window size
windowsize_r = 10
windowsize_c = 10

# Crop out the window and calculate the histogram
for r in range(0,resized_img.shape[0] - windowsize_r, windowsize_r):
    for c in range(0,resized_img.shape[1] - windowsize_c, windowsize_c):
        window = resized_img[r:r+windowsize_r,c:c+windowsize_c]
        hist = np.histogram(window,bins=256)
        plt.hist(resized_img.ravel(),256,[0,256])
        plt.title('Histogram for gray scale picture')
        plt.show()
#a= np.array(resized_img)
#print(a)
b = list(np.concatenate(a).flat)
#print(b)
# flat_list = []
#             # Iterate through the outer list
# for element in a:
#         if type(element) is list:
#          # If the element is of type list, iterate through the sublist
#             for item in element:
#                 flat_list.append(item)
#         else:
#                  flat_list.append(element)
# print(flat_list)

cv2.imshow("1880",resized_img)
cv2.waitKey(0)