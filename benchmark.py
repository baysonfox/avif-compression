import subprocess
import os
import pandas as pd

# Getting the result using ssimulacra2_rs
# ssimulacra2_rs image <source> <distorted>

def get_result(source: str, distorted) -> str:
    result = subprocess.check_output(['ssimulacra2_rs', 'image', source, distorted]).decode('utf-8')
    score = result.split(': ')[1]
    return score

columns = ['source', 'distorted', 'ssimulacra2']
data = []

path = os.path.join(os.getcwd(), 'benchmarking/images')
print(path)
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.jpg'):
            file, ext = os.path.splitext(file)
            source = os.path.join(root, file + ext)
            distorted = os.path.join(root, 'avif/', file + '.avif.png')
            result = get_result(source, distorted)
            data.append([source, distorted, result])

df = pd.DataFrame(data, columns=columns)
df.to_csv('metrics.csv', index=False)
            