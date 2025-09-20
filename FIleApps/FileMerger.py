#! python3
'''
fileMerger [mode] [file_type] [instruction] [directory | file...]

mode = dir | file | dirFile
file_type = pdf | docx | xlsx | csv | txt | json | png
instruction = tunnel
directory | file = directory or file path(s)
'''
import os, sys
import fileIO

def main():
    os.system('cls')
    # sanitize file_type
    if (not sys.argv[2].startswith('.')):
        sys.argv[2] = '.' + sys.argv[2]
#-------------------------------------------
# COMPILE FILE LIST
    fileList = []
    # Case 1: mode == dir
    if (sys.argv[1] == 'dir'):       
        # Case 1a: instruction == tunnel
        if (sys.argv[3] == 'tunnel'):
            fileIO.getFilesFromDirectory(sys.argv[4], fileList, sys.argv[2],  True)
        # Case 1b: instruction == None
        else:
            fileIO.getFilesFromDirectory(sys.argv[3], fileList, sys.argv[2])
    # Case 2: mode == file
    elif (sys.argv[1] == 'file'):
        # Case 2a: files given as sys.argv
        if len(sys.argv) > 3 and (os.path.exists(sys.argv[3])):
            index = 3
            while (index < len(sys.argv)):
                fileIO.appendFileList(os.curdir, fileList, sys.argv[2], sys.argv[index])
                index += 1
        # Case 2b: files not given as sys.argv
        else:
            while True:
                os.system('cls')
                print(str(len(fileList)) + ' Files to be merged: ' + ', '.join(f[f.rfind(f'\\')+1:] for f in fileList) + '\n')
                inputString = input('\nProvde a file\'s path, press enter to continue, or type \'exit\' to quit: ').replace('"', '')
                if (inputString == ''):
                    break
                else:
                    fileIO.appendFileList(os.path.dirname(inputString), fileList, sys.argv[2], os.path.basename(inputString))

    # Case 3: mode == dirFile
    
#-------------------------------------------    
# GET OUTPUT FILE PATH AND NAME
    # FIXME: be able to exit on fileName input
    fileName = fileIO.setFilePath(sys.argv[2])
#-------------------------------------------
# MERGE TARGET FILES
# CREATE AND WRITE OUTPUT FILE
    # Case 1: file_type == pdf
    if (sys.argv[2] == '.pdf'):
        import pyPDFMethods
        writer = pyPDFMethods.pdfMerger(fileList)
        pyPDFMethods.pdfCreator(fileName, 'wb', writer)
    # Case 2: file_type == docx
    elif (sys.argv[2] == '.docx'):
        import pyDocxMethods
        writer = pyDocxMethods.docxMerger(fileList)
        pyDocxMethods.docxCreator(fileName, writer)
#-------------------------------------------
    os.system('cls')
    print(fileName + ' created.')
    input('Press enter to exit...')


if __name__ == "__main__":
    main()