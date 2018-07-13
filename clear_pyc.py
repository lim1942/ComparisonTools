#coding=utf-8

# author:lim
# date:2018.7.13
# email:940711277

import os
import sys

suffixes = ['pyc', 'pyo']
dirName = ['__pycache__']


def clean(root_dir, suffixes=suffixes):

    if not os.path.isdir(root_dir):
        print ('Directory {} not exists, skipped.'.format(root_dir))

    suffixes = map(lambda x: '.' + x, suffixes)
    for root, dirs, files in os.walk(root_dir):

        # clear __pycache__ dir
        for _dir in dirs: 
            if any(map(lambda x: _dir==x, dirName)):
                try:
                    fullDirName = os.path.join(root,_dir)
                    os.system('rd /s /q {}'.format(fullDirName))
                    print(fullDirName+'  done')
                except Exception as e:
                    print ('Failed to delete {}: {}'.format(fullDirName, str(e)))
                    
        # clear pyc、pyo file
        for file in files:
            if any(map(lambda x: file.endswith(x), suffixes)):
                try:
                    fileName = os.path.join(root, file)
                    os.remove(fileName)
                    print(fileName+'  done')
                except Exception as e:
                    print ('Failed to delete {}: {}'.format(file, str(e)))


def clean_all(root_dirs, suffixes=suffixes):
    for root_dir in root_dirs:
        clean(root_dir, suffixes)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        root_dirs = [os.path.dirname(os.path.abspath(__file__))]
    else:
        root_dirs = sys.argv[1:]
    clean_all(root_dirs)