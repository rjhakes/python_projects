import os, sys
import FreeSimpleGUI as sg
import fileIO

'''
FIXME: events -FOLDER_PATH- and -TUNNEL- can misfire
FIXME: require file_type
FIXME: input sanitation and validation
FIXME: after merge, keep program open, reset values, present successful merge message 
FIXME: implement error handling
FIXME: improved variable naming
TODO: styling
TODO: implement additional file types
TODO: implement merge types and conditions
'''

def main():

        label1 = sg.Text("Select Files:")
        input1 = sg.Input(key='-FILE_PATH-', change_submits=True)
        choose_button1 = sg.FilesBrowse('Upload')

        selectFolderLabel = sg.Text('Select Folder:')
        input3 = sg.Input(key='-FOLDER_PATH-', change_submits=True)
        choose_button3 = sg.FolderBrowse('Select')

        label2 = sg.Text("Folder:")
        input2 = sg.Input(key='-OUTPUT_PATH-', change_submits=True)
        choose_button2 = sg.FolderBrowse('Select')

        label4 = sg.Text("File Name:")
        input4 = sg.Input(key='-OUTPUT_FILE-', change_submits=True)

        merge_button = sg.Button('Merge', key="-MERGE-")
        check_box1 = sg.Checkbox('Tunnel', key='-TUNNEL-', change_submits=True)
        check_box2 = sg.Checkbox('Add', key='-ADD-', change_submits=True)
        label3 = sg.Text('Choose file type:')
        file_types = ['', '.pdf', '.docx']
        file_type_menu = sg.Combo(file_types, key='-FILE_TYPE-')
        file_getter = [
                [input1, choose_button1],
        ]
        folder_getter = [
                [input3, choose_button3, check_box1]
        ]
        tab1 = sg.Tab('File', file_getter, element_justification='right')
        tab2 = sg.Tab('Folder', folder_getter, element_justification='right')
        tab_group_layout = [[tab1, tab2]]
        tab_group = sg.TabGroup(tab_group_layout, key='TABGROUP-', 
                                selected_background_color='white',
                                selected_title_color='black',
                                tab_background_color='gray')
        fileList = []
        column1_layout = [
                
                # [sg.Frame('Upload Files', [
                #         [sg.Column([[check_box2],[tab_group]], element_justification='right')]
                #         ])],
                [
                sg.Column([
                        [label3, file_type_menu],
                        [sg.Frame('Upload Files', [
                                [sg.Column([[check_box2],[tab_group]], element_justification='right')]
                                ])
                        ],
                        [sg.Frame('Output Info',[
                                [sg.Column([
                                        [label2, input2, choose_button2],
                                        ], element_justification='right')],
                                [sg.Column([
                                        [label4, input4]], element_justification='right')]
                                ])
                        ],
                        
                ], element_justification='right', expand_x=True
                ), 
                sg.Column([
                        [sg.Table(values=fileList, headings=['Files'], auto_size_columns=False, 
                          def_col_width=20, key='-TABLE-')
                        ],
                        [sg.Column([[],[merge_button]], element_justification='center', expand_x=True)]
                ], expand_y=True)                
                ]                
        ]
        
        
        layout = [
                [sg.Column(column1_layout, element_justification='left', expand_x=True)],
                # [sg.Column([[merge_button]], element_justification='right', expand_x=True)]
                

        ]

        window = sg.Window("File Merger", 
                        layout)
        
        fileName = ''
        while True:
                event, values = window.read()
                if (event == sg.WIN_CLOSED):
                        break
                if ((event == '-FILE_PATH-' and not values['-ADD-']) or
                    (event == '-FOLDER_PATH-' and not values['-ADD-'])):
                        fileList = []
                        window['-TABLE-'].update(values=[])
                if (event == "-FILE_PATH-"):
                        os.system('cls')
                        values['-FOLDER_PATH-'] = ''
                        window['-FOLDER_PATH-'].update('')
                        for f in values['-FILE_PATH-'].split(';'):
                                fileIO.appendFileList(os.path.dirname(f), fileList, 
                                                        values['-FILE_TYPE-'], os.path.basename(f))
                        window['-TABLE-'].update(values=([os.path.basename(f)] for f in fileList))
                elif (event == "-FOLDER_PATH-"):
                        values['-FILE_PATH-'] = ''
                        window['-FILE_PATH-'].update('')
                if ((event == "-FOLDER_PATH-" and values['-TUNNEL-']) or
                (event == "-TUNNEL-" and values['-FOLDER_PATH-'])):
                        fileIO.getFilesFromDirectory(values['-FOLDER_PATH-'], 
                                                        fileList, values['-FILE_TYPE-'], values['-TUNNEL-'])
                        window['-TABLE-'].update(values=([os.path.basename(f)] for f in fileList))
                elif (event == "-FOLDER_PATH-" and not values['-TUNNEL-']):
                        fileIO.getFilesFromDirectory(values['-FOLDER_PATH-'], 
                                                        fileList, values['-FILE_TYPE-'])
                        window['-TABLE-'].update(values=([os.path.basename(f)] for f in fileList))
                elif ((event == '-OUTPUT_PATH-' and not values['-OUTPUT_FILE-'] == '') or
                        (event == '-OUTPUT_FILE-' and not values['-OUTPUT_PATH-'] == '')):
                                fileName = fileIO.setFilePath(values['-FILE_TYPE-'], 
                                                        values['-OUTPUT_PATH-'], 
                                                        values['-OUTPUT_FILE-'])
                elif (event == '-MERGE-'):
                        if (values['-FILE_TYPE-'] == ''):
                                sg.popup_quick_message('File Type Required', background_color='red')
                        # MERGE TARGET FILES
                        # CREATE AND WRITE OUTPUT FILE
                        # Case 1: file_type == pdf
                        if (values['-FILE_TYPE-'] == '.pdf'):
                                import pyPDFMethods
                                writer = pyPDFMethods.pdfMerger(fileList)
                                pyPDFMethods.pdfCreator(fileName, 'wb', writer)
                        # Case 2: file_type == docx
                        elif (values['-FILE_TYPE-'] == '.docx'):
                                import pyDocxMethods
                                writer = pyDocxMethods.docxMerger(fileList)
                                pyDocxMethods.docxCreator(fileName, writer)
                        #-------------------------------------------
                        # break
                elif (event == sg.WIN_CLOSED):
                        break
        window.close()

if __name__ == '__main__':
        main()