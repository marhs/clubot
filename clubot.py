## Clubot ##

# Marco Herrero <me@marhs.de>

# Reddit API for python
import praw
# Python Imgur API
import pyimgur
# File management. Move, delete, copy, list. 
import shutil
from os import listdir, remove
# time.sleep
from time import sleep
# Configuration files. 
from config import *

# Reddit user agent
userAgent = 'Clubot, automated subreddit publisher. Author /u/helmetk'

def init():
    im = pyimgur.Imgur(imgurClientId)
    r = praw.Reddit(user_agent=userAgent)
    r.login(user,password)
    return [r,im]

r, m = init()

def upload():
    img = listdir(imgDir)
    if len(img) == 0:
        print('[Error] Folder empty')
        return False

    if img[0] == '.DS_Store':
        remove(imgDir + img[0])
        img = listdir(imgDir)

    print("[Uploading] img: " + imgDir + img[0] + " [Title] " + img[0][:-4])
    try:
        res = im.upload_image(imgDir+ img[0], title=img[0][:-4])
    except:
        return False
    shutil.move(imgDir + img[0], completedDir)
    print("[Photo uploaded]")

    return res

def post(subreddit):
    img = upload()
    if not img:
        print("[Error] Error uploading to imgur")
        return False
    print("[Posteando]")
    sub = r.submit(subreddit, img.title, url=img.link)
    return sub

def main():

    p = post('TemplePorn')
    if not p:
        print('[Error] Error posting')
    else:
        print("[CLUBOT] // New submission at TemplePorn with id: " + p.id)
    sleep(86400)
main()
