from PIL import Image
import ffmpeg
import os

Image.MAX_IMAGE_PIXELS = None

def get_keyint(path: str) -> int:
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    keyint = eval(video_stream['avg_frame_rate']) * 10
    return int(keyint)

def get_video_resolution(path: str) -> tuple:
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    w = int(video_stream['width'])
    h = int(video_stream['height'])
    return w, h

def get_img_size(path: str) -> tuple:
    im = Image.open(path)
    w, h = im.size
    return w, h

def get_tiles(width, height) -> tuple:
    tpx = 2000000
    rowsl = 0
    colsl = 0

    ctpx = width * height
    ctar = width / height

    while ctpx >= tpx * 4 / 3:
        if ctar > 1:
            colsl += 1
            ctar /= 2
            ctpx /= 2
        else:
            rowsl += 1
            ctar *= 2
            ctpx /= 2
    return rowsl, colsl

def return_path(path: str, type: str) -> str:
    root, file = os.path.split(path)
    pre, _ = os.path.splitext(file)
    if type == 'image':
        return os.path.join(root, pre + '.avif')
    elif type == 'video':
        return os.path.join(root, pre + '-av1.mkv')