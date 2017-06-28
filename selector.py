from os import listdir
from os.path import join, isfile
from shutil import copyfile

import settings


level = '01'
for file_name in (f for f in listdir(settings.LOCAL_DIRECTORY) if isfile(join(settings.LOCAL_DIRECTORY, f))):
    local_file = join(settings.LOCAL_DIRECTORY, file_name)
    with open(local_file, 'rb') as f:
        f.readline()
        f.readline()
        f.readline()
        line = str(f.readline())

        try:
            if line.split(',')[2] in level:
                copyfile(local_file, 'data/level1/' + file_name)
        except:
            print('error: ' + file_name)
