import os
path = os.path.join(os.getcwd(), 'todo')
image_extension = ('.jpg', '.JPG', '.png', '.PNG', '.jpeg')
video_extension = ('.mp4', '.MP4', '.MOV', '.mov')

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(image_extension):
            path = os.path.join(root, file)
            pre, ext = os.path.splitext(path)
            if  os.path.exists(os.path.join(pre + '.avif')):
                os.remove(path)
                print("Removed", path)
            else:
                print("Missing:", path)
        elif file.endswith(video_extension):
            path = os.path.join(root, file)
            pre, ext = os.path.splitext(path)
            if  os.path.exists(os.path.join(pre + '-av1.mkv')):
                os.remove(path)
                print("Removed", path)
            else:
                print("Missing:", path)
print("All images and videos converted & removed")
