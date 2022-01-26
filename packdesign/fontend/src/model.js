const R_INDEX = 0;
const G_INDEX = 1;
const B_INDEX = 2;

export default class UserModel {
    // isExist = false;

    constructor() {
        this.back_style = {
            select_background: 0,
            single_color: [0, 0, 0],
            gan_style: 0,
            gan_gen_result: [""],
            adjust_params: [0, 0, 0, 0],
            upload_img_url: "",
        };

        this.items = {
            text: "",
            prod_src: "",
            template_result:[],
            color_result:[]
        }

        this.design_setting = {
            url: "",
            // transport params
        }
    }

    // get isExist() {
    //     return this.isExist;
    // }

    // set isExist(exist) {
    //     this.isExist = exist;
    // }

    // ===========background============
    get select_background() {
        return this.back_style.select_background;
    }

    set select_background(selection) {
        this.back_style.select_background = selection;
    }

    get single_color() {
        return this.back_style.single_color;
    }

    get single_color_R() {
        return this.back_style.single_color[R_INDEX];
    }

    set single_color_R(new_color_R) {
        this.back_style.single_color[R_INDEX] = new_color_R >= 0 ? new_color_R : 0;
        this.back_style.single_color[R_INDEX] = new_color_R <= 255 ? new_color_R : 255;
    }

    get single_color_G() {
        return this.back_style.single_color[G_INDEX];
    }

    set single_color_G(new_color_G) {
        this.back_style.single_color[G_INDEX] = new_color_G >= 0 ? new_color_G : 0;
        this.back_style.single_color[G_INDEX] = new_color_G <= 255 ? new_color_G : 255;
    }

    get single_color_B() {
        return this.back_style.single_color[B_INDEX];
    }

    set single_color_B(new_color_B) {
        this.back_style.single_color[B_INDEX] = new_color_B >= 0 ? new_color_B : 0;
        this.back_style.single_color[B_INDEX] = new_color_B <= 255 ? new_color_B : 255;
    }

    get gan_style() {
        return this.back_style.gan_style;
    }

    set gan_style(new_style) {
        this.back_style.gan_style = new_style;
    }

    get gan_gen_result() {
        return this.back_style.gan_gen_result;
    }

    set gan_gen_result(new_result) {
        this.back_style.gan_gen_result = new_result;
    }

    get adjust_params() {
        return this.back_style.adjust_params;
    }

    set adjust_params(new_params) {
        if (new_params.length === this.back_style.adjust_params.length) {
            for (let i = 0; i < new_params.length; ++i) {
                this.back_style.adjust_params[i] = new_params[i] >= 0 ? new_params[i] : 0;
                this.back_style.adjust_params[i] = new_params[i] <= 100 ? new_params[i] : 100;
            }
        }
    }

    get upload_img_url() {
        return this.back_style.upload_img_url;
    }
    
    set upload_img_url(new_url) {
        this.back_style.upload_img_url = new_url;
    }

    
    // ===========text & prod============

    get text() {
        return this.items.text;
    }

    set text(new_text) {
        this.items.text = new_text;
    }

    get prod_src() {
        return this.items.prod_src;
    }

    set prod_src(new_prod) {
        this.items.prod_src = new_prod;
    }

    get template_result() {
        return this.items.template_result;
    }

    set template_result(new_temps) {
        this.items.template_result = new_temps;
    }

    get color_result() {
        return this.items.color_result;
    }

    set color_result(new_colors) {
        this.items.color_result = new_colors;
    }

    // ===========design url============

    get img_src() {
        return this.design_setting.url;
    }

    set img_src(new_src) {
        this.design_setting.url = new_src;
    }
}