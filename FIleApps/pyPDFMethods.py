#! python3

from pypdf import PdfReader
from pypdf import PdfWriter
import os, sys
import fileIO

def pdfMerger(fileList):
    writer = PdfWriter()
    os.system('cls')
    print(str(len(fileList)) + ' Files merged: ' + ', '.join(f[f.rfind(f'\\')+1:] for f in fileList) + '\n')
    for i in fileList:
        reader = PdfReader(i)
        for pageNum in range(reader.get_num_pages()):
            page = reader.get_page(pageNum)
            writer.add_page(page)
        reader.close()
    return writer

def pdfCreator(file, mode, writer=None):
    outputFile = open(file, mode)
    if (writer != None):
        writer.write(file)
    outputFile.close()


'''
# force '\\' in file paths
filePathRegex = re.compile(r'''
    # (?<!\\\\)\\\\
#    (\\)+
''', re.VERBOSE)


def getCorrectedFilePath(index):
        res = input('\nProvide a corrected file path, press enter to continue, or type \'exit\' to quit: ').replace('"', '')
        if (res != ''):
            if (index <= len(sys.argv)):
                sys.argv.insert(index + 1, res)
            else:
                sys.argv.append(res)


def pyPDFPrinter(filePath, case='', index=None):
    match case:
        case '/':
            print(print(filePath[filePath.rfind(f'\\')+1:] + ' failed to be added'))
            if (index != None):
                getCorrectedFilePath(index)
            else:
                print('\nPDF file not found.\nEnsure the file path exists and that the file is a .pdf\n')

def addPDFext(fileString):
    if fileString[-4:] != '.pdf':
        fileString = fileString + '.pdf'
    return fileString

def userInput(string, action=None):
    res = ''
    case = ''
    if (string == 'exit'):
        os.system('cls')
        quit()
    elif (action == 'filePath'):
        res, case = fileIO.validateFile(string, 'pdf')
    elif (action == 'dirPath'):
        res, case = fileIO.validateDirPath(string)
    return res, case

def processUserInput(filePath, fileList, case='', index=None):
    res = ''
    match case:
        case '/':
            pyPDFPrinter(filePath, case, index)
        case 'valid':
            res = fileList.append(filePathRegex.sub(r'\\', filePath))
    return res
'''