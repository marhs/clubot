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
# Log system
import logging

# Prepare loggging system
logging.basicConfig(format  ='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


# Reddit user agent
userAgent = 'Clubot, automated subreddit publisher. Author /u/helmetk'

def init():
    logging.debug('Iniciando imgur')
    im = pyimgur.Imgur(imgurClientId)
    logging.debug('IMgur iniciado, iniciando reddit')
    r = praw.Reddit(user_agent=userAgent)
    logging.debug('Reddit iniciado, logeando')
    r.login(user,password)
    return [r,im]

r, im = init()

def upload():
    img = listdir(imgDir)
    if len(img) == 0:
        logging.info('Folder empty')
        return False

    if img[0] == '.DS_Store':
        remove(imgDir + img[0])
        img = listdir(imgDir)

    logging.info("Uploading img: " + imgDir + img[0] + " [Title] " + img[0][:-4])
    try:
        res = im.upload_image(imgDir+ img[0], title=img[0][:-4])
    except:
        return False
    shutil.move(imgDir + img[0], completedDir)
    logging.info("Photo uploaded")

    return res

def post(subreddit):
    img = upload()
    if not img:
        logging.info("Error uploading to imgur")
        return False
    logging.info("Posteando")
    sub = r.submit(subreddit, img.title, url=img.link)
    return sub

def main():

    p = post(subreddit)

    if not p:
        logging.info('Error posting')
    else:
        logging.info("New submission at " + subreddit + " with id: " + p.id)
    logging.info('Waiting 1 day for next submission')
    sleep(86400)
main()
