import os

def setFileExt(filePath, ext):
    if (filePath[filePath.rfind('.')+1:] != ext):
        filePath = filePath + '.' + ext
    return filePath

def validateFile(filePath, ext=''):
    case = ''
    if (filePath != ''):
        filePath = setFileExt(filePath, ext)
        if (not os.path.exists(filePath)):
            case = '/'
        else:
            case = 'valid'
    return filePath, case

def validateDirPath(dirPath):
    if (not os.path.exists(dirPath)):
        os.mkdir(dirPath)
    return dirPath

def getFilesFromDirectory(parent,  fileList, fileType, recursive=False):
    if (recursive):
        recursivePreorderTraversal(parent, fileList, fileType)
    else:
        for file in os.listdir(parent):
            appendFileList(parent, fileList, fileType, file)  

# TODO: implement height balanced tree w/ recursive and iterative traversals

def recursivePreorderTraversal(parent, list, fileType=None):
    if (fileType != None):
        for root, dirs, files in os.walk(parent):
            for f in files:
                appendFileList(root, list, fileType, f)
    else:
        for root, dirs, files in os.walk(parent):
            for d in dirs:
                appendDirectoryList(root, list, d)

def appendFileList(parent, fileList, fileType, file): 
    if os.path.isfile(os.path.join(parent, file)) and file.endswith(fileType):
        fileList.append(os.path.join(parent,file))

def appendDirectoryList(parent, dirList, dir):
    if os.path.isdir(dir):
        dirList.append(os.path.join(parent, dir))

def setFilePath(fileType):
    inputString = input('Provide a path for output: ').replace('"', '')
    outputPath = validateDirPath(inputString)
    fileName = outputPath + '\\' + input('Provide a file name: ')
    if (not fileName.endswith(fileType)):
        fileName = fileName + fileType
    return fileName

def setFilePath(fileType, dir, file):
    dir = validateDirPath(dir)
    file = dir + '\\' + file
    if (not file.endswith(fileType)):
        file = file + fileType
    return file