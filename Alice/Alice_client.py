#-*-encoding:utf-8-*-

import socket
import os
import sys
import math
import time
import functions
from functions import file_encrypt, file_decrypt, printCN, raw_inputCN

def progressbar(cur, total):
    percent = '{:.2%}'.format(float(cur) / float(total))
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
        '=' * int(math.floor(cur * 50 / total)),
        percent))
    sys.stdout.flush()


def getFileSize(file):
    file.seek(0, os.SEEK_END)
    fileLength = file.tell()
    file.seek(0, 0)
    return fileLength


def getFileName(fileFullPath):
    index = fileFullPath.rindex('\\')
    if index == -1:
        return fileFullPath
    else:
        return fileFullPath[index + 1:]


def transferFile(fileFullPath):
    if os.path.exists(fileFullPath):
        timeStart = time.clock()
        file = open(fileFullPath, 'rb')
        fileSize = getFileSize(file)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((targetHost, targetPort))
        #获取文件大小
        client.send(str(fileSize))
        response = client.recv(1024)
        #获取文件名
        client.send(getFileName(fileFullPath))
        response = client.recv(1024)
        #发送文件内容
        sentLength = 0
        while sentLength < fileSize:
            bufLen = 1024
            buf = file.read(bufLen)
            client.send(buf)
            sentLength += len(buf)
            process = int(float(sentLength) / float(fileSize) * 100)
            progressbar(process, 100)
        client.recv(1024)
        file.close()
        timeEnd = time.clock()
        print "\r\nFinished, spent %d seconds" % (timeEnd - timeStart)
    else:
        print "File doesn't exist"

if __name__ == '__main__':
    targetHost = raw_input("Server IP Address: ")
    targetPort = int(raw_input("Server port: "))

    printCN("你是Alice,欢迎来到文件安全传输系统，请按照提示输入！\n")
    file_encrypt()
    path=os.path.dirname(__file__)
    transferFile(path+r"\file_encrypted")
    transferFile(path + r"\AES_key_encrypted")
    transferFile(path + r"\file_iv_encrypted")
    transferFile(path + r"\file_signature_encrypted")
    transferFile(path + r"\fill_number")
    raw_inputCN("回车结束程序\n")