# -*- coding: utf-8 -*-
import os, chardet, codecs, re

# 文件类型扩展名  文件列表
import struct

FileType, FileList = [], []
CFG_SET_BOM = True
CFG_SET_BOM_TYPE = "utf-8"

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

allCode = {}
def convert_2_target_coding(coding='utf-8', one = None):
    """ 转换成目标编码格式
    """
    if one:
        with open(one, 'rb') as f:
            data = f.read()
            codeType = chardet.detect(data)['encoding']
        # if codeType not in (coding, 'ascii', 'UTF-8-SIG', 'Windows-1252', 'ISO-8859-1'):
        if True:
            print(codeType)
            if not allCode.get(codeType):
                allCode[codeType] = 1
            else:
                allCode[codeType] += 1
            try:
                with codecs.open(one, 'r', codeType) as f:
                    content = f.read()
                #写入bom
                if CFG_SET_BOM:
                    if CFG_SET_BOM_TYPE == "utf-8":
                        bom_bytes = [0xEF, 0xBB, 0xBF]
                        with codecs.open(one, 'wb')as f:
                            for x in bom_bytes:
                                a = struct.pack('B', x)
                                f.write(a)
                    else:
                        print("不支持此bom类型")
                else:
                    with codecs.open(one, 'w')as f:
                        f.write("")
                # code优化提示
                tips = "/* coding: utf-8 */\n"
                with codecs.open(one, 'a', coding) as f:
                    f.write(tips)
                with codecs.open(one, 'a', coding) as f:
                    f.write(content)
                print(one + '\n')
            except:
                pass
    for filepath in FileList:
        with open(filepath, 'rb') as f:
            data = f.read()
            codeType = chardet.detect_all(data)['encoding']
        # if codeType not in (coding, 'ascii', 'UTF-8-SIG', 'Windows-1252', 'ISO-8859-1'):
        if True:
            print(codeType)
            if not allCode.get(codeType):
                allCode[codeType] = 1
            else:
                allCode[codeType] += 1
            try:
                with codecs.open(filepath, 'r', codeType) as f:
                    content = f.read()
                #写入bom
                if CFG_SET_BOM:
                    if CFG_SET_BOM_TYPE == "utf-8":
                        bom_bytes = [0xEF, 0xBB, 0xBF]
                        with codecs.open(filepath, 'wb')as f:
                            for x in bom_bytes:
                                a = struct.pack('B', x)
                                f.write(a)
                    else:
                        print("不支持此bom类型")
                        break
                else:
                    with codecs.open(filepath, 'w')as f:
                        f.write("")
                # code优化提示
                tips = "/* coding: utf-8 */\n"
                with codecs.open(filepath, 'a', coding) as f:
                    f.write(tips)
                with codecs.open(filepath, 'a', coding) as f:
                    f.write(content)
                print(filepath + '\n')
            except:
                continue

if __name__ == '__main__':
    # 获取目录
    ruike_project_path = "D:\workplace\lib\soui\SOUI\include"
    ruike_project_file = "D:\workplace\lib\soui\SOUI\include\soui-version.h"
    # WorkDir = str(input('input target folder\n\t:'))
    WorkDir = ruike_project_path
    # 目标编码格式
    TargetCoding = "utf-8"
    # 文件类型扩展名
    if ruike_project_file:
        convert_2_target_coding(TargetCoding, ruike_project_file)
    else:
        FileType = [".c", ".h", ".cpp", ".hpp", ".cc"]
        os.chdir(WorkDir)
        get_file_list(WorkDir)

        convert_2_target_coding(TargetCoding, ruike_project_path)
        print(allCode)


