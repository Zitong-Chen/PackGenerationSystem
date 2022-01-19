import os

all_file_list = []
n = 1
path = os.path.join(os.getcwd(), "static/materials/style3")
for x in os.listdir(path):
    f = os.path.join(path, x)
    if os.path.isfile(f):
        old_name = path+os.sep+x
        fn, ext = os.path.splitext(x)
        new_name = path+os.sep+str(n)+ext
        os.rename(old_name, new_name)
        print("Replace {} with {}".format(old_name, new_name))
        n += 1