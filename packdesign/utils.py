from io import BytesIO
import os
from numpy.core.fromnumeric import ndim
import random

import torch
from torchvision.utils import save_image
from torch.autograd import Variable
import numpy as np
from PIL import Image
from werkzeug.wrappers import PlainRequest
import base64
import cv2

from .CGAN import Generator

basedir = os.path.abspath(os.path.dirname(__file__))

IMG_CHANNEL = 3
IMG_WIDTH = 512
IMG_HEIGHT = 512

N_CLASS = 3
LATENT_DIM = 512
D = 128
MODEL_PATH = "models"
STYLES = ["style1", "style2", "style3"]

def get_random_model_path(style:str, static:str):
    if style in STYLES:
        style_model_path = os.path.join(os.path.join(static, MODEL_PATH), style)
        model_list = []
        for x in os.listdir(style_model_path):
            if ".pb" in x:
                model_list.append(os.path.join(style_model_path, x))
        random.shuffle(model_list)
        return model_list[0]
    else:
        print("Wrong style input!")

def load_GAN_generator(style:str, static_path:str, channel:int, latent_dims:int, d:int) -> Generator:
    generator=Generator(C=channel, latent_dim=latent_dims, n_class=N_CLASS, d=d)
    generator.load_state_dict(torch.load(get_random_model_path(style, static_path)))
    return generator

def get_noise(nums:int, latent_dim:int):
    noise = Variable(torch.FloatTensor(np.random.normal(0, 1, (nums, latent_dim, 1, 1))))
    return noise


def get_base_label_for_N_class():
    y_ = torch.LongTensor(np.array([num for num in range(N_CLASS)])).view(N_CLASS,1)
    y_fixed = torch.zeros(N_CLASS, N_CLASS)
    y_fixed = Variable(y_fixed.scatter_(1,y_.view(N_CLASS,1),1).view(N_CLASS, N_CLASS,1,1))
    return y_fixed


def normalize_img(img_array):
    # get dims of img_array
    if img_array.ndim == 4:
        for i in range(img_array.shape[0]):
            for c in range(img_array.shape[-1]):
                max_num = np.max(np.max(img_array[i,:,:,c], axis=0), axis=0)
                min_num = np.min(np.min(img_array[i,:,:,c], axis=0), axis=0)
                img_array[i,:,:,c] = (img_array[i,:,:,c] - min_num) / (max_num - min_num)
    elif img_array.ndim == 3:
        for c in range(img_array.shape[-1]):
            max_num = np.max(np.max(img_array[:,:,c], axis=0), axis=0)
            min_num = np.min(np.min(img_array[:,:,c], axis=0), axis=0)
            img_array[:,:,c] = (img_array[:,:,c] - min_num) / (max_num - min_num)
    return img_array


def generate_image(style:str, static_path:str, nums:int=3):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Device: {}, Style: {}".format(device, style))
    with torch.no_grad():
        gen_imgs_list = []
        for i in range(nums):
            generator = load_GAN_generator(style, static_path, IMG_CHANNEL, LATENT_DIM, D)
            base_labels = get_base_label_for_N_class()
            labels = torch.cat([torch.FloatTensor(torch.randn((N_CLASS,1))).view(1, N_CLASS, 1, 1), base_labels], 0)
            noises = get_noise(labels.shape[0], LATENT_DIM).to(device)
            generator.to(device)
            gen_imgs = generator(noises, labels).view(-1,IMG_CHANNEL,IMG_HEIGHT,IMG_WIDTH)
            # normalize target img
            gen_img_array = np.array([img.cpu().numpy().T for img in gen_imgs.data])
            norm_img = normalize_img(gen_img_array) * 255
            gen_imgs_list.append(norm_img[0])
    torch.cuda.empty_cache()
    return gen_imgs_list


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['png', 'jpg', 'jpeg', 'gif']

def get_random_file_name(path, size:int):
    all_file_list = []
    for x in os.listdir(path):
        f = os.path.join(path, x)
        if os.path.isfile(f):
            all_file_list.append(x)
    
    random.shuffle(all_file_list)
    if size > len(all_file_list):
        print("Size is greater than length of files. Get all files.")
        size = len(all_file_list)
    return all_file_list[:size]


# ----------------- base64, PIL, OpenCV Conversion ---------------------
# source: https://www.jb51.net/article/178106.htm
def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return image


def cv2_base64(image, f='.jpg'):
    base64_str = cv2.imencode(f, image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image

