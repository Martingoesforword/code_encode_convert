# -*- coding: utf-8 -*-
import os, chardet, codecs, re

# 文件类型扩展名  文件列表
import struct

FileType, FileList = [], []
CFG_SET_BOM = True
CFG_SET_BOM_TYPE = "utf-8"
# 目标编码格式
TargetCoding = "utf-8"
# 包括文件类型扩展名
FileType = [".c", ".h", ".cpp", ".hpp", ".cc"]


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


def convert_2_target_coding():
    """ 转换成目标编码格式
    """
    for filepath in FileList:

        # 获取文件编码
        with open(filepath, 'rb') as f:
            data = f.read()
            codeType = chardet.detect_all(data)[0]['encoding']
            # 2312范围较窄，使用18030替换
            if codeType == "GB2312":
                codeType = "gb18030"

        # 排除已经是utf-8的代码文件
        if codeType != "UTF-8-SIG":

            # 统计功能
            print(codeType)
            if not allCode.get(codeType):
                allCode[codeType] = 1
            else:
                allCode[codeType] += 1

            # 实际的编码转换
            with codecs.open(filepath, 'r', codeType) as f:
                content = f.read()
            if CFG_SET_BOM:
                # 写入bom签名头
                if CFG_SET_BOM_TYPE == "utf-8":
                    # 写入utf-8 bom签名头
                    bom_bytes = [0xEF, 0xBB, 0xBF]
                    with codecs.open(filepath, 'wb')as f:
                        for x in bom_bytes:
                            byte = struct.pack('B', x)
                            f.write(byte)
                else:
                    print("不支持此bom类型")
                    break
            else:
                # 没有bom签名头需要写
                with codecs.open(filepath, 'w')as f:
                    f.write("")

            # code优化提示，记录已经被转码
            tips = "/* coding: utf-8 */\n"
            with codecs.open(filepath, 'a', TargetCoding) as f:
                f.write(tips)
            with codecs.open(filepath, 'a', TargetCoding) as f:
                f.write(content)
            print(filepath + '\n')


if __name__ == '__main__':
    # 获取目录
    clike_files_path = "D:\\workplace\\cpp\\RuiKeStd_Soui2.x-master"
    # 设置工作目录
    WorkDir = clike_files_path
    os.chdir(WorkDir)

    # 获取所有需要转化编码的文件列表
    get_file_list(WorkDir)

    # 对整个文件列表进行编码转化
    convert_2_target_coding()
    print(allCode)
