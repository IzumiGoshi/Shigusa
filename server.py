import os
import shutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
import random
import urllib 

# ---> uvicorn server:app --port 8123

app = FastAPI()

def load_image_bytes(fpath):
    with open(fpath, 'rb') as f: img = f.read()
    return img


def image_walker(walker_path):
    image_files = []
    img_exts = ['jpg', 'jpeg', 'png']
    for root, dirs, files in os.walk(walker_path, topdown=False):
        for f in files:
            if '.' not in f: continue
            if f.split('.')[-1] not in img_exts: continue
            image_files.append(os.path.join(root, f))
    print('----> ', len(image_files))
    return image_files


DEFAULT_IMG_PATH = '/home/chris/Documents/ART/saved art/super favorites V2'
SAVE_DIR = '/home/chris/Documents/Programming/Shigusa/saves'
CURRENT = ''
images = image_walker(DEFAULT_IMG_PATH)
history = []
hist_back = 0


@app.get("/", response_class=HTMLResponse)
def api_get():
    with open('index.html', 'rb') as f: return f.read()


@app.get('/randimg/{key}')
def get_next(key: str):
    global images
    global history
    global CURRENT
    img = random.choice(images)
    CURRENT = img
    print(img)
    history.append(img)
    imgbytes = load_image_bytes(img)
    med_type = "image/" + img.split('.')[-1]
    return Response(content=imgbytes, media_type=med_type)


@app.get('/previmg/{key}')
def get_prev(key: str):
    global history
    global CURRENT
    history.pop(-1)
    img = history[-1]
    CURRENT = img
    print(img)
    imgbytes = load_image_bytes(img)
    med_type = "image/" + img.split('.')[-1]
    return Response(content=imgbytes, media_type=med_type)


@app.get('/setdir/{direc}')
def setdir(direc: str):
    global images
    direc = direc.replace('_|_|_|_', '/')
    print('\n\n----> ', direc, '\n\n')
    images = image_walker(direc)
    return Response(content="ok", media_type="text")


@app.get('/save')
def saveimg():
    global CURRENT
    fname = os.path.split(CURRENT)[-1]
    shutil.copy(CURRENT, os.path.join('save', fname))

    return Response(content="ok", media_type="text")


@app.get('/delete')
def deleteimg():
    '''
        Need a way to undo....
    '''
    return Response(content="ok", media_type="text")



# uvicorn server:app --port 8123

