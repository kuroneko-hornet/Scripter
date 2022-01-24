from celery import Celery
from create_video import create_telopped_video, create_sounded_video
import os
from datetime import datetime
from gdapi import download_video_Gdrive, download_font_Gdrive
from postgresql import delete_scriptinfo, select_accountinfo
import config
import json


app_celery = Celery("task", broker=os.environ["BROKER_URL"])
app_celery.conf.result_backend = os.environ["BROKER_URL"]


def set_accountinfo():
    info = select_accountinfo()
    with open(os.environ["TMP_DIR"] + os.environ["GACCOUNT"], 'w') as f:
        json.dump(info, f)


@app_celery.task
def create_video(filename, fontname):
    path_of_videofile = os.environ["TMP_DIR"] + filename
    path_of_nosound_video = os.environ["TMP_DIR"] + "nosound.mp4"
    # save videofile from google drive
    download_video_Gdrive(filename, path_of_videofile)
    os.environ["FONTPATH"] = os.environ["FONTPATHDIR"] + fontname
    if not os.environ["IS_LOCAL"]:
        download_font_Gdrive(fontname, os.environ["FONTPATH"])
        set_accountinfo()

    path_of_product =\
        f"{os.environ['TMP_DIR']}telop_{datetime.now().strftime('%Y%m%d%H%M')}_{filename}"
    print(" run create_telopped_video()...")
    create_telopped_video(path_of_videofile, path_of_nosound_video)
    print(" run create_sounded_video()...")
    create_sounded_video(path_of_videofile, path_of_nosound_video, path_of_product)
    print(" remove files...")

    # delete old data
    delete_scriptinfo()
    os.remove(path_of_videofile)
    os.remove(path_of_nosound_video)
    return