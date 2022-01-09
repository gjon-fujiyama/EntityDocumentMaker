# coding: utf-8
import PySimpleGUI as sg
import re
import numpy as np
from ColumnMasterAccess import ColumnMasterAccess

# +-----------------------------------------------------------------------------------+
# + サブウィンドウ　カラムマスター一覧編集
# +-----------------------------------------------------------------------------------+
class SubWindows():

    # +-----------------------------------------------------------------------------------+
    # + レイアウト初期設定
    # +-----------------------------------------------------------------------------------+
    def __init__(self, id, entity_cd, entity_name, entity_no):
        # ------ Menu Definition ------ #
        self.menu_def = [['File', ['Save', '----', 'Exit'], ]]
        self.icon_path = ".\FjiYama.ico"

        # data header
        data_header =  ['Mark',
                        'No',
                        'Column Cd',
                        'Column Name',
                        'Model',
                        'Digit',
                        'Acc',
                        'Not Null',
                        'PK',
                        'Explanation',
                        'DB DbCons',
                        'Remark',
                        'Status',
                        'Ref']

        radio_dic = {
                        '-radio Add-': ['Add Data', True, (None,None)],
                        '-radio Up-': ['Up Date', False, ('#d3d3d3','#d3d3d3')],
                        '-radio Del-': ['Del Data', False, ('#d3d3d3','#d3d3d3')],
                    }

        self.current_select_row = 0

        self.id = id
        self.entity_cd = entity_cd
        self.entity_name = entity_name
        self.entity_no = entity_no

        self.data_list = self.getColumnsTable()

        radio_layout = [sg.Radio(item[1][0],
                        key=item[0],
                        group_id='-Radio change-',
                        default=item[1][1],
                        enable_events=True) for item in radio_dic.items()],

        checkbox_lyout = [sg.Checkbox('All Mark Select',
                            key='-Sub All Mark Select-',
                            enable_events=True,
                            default=False,
                            disabled=True,
                            visible=False)]

        table_layout = [sg.Table(values=self.data_list,
                                headings=data_header,
                                auto_size_columns=False,
                                col_widths=[4, 3, 12, 15, 10, 5, 5, 8, 5, 15, 8, 15, 5, 5],
                                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                justification='left',
                                text_color='#000000',
                                background_color='#cccccc',
                                alternating_row_color='#ffffff',
                                header_text_color='#0000ff',
                                header_background_color='#cccccc',
                                key='-Columns Table-',
                                enable_events=True,
                                # enable_click_events=True,
                                size=(1050, 20),)]

        add_column = [sg.Column([self.getAddColumns()],
                                 key='-Column_Add-',
                                 scrollable = False,
                                 vertical_scroll_only = True,
                                 element_justification='left')]

        Layout = [[sg.Menu(self.menu_def, key='menu2')]
                , [sg.Button('Exit',key='Exit'),sg.Button('Save',key='Save', pad=((500, 0),(0,0)))]
                , [sg.Text('DB ID:[{}]'.format(self.id))
                ,  sg.Text('Entity ID:[{}]'.format(self.entity_cd))
                ,  sg.Text('Entity Name:[{}]'.format(self.entity_name))]
                , radio_layout
                , checkbox_lyout
                , table_layout
                , [sg.Button('Add Data',key='-Sub Add-',disabled=False,disabled_button_color=radio_dic['-radio Add-'][2]),
                  sg.Button('Up Data',key='-Sub Up-',disabled=True,disabled_button_color=radio_dic['-radio Up-'][2]),
                  sg.Button('Del Data',key='-Sub Del-',disabled=True,disabled_button_color=radio_dic['-radio Del-'][2])]
                , add_column
                , [sg.Text('',key='-logs-')]]

        # ウィンドウ更新
        self.new_window = sg.Window("-- Entity Create --", Layout, size=(1100, 600), modal=False, icon=self.icon_path)

    #--------------------------
    # Tableデータレイアウト初期設定
    #--------------------------
    def getColumnsTable(self):

        columnMasterAccess = ColumnMasterAccess()
        columnMaster_list = columnMasterAccess.columnMasterSearch(self.entity_cd, self.entity_no)

        self.rowMax = 1

        results = []

        # for index in range(1, 31):
        for columnMaster in columnMaster_list:
            index = columnMaster.column_no

            not_null_flg = ""
            primary_key_flg = ""
            db_constraint = ""
            del_flg = ""

            # ☑☐☒
            mark = "☒"

            if columnMaster.not_null_flg > 0:
                    not_null_flg = "〇"

            if columnMaster.primary_key_flg > 0:
                    primary_key_flg = "〇"

            if columnMaster.del_flg > 0:
                    del_flg = "削除"

            result = [mark,
                        str(self.rowMax),
                        columnMaster.column_cd,
                        columnMaster.column_name,
                        columnMaster.modl,
                        columnMaster.digit,
                        columnMaster.accuracy,
                        not_null_flg,
                        primary_key_flg,
                        columnMaster.explanation,
                        columnMaster.db_constraint,
                        columnMaster.remarks,
                        del_flg,
                        '済']

            results.append(result)
            self.rowMax = index + 1

        return results

    #--------------------------
    # 入力項目レイアウト初期設定
    #--------------------------
    def getAddColumns(self):
            not_null_flg = ""
            primary_key_flg = ""
            db_constraint = ""
            del_flg = ""

            Models=['', 'VARCHAR2', 'NUMBER', 'DATE', 'TIMESTAMP', 'BLOB', 'RAW', 'CHAR', 'LONG']

            index = '_Add'
            col1 = [[sg.Text('No', key='-T No{}-'.format(index))],[sg.Text(self.rowMax, key='-No{}-'.format(index))]]
            col2 = [[sg.Text('Column Cd', key='-T Column Cd{}-'.format(index))],[sg.InputText('', key='-Column Cd{}-'.format(index), enable_events=True, size=(15, 1))]]
            col3 = [[sg.Text('Column Name', key='-T Column Name{}-'.format(index))],[sg.InputText('', key='-Column Name{}-'.format(index), enable_events=True, size=(15, 1))]]
            col4 = [[sg.Text('Model', key='-T Model{}-'.format(index))],[sg.Combo(Models, key='-Model{}-'.format(index), enable_events=True, size=(12, 1), readonly=True)]]
            col5 = [[sg.Text('Digit', key='-T Digit{}-'.format(index))],[sg.InputText('', key='-Digit{}-'.format(index), enable_events=True, size=(5, 1))]]
            col6 = [[sg.Text('Acc', key='-T Acc{}-'.format(index))],[sg.InputText('', key='-Acc{}-'.format(index), enable_events=True, size=(2, 1))]]
            col7 = [[sg.Text('Not Null', key='-T Not Null{}-'.format(index))],[sg.Combo(['', '〇'], key='-Not Null{}-'.format(index), default_value=not_null_flg, size=(3,1), readonly=True)]]
            col8 = [[sg.Text('PK', key='-T PK{}-'.format(index))],[sg.Combo(['', '〇'],  key='-PK{}-'.format(index), default_value=primary_key_flg, size=(3,1), readonly=True)]]
            col9 = [[sg.Text('Explanation', key='-T Explanation{}-'.format(index))],[sg.InputText('', key='-Explanation{}-'.format(index), enable_events=True, size=(15, 1))]]
            col10 = [[sg.Text('DbCons', key='-T DbCons{}-'.format(index))],[sg.InputText('', key='-DbCons{}-'.format(index), enable_events=True, size=(8, 1))]]
            col11 = [[sg.Text('Remarks', key='-T Remarks{}-'.format(index))],[sg.InputText('', key='-Remarks{}-'.format(index), enable_events=True, size=(15, 1))]]
            col12 = [[sg.Text('Del', key='-T Del Flg{}-'.format(index))],[sg.Combo(['', '削除'], key='-Del Flg{}-'.format(index), default_value=del_flg, size=(5,1), readonly=True)]]

            cols = [sg.Column(col1, element_justification='center'),
                    sg.Column(col2, element_justification='center'),
                    sg.Column(col3, element_justification='center'),
                    sg.Column(col4, element_justification='center'),
                    sg.Column(col5, element_justification='center'),
                    sg.Column(col6, element_justification='center'),
                    sg.Column(col7, element_justification='center'),
                    sg.Column(col8, element_justification='center'),
                    sg.Column(col9, element_justification='center'),
                    sg.Column(col10, element_justification='center'),
                    sg.Column(col11, element_justification='center'),
                    sg.Column(col12, element_justification='center')]

            # return cols;
            return [sg.Frame('Column Add Items', [cols], key='-Column Add Items-', visible=True)]

    #--------------------------
    # ColumnTable Data Add(仮更新)
    #--------------------------
    def addTableColumns(self, new_values):
            digit_add = new_values['-Digit_Add-']
            acc_add = new_values['-Acc_Add-']
            new_row = ['☒',
                        str(self.rowMax),
                        new_values['-Column Cd_Add-'],
                        new_values['-Column Name_Add-'],
                        new_values['-Model_Add-'],
                        new_values['-Digit_Add-'],
                        new_values['-Acc_Add-'],
                        new_values['-Not Null_Add-'],
                        new_values['-PK_Add-'],
                        new_values['-Explanation_Add-'],
                        new_values['-DbCons_Add-'],
                        new_values['-Remarks_Add-'],
                        new_values['-Del Flg_Add-'],
                        '未済']

            self.data_list.append(new_row)
            # ウィンドウ更新
            self.new_window['-Columns Table-'].update(values=self.data_list)

            field_items = ['-Column Cd_Add-',
                            '-Column Name_Add-',
                            '-Model_Add-',
                            '-Digit_Add-',
                            '-Acc_Add-',
                            '-Not Null_Add-',
                            '-PK_Add-',
                            '-Explanation_Add-',
                            '-DbCons_Add-',
                            '-Remarks_Add-',
                            '-Del Flg_Add-']

            for field_name in field_items:
                self.new_window[field_name].update('')

            self.rowMax +=1
            # ウィンドウ更新
            self.new_window['-No_Add-'].update(str(self.rowMax))

    #--------------------------
    # ColumnTable UpDate(仮更新)
    #--------------------------
    def updateTableColumns(self, new_values):
            # no_Up = new_values['-No_Add-']
            columnCd_Up = new_values['-Column Cd_Add-']
            column_Name_Up = new_values['-Column Name_Add-']
            model_Up = new_values['-Model_Add-']
            digit_Up = new_values['-Digit_Add-']
            acc_Up = new_values['-Acc_Add-']
            not_Null_Up = new_values['-Not Null_Add-']
            pK_Up = new_values['-PK_Add-']
            explanation_Up = new_values['-Explanation_Add-']
            dbConstraint_Up = new_values['-DbCons_Add-']
            remarks_Up = new_values['-Remarks_Add-']
            del_Flg_Up = new_values['-Del Flg_Add-']

            # num = int(no_Up)
            num = self.current_select_row
            # no_Up = num

            self.data_list[num][0] = '☑'
            # self.data_list[num][1] = no_Up
            self.data_list[num][2] = columnCd_Up
            self.data_list[num][3] = column_Name_Up
            self.data_list[num][4] = model_Up
            self.data_list[num][5] = digit_Up
            self.data_list[num][6] = acc_Up
            self.data_list[num][7] = not_Null_Up
            self.data_list[num][8] = pK_Up
            self.data_list[num][9] = explanation_Up
            self.data_list[num][10] = dbConstraint_Up
            self.data_list[num][11] = remarks_Up
            self.data_list[num][12] = del_Flg_Up
            self.data_list[num][13] = '未済'

            # ウィンドウ更新
            self.new_window['-Columns Table-'].update(values=self.data_list)

    #--------------------------------------
    # ColumnTableClick UpDate Data Input
    #-------------------------------------^
    def clickTableUpdateColumns(self, num):

            self.data_list[num][0] = '☑'

            no_Up = self.data_list[num][1]
            columnCd_Up = self.data_list[num][2]
            column_Name_Up = self.data_list[num][3]
            model_Up = self.data_list[num][4]
            digit_Up = self.data_list[num][5]
            acc_Up = self.data_list[num][6]
            not_Null_Up = self.data_list[num][7]
            pK_Up = self.data_list[num][8]
            explanation_Up = self.data_list[num][9]
            dbConstraint_Up = self.data_list[num][10]
            remarks_Up = self.data_list[num][11]
            del_Flg_Up = self.data_list[num][12]

            self.new_window['-No_Add-'].update(no_Up)
            self.new_window['-Column Cd_Add-'].update(columnCd_Up)
            self.new_window['-Column Name_Add-'].update(column_Name_Up)
            self.new_window['-Model_Add-'].update(model_Up)
            self.new_window['-Digit_Add-'].update(digit_Up)
            self.new_window['-Acc_Add-'].update(acc_Up)
            self.new_window['-Not Null_Add-'].update(not_Null_Up)
            self.new_window['-PK_Add-'].update(pK_Up)
            self.new_window['-Explanation_Add-'].update(explanation_Up)
            self.new_window['-DbCons_Add-'].update(dbConstraint_Up)
            self.new_window['-Remarks_Add-'].update(remarks_Up)
            self.new_window['-Del Flg_Add-'].update(del_Flg_Up)


    #--------------------------
    # 入力項目活性制御
    #--------------------------
    def visibleChangeColumns(self, no, visible_flg, disabled_flg, all_d_flg, all_v_flg):
            self.new_window['-T No_Add-'].update(visible=visible_flg)
            self.new_window['-T Column Cd_Add-'].update(visible=visible_flg)
            self.new_window['-T Column Name_Add-'].update(visible=visible_flg)
            self.new_window['-T Model_Add-'].update(visible=visible_flg)
            self.new_window['-T Digit_Add-'].update(visible=visible_flg)
            self.new_window['-T Acc_Add-'].update( visible=visible_flg)
            self.new_window['-T Not Null_Add-'].update(visible=visible_flg)
            self.new_window['-T PK_Add-'].update(visible=visible_flg)
            self.new_window['-T DbCons_Add-'].update( visible=visible_flg)
            self.new_window['-T Explanation_Add-'].update(visible=visible_flg)
            self.new_window['-T Remarks_Add-'].update(visible=visible_flg)
            self.new_window['-T Del Flg_Add-'].update(visible=visible_flg)

            self.new_window['-No_Add-'].update(no, visible=visible_flg)
            self.new_window['-Column Cd_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Column Name_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Model_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Digit_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Acc_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Not Null_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-PK_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Explanation_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-DbCons_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Remarks_Add-'].update("",disabled=disabled_flg, visible=visible_flg)
            self.new_window['-Del Flg_Add-'].update("",disabled=disabled_flg, visible=visible_flg)

            # ウィンドウ更新
            self.new_window['-Sub All Mark Select-'].update(False, disabled=all_d_flg, visible=all_v_flg)

    #--------------------------
    # validateおよび行追加
    #--------------------------
    def validateAdd(self, new_values):
            column_cd_add = new_values['-Column Cd_Add-']
            column_name_add = new_values['-Column Name_Add-']
            model_add = new_values['-Model_Add-']
            digit_add = new_values['-Digit_Add-']
            acc_add = new_values['-Acc_Add-']

            skip_flg = False
            if column_cd_add and column_name_add and model_add:
                if model_add in ('VARCHAR2','CHAR', 'RAW'):
                    if not digit_add:
                        sg.popup_ok('Digit　が未設定です', title = 'Validate Error');
                        skip_flg = True

                if model_add in ('NUMBER'):
                    if not digit_add or not acc_add:
                        sg.popup_ok('Digit　もしく、Acc　が未設定です', title = 'Validate Error');
                        skip_flg = True
            else:
                sg.popup_ok('Column Cd Column Name Model のいずれかが未設定です', title = 'Validate Error');
                skip_flg = True

            return skip_flg

    #--------------------------
    # GUI表示ループ
    #--------------------------
    def windowsOpen(self):
        while True:
            new_event, new_values = self.new_window.read()
            # print('-------------------new_event:{}'.format(new_event))
            # print('-------------------new_values:{}'.format(new_values))
            # ウィンドウ閉じるボタン押下時
            if new_event in (sg.WIN_CLOSED, 'Exit'):
                # print('new_event1:{}/{}'.format(new_values,self.no))
                # print('new_event2:{}/{}'.format(new_event,self.no))
                self.new_window.close()
                break;

            # カラムID入力制限
            if new_event == '-Column Cd_Add-' and new_values['-Column Cd_Add-'] and not re.search(r"[a-zA-Z0-9_]+", new_values['-Column Cd_Add-'][-1]):
                self.new_window['-Column Cd_Add-'].update(new_values['-Column Cd_Add-'][:-1])

            if new_event == '-Column Cd_Add-' and len(new_values['-Column Cd_Add-']) > 31:
                self.new_window['-Column Cd_Add-'].update(new_values['-Column Cd_Add-'][:-1])

            # カラム名入力制限
            if new_event == '-Column Name_Add-' and len(new_values['-Column Name_Add-'].encode('utf-8')) > 31:
                self.new_window['-Column Name_Add-'].update(new_values['-Column Name_Add-'][:-1])

            # Digite入力制限
            if new_event == '-Digit_Add-' and new_values['-Digit_Add-'] and not re.search(r"[0-9]+", new_values['-Digit_Add-'][-1]):
                self.new_window['-Digit_Add-'].update(new_values['-Digit_Add-'][:-1])

            if new_event == '-Digit_Add-' and len(new_values['-Digit_Add-']) > 4:
                self.new_window['-Digit_Add-'].update(new_values['-Digit_Add-'][:-1])

            # Digite入力制限
            if new_event == '-Acc_Add-' and new_values['-Acc_Add-'] and not re.search(r"[0-9]+", new_values['-Acc_Add-'][-1]):
                self.new_window['-Acc_Add-'].update(new_values['-Acc_Add-'][:-1])

            if new_event == '-Acc_Add-' and len(new_values['-Acc_Add-']) > 2:
                self.new_window['-Acc_Add-'].update(new_values['-Acc_Add-'][:-1])

            # DB制約入力制限 1024
            if new_event == '-Explanation_Add-' and len(new_values['-Explanation_Add-'].encode('utf-8')) > 1024:
                self.new_window['-Explanation_Add-'].update(new_values['-Explanation_Add-'][:-1])

            # DB制約入力制限 256
            if new_event == '-DbCons_Add-' and new_values['-DbCons_Add-'] and not re.search(r"[\(a-zA-Z0-9_\)]+", new_values['-DbCons_Add-'][-1]):
                self.new_window['-DbCons_Add-'].update(new_values['-DbCons_Add-'][:-1])

            # 備考力制限 1024
            if new_event == '-Remarks_Add-' and len(new_values['-Remarks_Add-'].encode('utf-8')) > 1024:
                self.new_window['-Remarks_Add-'].update(new_values['-Remarks_Add-'][:-1])

            # カラムTable選択イベント
            if new_event == '-Columns Table-':
                gen = (i for i in new_values['-Columns Table-'])
                # print('-Columns Table-{}'.format(gen))
                for num in gen:

                    # ラジオボタン　削除選択時
                    if new_values['-radio Del-']:
                        # print(member_list[num][4])
                        mark = self.data_list[num][0]
                        if mark == '☐':
                            self.data_list[num][0] = '☑'
                        if mark == '☑':
                            self.data_list[num][0] = '☐'

                    # ラジオボタン　更新選択時
                    elif  new_values['-radio Up-']:
                        for i,datas in enumerate(self.data_list):
                            self.data_list[i][0] = '☐'

                            # ColumnTableクリック時、入力項目設定
                            self.clickTableUpdateColumns(num)

                    # ラジオボタン　追加選択時
                    else:
                        for i,datas in enumerate(self.data_list):
                            self.data_list[i][0] = '☒'

                    # ウィンドウ更新
                    self.new_window['-Columns Table-'].update(values=self.data_list)

                    # 選択カレント行設定
                    self.current_select_row = num

            # Columnデータ反映処理
            if new_values['menu2'] == "Save" or new_event == 'Save':
                # ColumnMaster Insert
                columnMasterAccess = ColumnMasterAccess()
                columnMasterAccess.columnMasterInsert(data_list=self.data_list, entity_cd=self.entity_cd, entity_no=self.entity_no)
                # Data取得
                self.data_list = self.getColumnsTable()
                # ウィンドウ更新
                self.new_window['-Columns Table-'].update(values=self.data_list)
                # pass

            # Columnデータ更新（仮更新）
            if new_event == '-Sub Up-':
                print('--------Up')
                self.updateTableColumns(new_values)

            # Columnデータ追加（仮追加）
            if new_event == '-Sub Add-':
                print('--------Add')
                skip_flg = self.validateAdd(new_values)

                if skip_flg == False:
                    self.addTableColumns(new_values)

            # Columnデータ削除（仮削除「物理」）
            if new_event == '-Sub Del-':
                print('--------Del')
                indexs = []
                for i,datas in enumerate(self.data_list):
                    mark = self.data_list[i][0]
                    if mark == '☑':
                        indexs.append(i)
                    self.data_list[i][13] = '未済'

                # NumPy配列ndarrayにて一括削除
                del_data_list = np.delete(self.data_list, indexs, 0)

                # NumPy配列ndarrayをリストに変換: tolist()
                self.data_list = del_data_list.tolist()

                # 行No降り直し
                for i,datas in enumerate(self.data_list):
                    self.data_list[i][1] = i + 1

                # 最後の行番号にプラス１
                self.rowMax = len(self.data_list) + 1

                # ウィンドウ更新
                self.new_window['-Columns Table-'].update(values=self.data_list)

            #  ラジオボタンイベント
            if '-radio' in new_event:
                # ラジオボタン 追加選択時
                if new_event == '-radio Add-':
                    self.new_window['-Sub Add-'].update(disabled=False, disabled_button_color=(None,None))
                    self.new_window['-Sub Up-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
                    self.new_window['-Sub Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

                    for i,datas in enumerate(self.data_list):
                        self.data_list[i][0] = '☒'

                    # ウィンドウ更新
                    self.new_window['-Columns Table-'].update(values=self.data_list)

                    # 入力項目制御
                    self.visibleChangeColumns(no=self.rowMax, visible_flg=True, disabled_flg=False, all_d_flg=True, all_v_flg=False)

                # ラジオボタン 更新選択時
                elif new_event == '-radio Up-':
                    self.new_window['-Sub Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
                    self.new_window['-Sub Up-'].update(disabled=False, disabled_button_color=(None,None))
                    self.new_window['-Sub Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

                    for i,datas in enumerate(self.data_list):
                        self.data_list[i][0] = '☐'

                    # ウィンドウ更新
                    self.new_window['-Columns Table-'].update(values=self.data_list)

                    # 入力項目制御
                    self.visibleChangeColumns(no='', visible_flg=True, disabled_flg=False, all_d_flg=True, all_v_flg=False)

                # ラジオボタン 削除選択時
                else:
                    self.new_window['-Sub Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
                    self.new_window['-Sub Up-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
                    self.new_window['-Sub Del-'].update(disabled=False, disabled_button_color=(None,None))

                    for i,datas in enumerate(self.data_list):
                        self.data_list[i][0] = '☐'

                    # ウィンドウ更新
                    self.new_window['-Columns Table-'].update(values=self.data_list)

                    # 入力項目制御
                    self.visibleChangeColumns(no='-', visible_flg=False, disabled_flg=True, all_d_flg=False, all_v_flg=True)

            # チェックボックス　一覧チェックボックス全選択・解除イベント
            if new_event == '-Sub All Mark Select-':
                selection_flg = new_values['-Sub All Mark Select-']
                print('--------Sub All Mark Select:{}'.format(selection_flg))
                # チェックありの場合
                if selection_flg:
                    for i,datas in enumerate(self.data_list):
                        self.data_list[i][0] = '☑'
                # チェックなしの場合
                else:
                    for i,datas in enumerate(self.data_list):
                        self.data_list[i][0] = '☐'

                # ウィンドウ更新
                self.new_window['-Columns Table-'].update(values=self.data_list)

        # ウィンドウクローズ
        self.new_window.close()
