import shutil
import os

path = '{}{}.zip'.format('output_CSVs/', '15.04.2021_18.00.20')
if os.path.isfile(path):
    os.remove(path)
print(path)
print('done')
