import cv2 as cv
import os 
import numpy as np 
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
from skimage.io import imread
from skimage.color import rgb2gray
from typing import Union


path='examples/images'

img_list=os.listdir(path)

rng=np.random.default_rng(len(img_list))
random_ints=rng.integers(low=0, high=len(img_list), size=1)

random_seed=random_ints
random_seed=(int(random_seed))

##random image entry 177 in db. Change to img_list[random_seed] for tru random generation
random_img=img_list[0]
print(random_img)

os.chdir(path)
# First image in db collection
#random image 177
file=random_img


def load_image(file: str, grey: bool = False) -> np.ndarray:
    """
    Load an image from a specified file path and optionally convert it to grayscale.

    Parameters:
    file (str): The path to the image file.
    grey (bool): If set to True, the image will be converted to grayscale. Default is False.

    Returns:
    np.ndarray: The loaded image, either in color or grayscale.
    """
    # Load the image from the specified file path
    img = cv.imread(file)

    # Check if the image should be converted to grayscale
    if grey:
        # Convert the image to grayscale
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Return the modified or original image
    return img

def show_image (img: np.array, label:str) -> None: 
    img=load_image(file)
    cv.imshow(label, img)
    if cv.waitKey(0) & 0xff == 27:
       cv.destroyAllWindows()
    else:
       cv.waitKey(5000)
       cv.destroyAllWindows() 
 

load_image(file)
show_image(file, "Original Image. Press 0")

#Harris Feature Matching
img=cv.imread(file)
gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray=np.float32(gray)
dst=cv.cornerHarris(gray,2,3,0,0.04)
dst=cv.dilate(dst, None)

#Threshold for an optimal value, it may vary depending on the image.
img[dst>0.03*dst.max()]=[0,0,255]


cv.imshow('Harris Feature Matching', img)
if cv.waitKey(0) & 0xff == 27:
     cv.destroyAllWindows()

#Sift Algorithm
img = cv.imread(file)
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
sift = cv.SIFT_create()
kp = sift.detect(gray,None)
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv.imshow('Sift Algorithm',img)
if cv.waitKey(0) & 0xff == 27:
     cv.destroyAllWindows()

#Orb Approach


img = cv.imread(file, cv.IMREAD_GRAYSCALE)
# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints with ORB
kp = orb.detect(img,None)
# compute the descriptors with ORB
kp, des = orb.compute(img, kp)
# draw only keypoints location,not size and orientation
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
plt.imshow(img2), plt.show()

#HOG Approach using SciKit Learn
image = cv.imread(file)
gray= cv.cvtColor(image,cv.COLOR_BGR2GRAY)

fd, hog_image = hog(gray, orientations=8, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualize=True, channel_axis=None)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

ax1.axis('off')
ax1.imshow(image, cmap=plt.cm.gray)
ax1.set_title('Input image')


# Rescale histogram for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

ax2.axis('off')
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title('Histogram of Oriented Gradients')
plt.show()



MIN_MATCH_COUNT = 10
img1 = cv.imread('spongebob caveman meme.jpg', cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread('spongebob mocking meme.jpg', cv.IMREAD_GRAYSCALE) # trainImage
# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)
# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
     if m.distance < 0.7*n.distance:
          good.append(m)

if len(good)>MIN_MATCH_COUNT:
 src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
 dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
 M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
 matchesMask = mask.ravel().tolist()
 h,w = img1.shape
 pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
 dst = cv.perspectiveTransform(pts,M)
 img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
else:
 print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
 matchesMask = None

 draw_params = dict(matchColor = (0,255,0), # draw matches in green color
 singlePointColor = None,
 matchesMask = matchesMask, # draw only inliers
 flags = 2)
img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
plt.imshow(img3, 'gray'),plt.show()


##Orb Detector

img1 = cv.imread('spongebob caveman meme.jpg', cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread('spongebob mocking meme.jpg', cv.IMREAD_GRAYSCALE) # trainImage

# Initiate SIFT detector
orb = cv.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params,search_params)

des1 = np.float32(des1)
des2 = np.float32(des2)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

matches = flann.knnMatch(des1,des2,k=2)
# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
     if m.distance < 0.7*n.distance:
          good.append(m)
print(good)
if len(good)>MIN_MATCH_COUNT:
 src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
 dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
 M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
 matchesMask = mask.ravel().tolist()
 h,w = img1.shape
 pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
 dst = cv.perspectiveTransform(pts,M)
 img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
else:
 print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
 matchesMask = None

 draw_params = dict(matchColor = (0,255,0), # draw matches in green color
 singlePointColor = None,
 matchesMask = matchesMask, # draw only inliers
 flags = 2)
img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
plt.imshow(img3, 'gray'),plt.show()

