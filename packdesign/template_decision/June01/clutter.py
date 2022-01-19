import os
import matlab
import matlab.engine

def get_clutter_SE(filepath: str):
    base_dir = os.path.split(os.path.abspath(__file__))[0]
    eng = matlab.engine.start_matlab()
    eng.addpath(base_dir,  nargout=0)
    SE = eng.getClutter_SE(filepath)  
    eng.exit()
    return SE

def get_clutter_FC(filepath: str):
    base_dir = os.path.split(os.path.abspath(__file__))[0]
    eng = matlab.engine.start_matlab()
    eng.addpath(base_dir,  nargout=0)
    FC = eng.getClutter_FC(filepath)
    eng.exit()
    return FC

