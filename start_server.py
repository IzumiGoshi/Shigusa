import os


fpath = os.path.split(__file__)[0]
os.chdir(fpath)
os.system('uvicorn server:app --port 8123')
input('...')
