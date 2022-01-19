# mapping parameters: blur, a(,b), offset, edge
# input: two images: based image, texture image
# workflow:
#   1. determine whether the texture image is bigger than the based image with offset
#       yes: crop the texture image
#       no: resize the texture image
#   2. blur the based image 
#   3. do the replacement on the texture image accoding to the blur based image
#   4. blend the original based image and transformed texture image
import os
import json
import cv2
import numpy as np

def getImage(filePath: str):
    return cv2.imread(filePath, cv2.IMREAD_COLOR)

# calculate background color
# input: BGR images
# output: a rough color range of background in gray mode
def getBackgroundColorRange(img, back_mask):
    img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    background = cv2.bitwise_and(img, img, mask=back_mask)
    background = int(np.sum(back_mask / 255 * img) / np.sum(back_mask / 255))
    return list([max(0, background - 10), min(255, background + 10)])

# smooth the edge
def getBlendMask(img, background, a, edge=5):
    h, w = img.shape
    mask = cv2.inRange(img, background[0], background[1]) / 255
    for i in np.nditer(mask, op_flags=["readwrite"]):
        if i <=.9:
            i[...] = a
    mask[edge:h-edge, edge:w-edge] = a

    mask_ = mask[:,:,np.newaxis]
    new_mask = np.concatenate((mask_, mask_, mask_), 2)

    return new_mask

# get Region of Interest
def getROI(mask) -> list:
    x_1 = 0
    y_1 = 0
    x_2 = mask.shape[0]
    y_2 = mask.shape[1]

    ## region of interest through cols
    cols = np.sum(mask, axis = 0)
    for i in range(0, cols.shape[0]):
        if cols[i] != 0:
            y_1 = i
            break
    for i in range(0, cols.shape[0]):
        if cols[-i] != 0:
            y_2= cols.shape[0] - i
            break

    ## region of interest through rows
    rows = np.sum(mask, axis = 1)
    for i in range(0, rows.shape[0]):
        if rows[i] != 0:
            x_1 = i
            break
    for i in range(0, rows.shape[0]):
        if rows[-i] != 0:
            x_2 = rows.shape[0] - i
            break

    return [x_1, x_2, y_1, y_2]

def blendImage(basedImage, basedMask, textureImage, resize=(800,800), blur=2, a=0.4, offset=8):
    def transformT(texture, based):
        height, width = based.shape[:2]
        h, w = texture.shape[:2] 
        if h < height or w < width:
            scale = max(height / h, width / w)
            texture = cv2.resize(texture, (0, 0), fx=scale, fy=scale)
            h, w = texture.shape[:2] 
               
        x1_T = int(h / 2 - height /2)
        y1_T = int(w / 2 - width / 2)
        x2_T = x1_T + height
        y2_T = y1_T + width

        texture = texture[x1_T : x2_T, y1_T : y2_T]

        mid = int((0 + 255) / 2)
        based -= mid
        based  = based / mid

        for w in range(width):
            for h in range(height):
                m = int(based[h][w] * offset)
                if (w - m) >= 0 and (w - m) < width and (h - m) < height:
                    texture[h - m][w - m] = texture[h][w]
        
        return texture


    # get based image and mask
    basedImg = getImage(basedImage)
    basedImg_mask = getImage(basedMask)
    basedImg_mask = cv2.cvtColor(basedImg_mask, cv2.COLOR_BGR2GRAY)
    _, basedImg_mask = cv2.threshold(basedImg_mask, 150, 255, cv2.THRESH_BINARY) # 255->white

    # resize image and get reverse mask
    basedImg = cv2.resize(basedImg, resize) 
    basedImg_mask = cv2.resize(basedImg_mask, resize) 
    basedImgBack_mask = cv2.bitwise_not(basedImg_mask)
    
    # resize texture image to fix the based, according to the larger ratio
    textureImg = getImage(textureImage)
    Ht, Wt, _ = textureImg.shape
    x1, x2, y1, y2 = getROI(basedImg_mask)
    H_ROI = np.ceil(x2 - x1)
    W_ROI = np.ceil(y2 - y1)
    ratio = np.maximum(H_ROI / Ht, W_ROI / Wt)
    H_resize, W_resize = int(Ht * ratio), int(Wt * ratio)
    textureImg = cv2.resize(textureImg, (W_resize, H_resize))

    # get target region of texture
    diff_H = int((H_resize - H_ROI) / 2)
    diff_W = int((W_resize - W_ROI) / 2)
    xt1, yt1 = diff_H, diff_W
    xt2, yt2 = int(xt1 + H_ROI), int(yt1 + W_ROI)

    # offset the mask 
    offsetMask = np.zeros(basedImg_mask.shape, dtype=np.uint8) 
    offsetMask[offset:, offset:] = basedImg_mask[:-offset, :-offset] 

    # blur target based img
    blurBasedImg = cv2.cvtColor(basedImg.copy(), cv2.COLOR_BGR2GRAY)
    blurBasedImg = cv2.blur(blurBasedImg, (blur, blur))
    blurBasedImg = cv2.bitwise_and(blurBasedImg, blurBasedImg, mask=offsetMask)

    # transform textImg according to offset mask
    textureImg = transformT(textureImg, blurBasedImg[x1+offset:x2+offset, y1+offset:y2+offset])
    # textureImg = textureImg[xt1:xt2, yt1:yt2]

    # get blend mask
    background = getBackgroundColorRange(basedImg.copy(), basedImgBack_mask)
    greyBody = cv2.cvtColor(basedImg.copy(), cv2.COLOR_BGR2GRAY)
    bgrBody = cv2.cvtColor(greyBody, cv2.COLOR_GRAY2BGR)
    mask = getBlendMask(greyBody, background, a)
    cv2.imwrite("blend_mask.jpg", mask * 255)
    
    # blend two images
    blend_front_img = basedImg.copy() * mask
    blend_front_img[x1:x2, y1:y2] += textureImg * (1 - mask[x1:x2, y1:y2])
    blend_front_img = cv2.bitwise_and(blend_front_img, blend_front_img,  mask=basedImg_mask)

    # use mask to construct the result img
    blend_back_img = cv2.bitwise_and(basedImg, basedImg,  mask=basedImgBack_mask)
    blend_img = blend_back_img + blend_front_img
    # body = basedImg[x1:x2,y1:y2,:]

    return blend_img

def getRenderResult(basedImagePath:str, basedImageMaskPath:str, textureImagePath:str, a=0.5, offset=2, blur=3):
    renderImg = blendImage(basedImagePath, basedImageMaskPath, textureImagePath, a=a, offset=offset, blur=blur)
    print("Render {} on {} success!".format(basedImagePath, textureImagePath))
    return renderImg

