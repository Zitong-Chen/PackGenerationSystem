from typing import Any, Callable, List, Tuple
import cv2
import numpy as np
import random
import copy
from ..template_decision import assemble
from ..template_decision.item_pos import TEXT_POS, PROD_POS 

class ColorGene:
    def __init__(self) -> None:
        self.R = random.randint(0, 255)
        self.G = random.randint(0, 255)
        self.B = random.randint(0, 255)

    def __str__(self) -> str:
        return f"Color Gene: (R: {self.R}, G: {self.G}, B: {self.B})"

    def mutation(self):
        position = random.randint(0, 2)
        if position == 0:
            self.R = random.randint(0, 255)
        if position == 1:
            self.G = random.randint(0, 255)
        if position == 2:
            self.B = random.randint(0, 255)
    
    def fitness(self, img, text, pos_code:TEXT_POS, font_style, font_size, eval: Callable[[Any], float]) -> float:
        text_pos = assemble.get_single_text_pos(pos_code, img)
        text_orientation = assemble.HORIZONTAL
        if pos_code in [TEXT_POS.VERTICAL_LEFT, TEXT_POS.VERTICAL_MIDDLE, TEXT_POS.VERTICAL_RIGHT]:
            text_orientation = assemble.VERTICAL
        text_mask, text_back_mask = assemble.get_text_mask_from_PIL(img.shape, text_pos, text, font_style, font_size, text_orientation)
        target_img = assemble.add_text(img, text_mask, text_back_mask, (self.R, self.G, self.B))
        c_with_text = eval(target_img) 
        c_original = eval(copy.deepcopy(img))
        return np.abs(c_with_text / c_original - 1)
    
    def RGB_tuple(self) -> Tuple:
        return (self.R, self.G, self.B)
    
    def BGR_tuple(self) -> Tuple:
        return (self.B, self.G, self.R)

def init_pops(pops_size: int) -> List[ColorGene]:
    pops = list()
    for i in range(pops_size):
        pops.append(ColorGene())
    return pops


def selection(pops: List[ColorGene], fitness, parenent_nums: int) -> List[ColorGene]:
    # pops: popspulation to be operated on
    # fitness: fitness value caculated on pops
    # parenent_nums: numbers of parenent genes to be crossovered
    new_pops = np.empty(parenent_nums, dtype=ColorGene)
    fitness_copy = np.copy(fitness)
    for i in range(parenent_nums):
        max_idx = np.where(fitness_copy == np.min(fitness_copy))
        max_idx = max_idx[0][0]
        new_pops[i] = pops[max_idx]
        fitness_copy = np.delete(fitness_copy, max_idx, axis=0)
    return new_pops.tolist()

def crossover(pops: List[ColorGene]) -> List[ColorGene]:
    offsprings = list()
    for i in range(0, len(pops), 2):
        if (i + 1) < len(pops):
            # if flag equals to 0, do no switch
            # else switch one color channel, and add new offspring in pops
            flag = random.randint(0, 3) 
            offspring1 = copy.deepcopy(pops[i])
            offspring2 = copy.deepcopy(pops[i + 1])
            if flag == 0:
                temp = offspring1.R
                offspring1.R = offspring2.R
                offspring2.R = temp
            if flag == 1:
                temp = offspring1.G
                offspring1.G = offspring2.G
                offspring2.G = temp
            if flag == 2:
                temp = offspring1.B
                offspring1.B = offspring2.B
                offspring2.B = temp
            offsprings.append(offspring1)
            offsprings.append(offspring2)
    for item in offsprings:
        pops.append(item)
    return pops
    

def mutation(pops: List[ColorGene], mu_rate = 0.2) -> List[ColorGene]:
    for i in range(len(pops)):
        mu_flag = random.random()
        if mu_flag < mu_rate:
            pops[i].mutation()
    return pops

