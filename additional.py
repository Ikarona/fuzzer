import random
import pickle
import paramset
import os
import math
import mutation_struct

def ReadFile(file):
    fd = open(file,'rb')
    cont = fd.read()
    fd.close()
    return cont

def WriteFile(file, cont):
    fd = open(file, 'wb')
    if fd.write(cont):
        return 0
    else:
        return 1
    fd.close()

def ListDir(path):
    return os.listdir(path)

def IsEmptyDir(path):
    return ListDir(path) == []

def ClearDir(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))

def SeparateName(fullname):
    if '.' in fullname:
        name, ext = fullname.split('.')
    else:
        name = fullname
        ext = ''
    return name, ext

def CreateAdditionalFiles(num, path='./'):
    filesList = os.listdir(path)
    mutate = mutation_struct.Data(random.Random())
    flag = True
    while(num != 0):
        fileToManipulate = random.choice(filesList)
        filePath = os.path.join(paramset.INITDIR, fileToManipulate)
        fileInfo = ReadFile(filePath)
        newFileInfo = mutate.random_file(fileInfo)
        name, ext = SeparateName(fileToManipulate)
        name = num + '.' + ext
        fileName = os.path.join(paramset.INITDIR, name)
        if not WriteFile(fileName, newFileInfo):
            flag = False
        num -= 1
    if flag == False:
        return 1
    else:
        return 0

def