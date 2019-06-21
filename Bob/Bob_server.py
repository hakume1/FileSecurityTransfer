# -*-encoding:utf-8-*-

import socket
import threading
import os
import sys
import math
import functions
import time
from functions import file_encrypt, file_decrypt, printCN

bindIp = "0.0.0.0"
bindPort = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bindIp, bindPort))
server.listen(1)
print "Listening on %s:%d" % (bindIp, bindPort)

def progressbar(cur, total):
    percent = '{:.2%}'.format(float(cur) / float(total))
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
        '=' * int(math.floor(cur * 50 / total)),
        percent))
    sys.stdout.flush()


def checkFileName(originalFileName):
    name = originalFileName
    index = 1
    newNameSuffix = "(" + str(index) + ")"
    finalFileName = originalFileName
    if os.path.exists(finalFileName):
        finalFileName = name + " " + newNameSuffix
    while os.path.exists(finalFileName):
        index += 1
        oldSuffix = newNameSuffix
        newNameSuffix = "(" + str(index) + ")"
        finalFileName = finalFileName.replace(oldSuffix, newNameSuffix)
    return finalFileName


def handleClient(clientSocket):
    # receive file size
    fileSize = int(clientSocket.recv(1024))
    # print "[<==] File size received from client: %d" % fileSize
    clientSocket.send("Received")
    # receive file name
    fileName = clientSocket.recv(1024)
    # print "[<==] File name received from client: %s" % fileName
    clientSocket.send("Received")
    fileName = checkFileName(fileName)
    file = open(fileName, 'wb')
    # receive file content
    print "[==>] Saving file to %s" % fileName
    receivedLength = 0
    while receivedLength < fileSize:
        bufLen = 1024
        if fileSize - receivedLength < bufLen:
            bufLen = fileSize - receivedLength
        buf = clientSocket.recv(bufLen)
        file.write(buf)
        receivedLength += len(buf)
        process = int(float(receivedLength) / float(fileSize) * 100)
        progressbar(process, 100)

    file.close()
    print "\r\n[==>] File %s saved." % fileName
    clientSocket.send("Received")


if __name__ == '__main__':
    count=0;
    printCN("你是Bob,欢迎来到文件安全传输系统，请按照提示输入！\n")
    while count < 5:
        client, addr = server.accept()
        print "\n[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
        clientHandler = threading.Thread(target=handleClient, args=(client,))
        clientHandler.start()
        count=count+1
    else:
        time.sleep(1)
        file_decrypt()