import os
import subprocess
import ffmpeg
import shlex
from utils import get_keyint, get_video_resolution, get_tiles, return_path, get_img_size

path = os.getcwd()
path = os.path.join(path, 'todo/')
video_extension = ('.mp4', '.MP4', '.MOV', '.mov')
image_extension = ('.jpg', '.JPG', '.png', '.PNG', '.jpeg')

video_files = []
image_files = []
log_lines = []

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(video_extension):
            video_files.append(os.path.join(root, file))
        if file.endswith(image_extension):
            image_files.append(os.path.join(root, file))
            
for file in video_files:
    new_path = return_path(file, 'video')
    keyint = get_keyint(file)
    w, h = get_video_resolution(file)
    rows, columns = get_tiles(w, h)
    ffmpeg_cmd = (
        ffmpeg
        .input(file)
        .output(
            new_path,
            vcodec="libsvtav1",
            acodec="copy",
            preset=10,
            crf=40,
            threads=10,
            **{"svtav1-params":"input-depth=10:tune=3:enable-qm=1:qm-min=0:enable-dlf=2:keyint={}:tile-rows={}:tile-columns={}".format(keyint, rows, columns)}
        )
        .run(overwrite_output=True)
    )

for file in image_files:
    new_path = return_path(file, 'image')
    w, h = get_img_size(file)
    rows, columns = get_tiles(w, h)
    avifenc_cmd = """
        avifenc \
        --min 0 --max 63 \
        -a enable-chroma-deltaq=1 \
        -a enable-qm=0 \
        --autotiling \
        -a quant-b-adapt=1 \
        -a sb-size=64 \
        -a tune=ssim \
        -a deltaq-mode=2 \
        -a cpu-used=4 \
        -a tune-content=psy \
        --jobs 8 -s 3 \
        -d 10 \
        {} {}
    """.format(shlex.quote(file), shlex.quote(new_path))

    subprocess.run(avifenc_cmd, shell=True)
