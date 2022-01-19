from enum import Enum

class TEXT_POS(Enum):
    # oriention & pos
    HORIZONTAL_TOP = 0
    HORIZONTAL_MIDDLE = 1
    HORIZONTAL_BOTTOM = 2
    VERTICAL_LEFT = 3
    VERTICAL_MIDDLE = 4
    VERTICAL_RIGHT = 5

class PROD_POS(Enum):
    # vertical position & horizontal postion
    TOP_MIDDLE = 0
    MIDDLE_MIDDLE = 1
    BOTTOM_MIDDLE = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    MIDDLE_RIGHT = 5

def get_single_text_pos(type:TEXT_POS, back_img):
    Hb, Wb = back_img.shape[0], back_img.shape[1]
    # Ht, Wt = text_size[1], text_size[0]
    if type == TEXT_POS.HORIZONTAL_TOP:
        # Type 0: text at top
        height_pos = Hb // 4
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == TEXT_POS.HORIZONTAL_MIDDLE:
        # Type 1: text at center
        height_pos = Hb // 2
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == TEXT_POS.HORIZONTAL_BOTTOM:
        # Type 2: text at bottom
        height_pos = 3 * Hb // 4
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == TEXT_POS.VERTICAL_LEFT:
        # Type 3: text at left, vertically
        height_pos = Hb // 2
        width_pos = Wb // 4 
        return (int(height_pos), int(width_pos))
    elif type == TEXT_POS.VERTICAL_MIDDLE:
        # Type 4: text at middle, vertically
        height_pos = Hb // 2
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == TEXT_POS.VERTICAL_RIGHT:
        # Type 4: text at right, vertically
        height_pos = Hb // 2
        width_pos = 3 * Wb // 4 
        return (int(height_pos), int(width_pos))
    else:
        # Undefined type
        pass
    
def get_prod_pos(type:PROD_POS, back_img):
    Hb, Wb = back_img.shape[0], back_img.shape[1]
    # Hp, Wp = prod_img.shape[0], prod_img.shape[1]
    if type == PROD_POS.TOP_MIDDLE:
        # Type 0: text at top
        height_pos = Hb // 4
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == PROD_POS.MIDDLE_MIDDLE:
        # Type 1: prod at center
        height_pos = Hb // 2
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == PROD_POS.BOTTOM_MIDDLE:
        # Type 2: prod at bottom
        height_pos = 3 * Hb // 4
        width_pos = Wb // 2 
        return (int(height_pos), int(width_pos))
    elif type == PROD_POS.BOTTOM_LEFT:
        # Type 3: prod at bottom left
        height_pos = 3 * Hb // 4
        width_pos = Wb // 4 
        return (int(height_pos), int(width_pos))
    elif type == PROD_POS.BOTTOM_RIGHT:
        # Type 4: prod at bottom right
        height_pos = 3 * Hb // 4
        width_pos = 3 * Wb // 4
        return (int(height_pos), int(width_pos))
    elif type == PROD_POS.MIDDLE_RIGHT:
        # Type 4: prod at middle right
        height_pos = Hb // 2
        width_pos = 3 * Wb // 4
        return (int(height_pos), int(width_pos))
    else:
        # Undefined type
        pass


