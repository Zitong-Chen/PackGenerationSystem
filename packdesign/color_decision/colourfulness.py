import copy
from typing import Any, Callable
import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from . import GA

from ..template_decision import assemble
from ..template_decision.item_pos import TEXT_POS

def get_img_with_cv2(filename):
    return cv2.imread(filename, flags=cv2.IMREAD_COLOR)

def get_img_with_PIL(filename):
    return Image.open(filename)

def get_colorfulness1(img):
    img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    (L, U, V) = cv2.split(img_luv.astype('float'))

    # compute saturation, 0?
    chroma = np.array((U, V))
    lightness = np.array((L, L))

    saturation = np.divide(U, L + 1) + np.divide(V, L + 1)

    # compute colourfulness index
    colorfulness = np.mean(saturation) + np.std(saturation)

    return colorfulness

def get_colorfulness2(img):
    (B, R, G) = cv2.split(img.astype("float"))

    # compute rg and yb
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)

    # compute mean and standard deviation
    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)

    std_rg =  np.std(rg)
    std_yb = np.std(yb)

    # compute the final mean and std
    sigama_rgyb = np.sqrt(mean_rg**2 + mean_yb**2)
    mu_rgyb = np.sqrt(std_rg**2 + std_yb**2)

    #compute the colourfulness index
    colorfulness = sigama_rgyb + 0.3 * mu_rgyb

    return colorfulness


def get_color_gene_by_GA(eval_img, text:str, pos_code:TEXT_POS, font_style, font_size, 
init_pops:int, selection_pops:int, mutation_rate:float, generation:int, final_pops:int, eval: Callable[[Any], float]):
    print("Starting matching text colors by GA....")
    pops = GA.init_pops(init_pops)
    for e in range(generation):
        fitness = [pop.fitness(eval_img, text, pos_code, font_style, font_size, eval) for pop in pops]
        pops = GA.selection(pops, fitness, selection_pops)
        pops = GA.crossover(pops)
        pops = GA.mutation(pops, mutation_rate)
    tops = GA.selection(pops, fitness, final_pops)
    tops_BGR = [pop.BGR_tuple() for pop in tops]
    print("GA Done!")
    return tops_BGR

