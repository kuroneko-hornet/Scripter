from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os
import config
from postgresql import select_accountinfo


gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.\
    from_json_keyfile_dict(select_accountinfo(), scope)
drive = GoogleDrive(gauth)


def upload_Gdrive(title, input_path):
    file = drive.CreateFile({
        "title": title,
        'mimeType': 'video/mp4',
        "parents":  [{'id': os.environ["ID"]}]})
    file.SetContentFile(input_path)
    file.Upload()


def download_video_Gdrive(title, save_path):
    for file in drive.ListFile({'q': f'title = "{title}"'}).GetList():
        print('title: %s, id: %s' % (file['title'], file['id']))
        file.GetContentFile(save_path)


def download_font_Gdrive(fontname, save_path):
    for file in drive.ListFile({'q': f'title = "{fontname}"'}).GetList():
        print('title: %s, id: %s' % (file['title'], file['id']))
        file.GetContentFile(save_path)
