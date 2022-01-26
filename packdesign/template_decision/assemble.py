import os
from typing import List, Tuple
import cv2
import copy
from PIL import ImageDraw, ImageFont, Image

import numpy as np
from numpy.lib.type_check import imag
from numpy.random import randn
from numpy.random.mtrand import randint
from .item_pos import get_prod_pos, get_single_text_pos, PROD_POS, TEXT_POS

from . import visual_clutter

HORIZONTAL = 0
VERTICAL = 1
INITIAL_WIDTH = 512
INITIAL_HEIGHT = 512
INITAL_CHANNEL = 3

TEXT_PROD_TEMPLATES = [
    (0,1),(0,2),(0,4),(1,1),(1,4),(2,5),(4,1),(3,1),(5,1),(5,2)
]

TEXT_TEMPLATES = [
    0, 1, 2, 3, 4, 5
]

def get_text_orientation(text_pos_code: TEXT_POS):
    text_orientation = HORIZONTAL
    if text_pos_code in [TEXT_POS.VERTICAL_LEFT, TEXT_POS.VERTICAL_MIDDLE, TEXT_POS.VERTICAL_RIGHT]:
        text_orientation = VERTICAL
    return text_orientation


def get_text_mask_from_PIL(backimg_shape:Tuple, center_pos:Tuple, text:str, font, text_size, orientation=HORIZONTAL):
    # image_shape get from cv2 img
    Hb, Wb, Cb = backimg_shape[0], backimg_shape[1], backimg_shape[2]

    img_array = np.zeros((Wb, Hb, Cb), np.uint8)
    new_img = Image.fromarray(img_array)
    draw_text = ImageDraw.Draw(new_img)

    # text font
    font_style = ImageFont.truetype(font, text_size)

    # get text mask
    if orientation == HORIZONTAL:
        width, height = draw_text.textsize(text, font_style)
        if width >= Wb or height >= Hb:
            print("Too large font size!")
            return
        top, _, left, _ = target_region_at_img1(backimg_shape, (height, width), center_pos)
        draw_text.text((left, top), text, (255, 255, 255), font=font_style)

    if orientation == VERTICAL:
        width, height = 0, 0
        for _, ch in enumerate(text):
            w, h = draw_text.textsize(ch, font_style)
            width = np.maximum(w, width)
            height += h
        top, _, left, _ = target_region_at_img1(backimg_shape, (height, width), center_pos)
        for _, ch in enumerate(text):
            _, h = draw_text.textsize(ch, font_style)
            draw_text.text((left, top), ch, (255, 255, 255), font=font_style)
            top += h
    
    text_mask = cv2.cvtColor(np.asanyarray(new_img), cv2.COLOR_RGB2GRAY)
    ret, text_mask = cv2.threshold(text_mask, 150, 255, cv2.THRESH_BINARY) # 255->white
    back_mask = cv2.bitwise_not(text_mask)
    return text_mask, back_mask

def add_text(back_img, text_mask, back_mask, color: Tuple):
    # image_shape get from cv2 img
    Hb, Wb, Cb = back_img.shape[0], back_img.shape[1], back_img.shape[2]

    # get font color background
    text_color = np.ones((Hb, Wb, Cb), np.uint8)
    for i in range(Cb):
        text_color[:,:,i] *= color[i]
    text_color = np.array(text_color, dtype=np.uint8)

    # put text on img using text_mask
    back_copy = copy.deepcopy(back_img)  #get img copy
    targ_text = cv2.bitwise_and(text_color, text_color, mask=text_mask) 
    targ_back = cv2.bitwise_and(back_copy, back_copy, mask=back_mask)
    targ_img = cv2.add(targ_back, targ_text)
    return targ_img
    

def target_region_at_img1(img1_shape:Tuple, img2_shape:Tuple, center_pos:Tuple):
    # get region of target position when centering at center_pos
    cx, cy = center_pos[0], center_pos[1]
    H1, W1 = img1_shape[0], img1_shape[1]
    H2, W2 = img2_shape[0], img2_shape[1]

    x1, y1 = int(cx - H2/2), int(cy - W2/2)
    x2, y2 = int(x1 + H2), int(y1 + W2)
    # when the region oversize 
    if x2 >= H1:
        x1, x2 = H1 - 1 - H2, H1
    if y2 >= W1:
        y1, y2 = W1 - 1 - W2, W1
    return x1, x2, y1, y2

def add_product(back_img, prod_img, center_pos: Tuple):
    # resize product image
    Hb, Wb, Cb = back_img.shape
    Hp_, Wp_, Cp = prod_img.shape

    Hp = int(Hb//3 * 0.8)
    Wp = int(Hp * Wp_ / Hp_)
    prod_img = cv2.resize(prod_img, (Wp, Hp)) 

    # get mask for RGB or RGBA product img
    if Cp == 4: # RGBA
        prod_mask = prod_img[:,:,3]
        prod_img = prod_img[:,:,:3]
        
    elif Cp == 3: # RGB
        prod_mask = np.array(np.ones((int(Hp), int(Wp))) * 255, dtype=np.uint8)
    else: # Something wrong
        print("Invalid Input!")
        return
    
    # get binary prod mask and reverse to get back mask
    ret, prod_mask = cv2.threshold(prod_mask, 150, 255, cv2.THRESH_BINARY) # 255->white
    back_mask = cv2.bitwise_not(prod_mask)
    # get region of target position when centering at center_pos
    x1, x2, y1, y2 = target_region_at_img1(back_img.shape, prod_img.shape, center_pos)
    # mix two imgs at (x1, y1)-(x2, y2)
    img_copy = copy.deepcopy(back_img)  #get img copy
    targ_region = back_img[x1:x2, y1:y2]
    targ_prod = cv2.bitwise_and(prod_img, prod_img, mask=prod_mask) 
    targ_back = cv2.bitwise_and(targ_region, targ_region, mask=back_mask)
    img_copy[x1:x2, y1:y2] = cv2.add(targ_back, targ_prod)

    # get whole pic mask
    whole_prod_mask = np.zeros((int(Hb), int(Wb)), dtype=np.uint8)
    whole_prod_mask[x1:x2, y1:y2] = prod_mask
    ret, whole_prod_mask = cv2.threshold(whole_prod_mask, 150, 255, cv2.THRESH_BINARY) # 255->white
    whole_back_mask = cv2.bitwise_not(whole_prod_mask)

    return img_copy, whole_prod_mask, whole_back_mask

def assemble_text_prod(back_img, text, font_style, font_size, text_color:Tuple, text_pos_code:TEXT_POS, prod_img=None, prod_pos_code:PROD_POS=None):
    prod_mask, prod_back_mask = None, None
    if prod_img is not None:
        prod_pos = get_prod_pos(prod_pos_code, back_img)
        back_img, prod_mask, prod_back_mask = add_product(back_img, prod_img, prod_pos)
    text_pos = get_single_text_pos(text_pos_code, back_img)
    text_orientation = get_text_orientation(text_pos_code)
    text_mask, text_back_mask = get_text_mask_from_PIL(back_img.shape, text_pos, text, font_style, font_size, text_orientation)
    target_img = add_text(back_img, text_mask, text_back_mask, text_color)

    return target_img, text_mask, text_back_mask, prod_mask, prod_back_mask

def mat_back_img(back_img, text_back_mask, prod_back_mask=None):
    # get back_img matting with text and prod 
    back_copy = copy.deepcopy(back_img)  #get img copy
    targ_back = cv2.bitwise_and(back_copy, back_copy, mask=text_back_mask)
    if prod_back_mask is not None:
        targ_back = cv2.bitwise_and(targ_back, targ_back, mask=prod_back_mask)
    return targ_back
    

def combine_templates(f, text, prod=None):
    # get background
    file_name, ext = os.path.splitext(os.path.split(f)[-1])
    background = cv2.imread(f, cv2.IMREAD_COLOR)
    font_style = "packdesign/static/fonts/SimHei.ttf"
    font_size = 72

    template_list = []
    if prod is not None:
        for text_pos_code, prod_pos_code in TEXT_PROD_TEMPLATES:
            # get prod
            prod_pos = get_prod_pos(PROD_POS(prod_pos_code), background)
            back_img, prod_mask, prod_back_mask = add_product(background, prod, prod_pos)
            # get text
            text_pos = get_single_text_pos(TEXT_POS(text_pos_code), back_img)
            text_orientation = get_text_orientation(TEXT_POS(text_pos_code))
            text_mask, text_back_mask = get_text_mask_from_PIL(back_img.shape, text_pos, text, font_style, font_size, text_orientation)
            # target, _, text_back_mask, _, prod_back_mask = assemble_text_prod(background, text, "packdesign/static/fonts/SimHei.ttf", 
            #     68, (94,94,94), TEXT_POS(text_pos_code), prod, PROD_POS(prod_pos_code))
            target_back = mat_back_img(back_img, text_back_mask, prod_back_mask)
            template_list.append((target_back, text_pos_code, prod_pos_code))
    else:
        for text_pos_code in TEXT_TEMPLATES:
             # get text
            text_pos = get_single_text_pos(TEXT_POS(text_pos_code), background)
            text_orientation = get_text_orientation(TEXT_POS(text_pos_code))
            text_mask, text_back_mask = get_text_mask_from_PIL(background.shape, text_pos, text, font_style, font_size, text_orientation)
            # target, _, text_back_mask, _, prod_back_mask = assemble_text_prod(background, text, "packdesign/static/fonts/SimHei.ttf", 
            #     68, (94,94,94), TEXT_POS(text_pos_code), prod, PROD_POS(prod_pos_code))
            target_back = mat_back_img(background, text_back_mask)
            template_list.append((target_back, text_pos_code, -1))

    return template_list

def sort_templates(f_list:List, base_dir):
    scores = []
    for f in f_list:
        # temp_score = visual_clutter.get_feature_congestion(os.path.join(base_dir, f))
        temp_score = randint(0,10)
        scores.append((f, temp_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    template_list = [item[0] for item in scores]
    
    return template_list
