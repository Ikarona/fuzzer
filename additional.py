import random
import pickle
import paramset
import os
import math


def readFile(file):
    fd = open(file,'rb')
    cont = fd.read()
    fd.close()
    return cont

def writeFile(file, cont):
    fd = open(file, 'wb')
    if fd.write(cont):
        return 0
    else:
        return 1
    fd.close()

def listDir(path):
    return os.listdir(path)

def isEmptyDir(path):
    return listDir(path) == []

def clearDir(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))

