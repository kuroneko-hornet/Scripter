from flask import Flask, render_template, request
from flask import send_file as flask_send_file
import os
from glob import glob

from tasks import create_video, set_accountinfo
from postgresql import insert_scriptinfo
from gdapi import upload_Gdrive
import config

app_flask = Flask(__name__)


def save_scriptinfo(script_dict):
    for id in range(int(len(script_dict)//6)):
        insert_params = {
            "id": f"text{id}",
            "script": script_dict[f"input_text{id}"],
            "fontsize": int(script_dict[f"input_fontsize{id}"]),
            "starttime": float(script_dict[f"input_start{id}"]),
            "endtime": float(script_dict[f"input_end{id}"]),
            "color": script_dict[f"input_color{id}"],
            "xymode": script_dict[f"input_xy_mode{id}"]
        }
        insert_scriptinfo(insert_params)
    return


def save_videofile(video_file):
    set_accountinfo()
    file_path = os.environ["TMP_DIR"] + video_file.filename
    video_file.save(file_path)
    upload_Gdrive(video_file.filename, file_path)


@app_flask.route('/')
def index():
    return render_template('index.html')


@app_flask.route("/", methods=["POST"])
def index_post():
    print("\t[ POST ] ")
    print("\t[ request.files ]")
    print(request.files)
    print("\t[ request.form ]")
    print(request.form)

    save_scriptinfo(request.form)
    save_videofile(request.files["video_file"])

    # create_video
    print(" [ Start .MP4 Scripter ]")
    fontname = "ヒラギノ丸ゴ ProN W4.ttc"
    create_video.delay(request.files["video_file"].filename, fontname)

    return render_template("index.html")


@app_flask.route("/downloadlist")
def list_download():
    output = ""
    for download_path in glob(os.environ["DOWNLOAD_LIST_PATTERN"]):
        fname = os.path.split(download_path)[1]
        output += f"<li><a href='/yourproduct/{fname}'>{fname}</a></li>"
    return render_template("download.html", download_links_html=output)


@app_flask.route("/yourproduct/<fname>")
def download(fname):
    fname = os.environ["TMP_DIR"] + fname
    return flask_send_file(fname)


if __name__ == "__main__":
    app_flask.run(debug=True, host="0.0.0.0")
