import os
import shutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
import random
import urllib 

# ---> uvicorn server:app --port 8123

app = FastAPI()


images = []
history = []
hist_back = 0


def image_walker(walker_path):
    image_files = []
    for root, dirs, files in os.walk(walker_path, topdown=False):
        for f in files:
            if '.jpg' in f.lower() or '.png' in f.lower() or '.jpeg' in f.lower():
                image_files.append(os.path.join(root, f))
    print('----> ', len(image_files))
    return image_files


def load_dir(dirpath):
    global images
    images = image_walker(dirpath)
load_dir('default directory goes here')


@app.get("/", response_class=HTMLResponse)
def api_get():
    with open('gesture.html', 'rb') as f: return f.read()


def load_image_bytes(fpath):
    with open(fpath, 'rb') as f: img = f.read()
    return img


def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def get_next_image():
    global history
    global hist_back

    if hist_back == 1: 
        fpath = random.choice(images)
        history.append(fpath)
    else:
        fpath = history[-1 * hist_back]

    dirname, fname = os.path.split(fpath)
    print(fname, '   ', fpath)
    return load_image_bytes(fpath)


@app.get('/image/{key}')
def get_image(key: str):
    global history
    global hist_back

    if key.startswith('xprev'):
        hist_back = hist_back + 1

    else:
        hist_back = hist_back - 1

    hist_back = clamp(hist_back, 1, len(history))

    img = get_next_image()
    return Response(content=img, media_type="image/png")


@app.get('/dir/{direc}')
def set_dir(direc: str):
    direc = urllib.parse.unquote(direc)
    load_dir(direc)
    return Response(content="ok", media_type="text")

@app.get('/save')
def save():
    global history
    fpath = history[-1]
    dirname, fname = os.path.split(fpath)
    shutil.copy(fpath, os.path.join('save', fname))
    return Response(content="ok", media_type="text")

