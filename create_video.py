from PIL import Image, ImageFont, ImageDraw
from moviepy.editor import VideoFileClip
from tqdm import trange
import numpy as np
import cv2
import json
import os
from postgresql import select_scriptinfo
import config


def set_text_xy(text, wh, text_wh):
    valid_text_area = [int(wh[0] - text_wh[0]), int(wh[1] - text_wh[1])]
    if text["xymode"] == "center":
        xy = (int(valid_text_area[0] / 2), int(valid_text_area[1] / 2))
    elif not text["xymode"]:  # default
        xy = (valid_text_area[0] / 2), int((wh[1] * 0.9 - text_wh[1]))
    else:
        exit(print(f"The parameter '{text['xymode']}' is not valid for 'xymode'"))
    return xy


def set_text_color(text):
    color_transer = {
        "red": "blue",
        "blue": "red",
        "green": "green",
        "black": "black",
        "white": "white"
    }
    if text["color"] in color_transer:
        return color_transer[text["color"]]
    elif not text["color"]:
        return "black"
    else:
        exit(print(f"The parameter '{text['color']}' is not valid for 'color'"))
    # default: black


def insert_telop(img, text_params, w, h):
    text_str = text_params["script"]
    font_size = text_params["fontsize"]
    # fontpath は後で text_params の要素として追加したい
    font_path = os.environ["FONTPATH"]
    font = ImageFont.truetype(font_path, font_size)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    text_w, text_h = draw.textsize(text_str, font)

    xy = set_text_xy(text_params, [w, h], [text_w, text_h])
    color = set_text_color(text_params)

    draw.text(xy=xy, text=text_str, font=font, fill="white",
              stroke_width=int(font_size / 25),
              stroke_fill=color,
              )

    img = np.array(img)
    return img


def load_telop_data(telop_params_path):
    with open(telop_params_path, 'r') as f:
        text_dict = json.load(f)
    return text_dict


def lastone(iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, False
        last = val
    yield last, True


def create_telopped_video(input_path, output_path):
    mov_object = cv2.VideoCapture(input_path)
    print(type(mov_object))
    flame_count = int(mov_object.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = mov_object.get(cv2.CAP_PROP_FPS)
    w = int(mov_object.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(mov_object.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # for mp4
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    scriptinfo_list = select_scriptinfo()
    # scriptinfo_list = load_telop_data(telop_path)

    print(f"[Frame count = {flame_count}, frame per second = {fps}]")
    print(f"[input path = {input_path}, output path = {output_path}]")

    finish_telopped = False

    for i in trange(flame_count):
        read_succeeded, frame = mov_object.read()
        if read_succeeded:
            if finish_telopped:
                video_writer.write(frame)
                continue
            time = i / fps
            for text_params, is_last in lastone(scriptinfo_list):
                if time < text_params["starttime"]:  # next frame
                    break
                elif text_params["endtime"] < time:  # next text
                    if is_last:  # the last telop is finished
                        finish_telopped = True
                    continue
                else:  # insert telop
                    frame = insert_telop(frame, text_params, w, h)
            video_writer.write(frame)
        else:
            pass
    return


def create_sounded_video(src_path, telopped_path, output_path):
    src_video = VideoFileClip(telopped_path)
    src_audio = VideoFileClip(src_path).audio
    target_video = src_video.set_audio(src_audio)
    target_video.write_videofile(output_path, audio_codec='aac')


if __name__ == "__main__":
    datadir = '../movie-data/'
    src_video_path = 'test2.mp4'

    input_path = f'{datadir}test2.mp4'
    telopped_path = f'{datadir}telopped_{src_video_path}'
    output_path = f'{datadir}output_{src_video_path}'

    create_telopped_video(input_path, telopped_path)
    create_sounded_video(input_path, telopped_path, output_path)
