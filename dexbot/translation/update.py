import subprocess
import glob
import os
import ntpath
import shutil

def update(dir_path):
    for file in glob.glob(dir_path, recursive=True):
        file_name = ntpath.basename(file)
        ts_file = 'dexbot/translation/ru/' + os.path.splitext(file_name)[0] + '_ru.ts'
        command = ['C:/Qt/Tools/linguist_6.5.2/lupdate.exe', file, '-ts', ts_file]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()

def release():
    dir_path = "dexbot/translation/ru/*.ts"
    for file in glob.glob(dir_path, recursive=True):
        file_name = ntpath.basename(file)
        qm_file = 'dexbot/translation/ru/' + os.path.splitext(file_name)[0] + '.qm'
        command = ['C:/Qt/Tools/linguist_6.5.2/lrelease.exe', file, qm_file]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        shutil.move(qm_file, 'dexbot/resources/translates/ru/' + os.path.splitext(file_name)[0] + '.qm')
    
#update("dexbot/views/ui/*.ui")
update("dexbot/translator_strings.py")
release()