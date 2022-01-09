import sys, codecs
import os
import glob
import subprocess
import shutil

class FileOperation():

    # ファイルを開く
    def fileOpen(self, file_full_path):
        # print('---fileOpen:{}---'.format(file_full_path))
        if file_full_path:
            subprocess.Popen(['start', file_full_path], shell=True)

    # フォルダを開く
    def folderOpen(self, folder_path):
        # print('---folderOpen:{}---'.format(folder_path))
        if folder_path:
            subprocess.Popen(['explorer', folder_path])

    # フルファイルパスからディレクトリパスのみ取得する
    def getFolderPath(self, file_full_path):

        if file_full_path:
            dir_path = os.path.dirname(file_full_path)
        else:
            dir_path = ""

        return dir_path;
