# -*- coding: utf-8 -*-
import os, chardet, codecs, re

# 文件类型扩展名  文件列表
FileType, FileList = [], []


def get_file_list(Dir):
    """ 获取指定目录下所有指定类型文件
    """
    if len(Dir.strip(' ')) == 0:
        return
    dirList = [os.path.join(Dir, f) for f in os.listdir(Dir)]
    fileList = [f for f in dirList if os.path.isfile(f) and os.path.splitext(f)[1] in FileType]
    folderList = [f for f in dirList if os.path.isdir(f)]
    FileList.extend(fileList)
    # 递归字文件夹
    for subfolder in folderList:
        get_file_list(subfolder)


def convert_2_target_coding(coding='utf-8'):
    """ 转换成目标编码格式
    """
    for filepath in FileList:
        with open(filepath, 'rb') as f:
            data = f.read()
            codeType = chardet.detect(data)['encoding']
        coding = 'utf-8'
        if codeType not in (coding, 'ascii'):
            try:
                with codecs.open(filepath, 'r', 'gbk') as f:
                    content = f.read()
                with codecs.open(filepath, 'w', coding) as f:
                    f.write(content)
                print(filepath + '\n')
            except:
                continue

if __name__ == '__main__':
    # 获取目录
    ruike_project_path = "D:\workplace\cpp\RuiKeStd_Soui2.x-master"
    # WorkDir = str(input('input target folder\n\t:'))
    WorkDir = ruike_project_path
    # 目标编码格式
    TargetCoding = str(input('target coding(default to utf-8)\n\t:')).lower()
    # 文件类型扩展名
    FileType = re.split(r'\s+', str(input('file type(filename extension, such as .c .h)\n\t:')))
    os.chdir(WorkDir)
    get_file_list(WorkDir)
    convert_2_target_coding(TargetCoding)


