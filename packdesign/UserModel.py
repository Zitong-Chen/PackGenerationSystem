class UserModel():

    def __init__(self) -> None:
        # ===== Background =====
        self.__back_selection = 0
        # 0 => Single Color
        self.__single_color = [0, 0, 0] # R, G, B

        # 1 => GAN Generate 
        self.__gan_style = None
        self.__gan_gen_result = None
        self.__adjust_params = [0, 0, 0, 0] # Blur, Abstract, Particle, Tranparent

        # 2 => Upload Pic
        self.__upload_img_url = None


    # Back Style
    def get_back_style(self):
        return self.__back_selection
    def set_back_style(self, back_style):
        if back_style in range(0, 3):
            self.__back_selection = back_style
        else:
            pass
    
    # Single Color
    def get_single_color(self):
        return self.__single_color
    def set_single_color(self, new_color):
        if len(new_color) == len(self.__single_color):
            for i in range(0, len(new_color)):
                self.__single_color = max(0, new_color[i])
                self.__single_color = min(255, new_color[i])
        else:
            pass
        
    # GAN Style
    def get_gan_style(self):
        return self.__gan_style
    def set_gan_style(self, new_style):
        self.__gan_style = new_style

    def get_gan_gen_result(self):
        return self.__gan_gen_result
    def set_gan_gen_result(self, new_result):
        self.__gan_gen_result = new_result
    
    def get_adjust_params(self):
        return self.__adjust_params
    def set_adjust_params(self, new_params):
        if len(new_params) == len(self.__adjust_params):
            for i in range(0, len(new_params)):
                self.__adjust_params = max(0, new_params[i])
                self.__adjust_params = min(100, new_params[i])
        else:
            pass

    # Upload Img
    def get_upload_img_url(self):
        return self.__upload_img_url
    def set_upload_img_url(self, new_url):
        self.__upload_img_url = new_url
    