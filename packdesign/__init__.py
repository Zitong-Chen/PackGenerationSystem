import os
from posixpath import join
from PIL.Image import Image
from flask import Flask, render_template, redirect, request, jsonify
from flask.globals import session
from flask.helpers import send_from_directory, url_for
import json
import numpy as np
import cv2
import base64
from numpy.core.fromnumeric import prod, size
from numpy.core.numeric import full
import torch
from torch import argsort
from werkzeug.utils import secure_filename
import time

from torch.functional import align_tensors

from packdesign.template_decision import assemble
from packdesign.template_decision.item_pos import PROD_POS, TEXT_POS
from . import utils
from .template_decision import assemble
from .color_decision import colourfulness
from .blending import blending

GENERATE_IMG_KEY = "GENERATE_IMG"
TEMPLATE_IMG_KEY = "TEMPLATE_IMG"
COLOR_IMG_KEY = "COLOR_IMG"
USER_DATA_KEY = "USER_DATA"
USER_SESSION = "user"
TEMP_POS_KEY = 'TEMP_POS_JSON'
IMG_SHAPE = (512, 512, 3)
MATERIALS_KEY = "MATERIALS_IMG"
RENDER_IMG = "RENDER_IMG"
RENDER_MODEL = "RENDER_MODEL"

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_folder='fontend/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        USER_DATA='user_data',
        GENERATE_IMG='generate_img',
        TEMPLATE_IMG='template_img',
        COLOR_IMG='color_img',
        RENDER_IMG='render_img',
        RENDER_MODEL='render_model',
        TEMP_POS_JSON='pos.json',
        MATERIALS_IMG='materials',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # sample page
    @app.route('/')
    def get_home():
        session['user'] = int(time.time())
        # session['user_data'] = UserModel() 
        base_path = os.path.join(app.static_folder, app.config[USER_DATA_KEY])
        user_path = os.path.join(base_path, str(session.get(USER_SESSION)))
        os.makedirs(os.path.join(user_path, app.config[GENERATE_IMG_KEY]), exist_ok=True)
        os.makedirs(os.path.join(user_path, app.config[TEMPLATE_IMG_KEY]), exist_ok=True)
        os.makedirs(os.path.join(user_path, app.config[COLOR_IMG_KEY]), exist_ok=True)
        os.makedirs(os.path.join(user_path, app.config[RENDER_IMG]), exist_ok=True)

        return redirect(url_for('show_index'), code=301)

    @app.route('/index')
    def show_index():
        return render_template('index.html')
    
    @app.route('/materials', methods=['GET', 'POST'])
    def get_random_materials():
        if request.method == "GET":
            materials_path = os.path.join(app.static_folder, app.config[MATERIALS_KEY])
            img_list = []
            for style in utils.STYLES:
                imgs = utils.get_random_file_name(os.path.join(materials_path, style), 3)
                imgs = ["{}/{}".format(style, i) for i in imgs]
                img_list.extend(imgs)
            data = {"status": True, "img": img_list, "base_dir": os.path.join('static', app.config[MATERIALS_KEY]) + '/' }
            return jsonify(**data)



    @app.route('/single-color',methods=['GET', 'POST'])
    def generate_singlecolor():
        if request.method == 'POST':
            R = int(json.loads(request.form.get('R')))
            G = int(json.loads(request.form.get('G')))
            B = int(json.loads(request.form.get('B')))

            BGR_color = (B, G, R)

            # config data path
            user_path = os.path.join(app.config[USER_DATA_KEY], str(session.get(USER_SESSION)))
            gen_path = os.path.join(user_path, app.config[GENERATE_IMG_KEY])
            full_gen_path = os.path.join(app.static_folder, gen_path)

            # image_shape get from cv2 img
            Hb, Wb, Cb = IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2]

            img_list = []
            t = time.time()
            # get font color background
            single_color = np.ones((Hb, Wb, Cb), np.uint8)
            for i in range(Cb):
                single_color[:,:,i] *= BGR_color[i]
            single_color = np.array(single_color, dtype=np.uint8)

            cv2.imwrite(os.path.join(full_gen_path, "single_color" + str(t) + ".jpg"), single_color)
            img_url = "single_color" + str(t) + ".jpg"
            img_list.append(img_url)

            data = {"status": True, "img": img_list, "base_dir": os.path.join('static', gen_path) + '/' }
            return jsonify(**data)
            
            

    @app.route('/generate/style=<int:style>', methods=['GET', 'POST'])
    def generate_background(style):
        if request.method == 'GET':
            # get storge path
            user_path = os.path.join(app.config[USER_DATA_KEY], str(session.get(USER_SESSION)))
            
            gen_path = os.path.join(user_path, app.config[GENERATE_IMG_KEY])
            full_gen_path = os.path.join(app.static_folder, gen_path)
            if not os.path.exists(full_gen_path):
                os.makedirs(full_gen_path, exist_ok=True)

            print(request)
            style_index = style
            print(style_index)

            if style_index < len(utils.STYLES):
                t = int(time.time())
                img_list = []
                count = 0
                # generate style labels and noise
                target_style = utils.STYLES[style_index]
                model_path = '/home/zitong/ThesisSystem/packdesign/static'
                
                gen_imgs = utils.generate_image(target_style, model_path, nums=9)
                for img in gen_imgs:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(os.path.join(full_gen_path, "{}-{}.jpg".format(str(count), str(int(t)))), img)
                    img_url = "{}-{}.jpg".format(str(count), str(int(t)))
                    
                    # retval, buffer = cv2.imencode('.jpg', img)
                    # image_base64 = "data:image/jpeg;base64," + str(base64.b64encode(buffer), encoding='utf-8')
                    # img_list.append(image_base64)
                    img_list.append(img_url)
                    count+=1
                
                data = {"status": True, "img": img_list, "base_dir": os.path.join('static', gen_path) + '/' }
            else:
                data = {"status": False}

            return jsonify(**data)
    
    @app.route('/template', methods=['GET', 'POST'])
    def generate_template():
        if request.method == 'POST':
            text = str(request.form.get('text'))

            # get relative and absolute path of user_data
            user_path = os.path.join(app.config[USER_DATA_KEY], str(session.get(USER_SESSION)))
            gen_path = os.path.join(user_path, app.config[GENERATE_IMG_KEY])
            temp_path = os.path.join(user_path, app.config[TEMPLATE_IMG_KEY])
            full_gen_path = os.path.join(app.static_folder, gen_path)
            full_temp_path = os.path.join(app.static_folder, temp_path)

            if not os.path.exists(full_temp_path):
                os.makedirs(full_temp_path, exist_ok=True)
            
            # TODO:replace different prefix for different format
            prod = request.form.get('prodBase64').split(',')[-1]
            # backimg = cv2.imread(os.path.join(app.static_folder, backurl))

            # get back img
            backurl = str(request.form.get('backurl'))
            back_file = backurl.split("static/")[-1]

            back_path = os.path.join(app.static_folder, back_file)

            if prod is not None and len(prod) != 0:
                prod = utils.base64_cv2(prod)
            else:
                prod = None

            # get template mask
            templates = assemble.combine_templates(back_path, text, prod)
            t = time.time()
           
            img_list = []
            pos_codes = {}
            count = 0
            for temp, text_pos_code, prod_pos_code in templates:
                # save in static path
                temp_file = "{}-{}.jpg".format(str(count), str(int(t)))
                pos_code = (text_pos_code, prod_pos_code)
                cv2.imwrite(os.path.join(full_temp_path, temp_file), temp)
                # retval, buffer = cv2.imencode('.jpg', temp)
                # image_base64 = "data:image/jpeg;base64," + str(base64.b64encode(buffer), encoding='utf-8')
                # img_list.append(image_base64)
                img_list.append(os.path.join(temp_path, temp_file))
                # save text & prod pos info
                pos_codes[temp_file] = pos_code
                count += 1
            
            # store chosen back file & pos code info in json file 
            pos_codes['back_file'] = back_file           
            pos_json = json.dumps(pos_codes)
            json_file = open(os.path.join(full_temp_path, app.config[TEMP_POS_KEY]), 'w')
            json_file.write(pos_json)
            json_file.close()
            sorted_templates = assemble.sort_templates(img_list, app.static_folder)
        
            # reponse POST request
            data = {"status": True, "img": sorted_templates, "base_dir": 'static/'}
            return jsonify(**data)

    @app.route('/upload', methods=['POST'])
    def upload_prod():
        from PIL import Image
        file = request.files.get('file')
        # print(file)
        # filename = request.form.get('filename')
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.static_folder, filename))
            with open(os.path.join(app.static_folder, filename), 'rb') as f:
                image = f.read()
                base64_img = base64.b64encode(image)
                # pil_img = utils.base64_pil(base64_img).resize((utils.IM_SIZE, utils.IM_SIZE), Image.ANTIALIAS).convert(
                #     'RGB')
                # pil_img = utils.crop_and_normalize(pil_img)
                # base64_img = utils.pil_base64(pil_img)
                # # image_base64 = "data:image/jpeg;base64," + str(base64.b64encode(image), encoding='utf-8')
                image_base64 = "data:image/jpeg;base64," + str(base64_img, encoding='utf-8')
                data = {"status": True, "img": image_base64, "url": os.path.join(app.static_folder, filename)}
                return jsonify(**data)
        else:
            data = {"status": False}
            return jsonify(**data) 
    
    @app.route('/color-decision', methods=['GET', 'POST'])
    def generate_textcolor():
        if request.method == 'POST':
            # get relative and absolute path of user_data
            user_path = os.path.join(app.config[USER_DATA_KEY], str(session.get(USER_SESSION)))
            gen_path = os.path.join(user_path, app.config[GENERATE_IMG_KEY])
            temp_path = os.path.join(user_path, app.config[TEMPLATE_IMG_KEY])
            color_path = os.path.join(user_path, app.config[COLOR_IMG_KEY])
            full_gen_path = os.path.join(app.static_folder, gen_path)
            full_temp_path = os.path.join(app.static_folder, temp_path)
            full_color_path = os.path.join(app.static_folder, color_path)

            if not os.path.exists(full_color_path):
                os.makedirs(full_color_path, exist_ok=True)
            
            # get pos json
            pos_json = open(os.path.join(full_temp_path, app.config[TEMP_POS_KEY]), 'r')
            pos_dict = json.load(pos_json)
            pos_json.close()

            # get original gen_img url
            back_file = pos_dict['back_file']
            # backurl = str(request.form.get('backurl'))
            # back_file = os.path.split(backurl)[-1]
            back_path = os.path.join(app.static_folder, back_file)

            # get template url
            template_url = str(request.form.get('template'))

            # get text & prod pos from template
            template_file = os.path.split(template_url)[-1]
            text_pos_code, prod_pos_code = pos_dict[template_file]
            
            text = str(request.form.get('text'))
            prod = request.form.get('prodBase64').split(',')[-1]

            # img_file = os.path.split(backurl)[-1]
            # img_path = os.path.join(app.static_folder, img_file)
            back_img = cv2.imread(back_path, cv2.IMREAD_COLOR)
            font_style = "packdesign/static/fonts/SimHei.ttf"
            font_size = 72

            if prod is not None and len(prod) != 0 and prod_pos_code != -1:
                # get prod
                prod_pos = assemble.get_prod_pos(PROD_POS(prod_pos_code), back_img)
                prod = utils.base64_cv2(prod)
                back_img, prod_mask, prod_back_mask = assemble.add_product(back_img, prod, prod_pos)
            else:
                prod = None

            # get color design using GA
            tops_BGR = colourfulness.get_color_gene_by_GA(back_img, text, TEXT_POS(text_pos_code), font_style, 
            font_size, 32, 8, 0.3, 40, 8, colourfulness.get_colorfulness2)

            t = time.time()
            count = 0
            img_list = []
            # add text and return   
            text_pos = assemble.get_single_text_pos(TEXT_POS(text_pos_code), back_img)
            text_orientation = assemble.get_text_orientation(TEXT_POS(text_pos_code))  
            print(template_url ,text_orientation)    
            text_mask, text_back_mask = assemble.get_text_mask_from_PIL(back_img.shape, text_pos, text, font_style, font_size, text_orientation)
            for BGR in tops_BGR:
                target_img = assemble.add_text(back_img, text_mask, text_back_mask, BGR)
                cv2.imwrite(os.path.join(full_color_path, "{}-{}.jpg".format(str(count), str(int(t)))), target_img)
                img_list.append(os.path.join(color_path, "{}-{}.jpg".format(str(count), str(int(t)))))
                count += 1
        
        data = {"status": True, "img": img_list, "base_dir": 'static/'}
        return jsonify(**data)
    
    @app.route("/render", methods=["POST", "GET"])
    def render_design_on_pack():
        if request.method == "POST":
            user_path = os.path.join(app.config[USER_DATA_KEY], str(session.get(USER_SESSION)))
            gen_path = os.path.join(user_path, app.config[GENERATE_IMG_KEY])
            temp_path = os.path.join(user_path, app.config[TEMPLATE_IMG_KEY])
            color_path = os.path.join(user_path, app.config[COLOR_IMG_KEY])
            render_path = os.path.join(user_path, app.config[RENDER_IMG])
            full_gen_path = os.path.join(app.static_folder, gen_path)
            full_temp_path = os.path.join(app.static_folder, temp_path)
            full_color_path = os.path.join(app.static_folder, color_path)
            full_render_path = os.path.join(app.static_folder, render_path)

            # in case of missing diretory
            if not os.path.exists(full_render_path):
                os.makedirs(full_render_path, exist_ok=True)

            t = time.time()
            img_list = []

            # get target file for render
            final_url = str(request.form.get('image'))
            final_file = final_url.split("static/")[-1]
            final_path = os.path.join(app.static_folder, final_file)

            # render pack design  
            render_model_path = os.path.join(app.static_folder, app.config[RENDER_MODEL])
            render_bag_model = os.path.join(render_model_path, "bag_front.jpg")
            render_bag_model_mask = os.path.join(render_model_path, "bag_mask.jpg")
            render_preview = blending.getRenderResult(render_bag_model, render_bag_model_mask, final_path,a=0.4,offset=2)
            # save image
            cv2.imwrite(os.path.join(full_render_path, "render-{}-{}.jpg".format("bag", str(int(t)))), render_preview)
            img_list.append(os.path.join(render_path, "render-{}-{}.jpg".format("bag", str(int(t)))))
             
        data = {"status": True, "img": img_list, "base_dir": "static/"}
        return jsonify(**data)


    
    return app