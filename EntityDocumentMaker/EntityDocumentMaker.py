#!/usr/bin/env python
# coding: utf-8
# +-----------------------------------------------------------------------------------+
# + クラスインポート
# +-----------------------------------------------------------------------------------+
import PySimpleGUI as sg
import os
import re
import numpy as np
# import threading

from SettingEntityAccess import SettingEntityAccess
from EntityMasterAccess import EntityMasterAccess
from ColumnMasterAccess import ColumnMasterAccess
from entityExcelRead import EntityRead
from ConfigManager import ConfigManager
from subWindows import SubWindows
from entityExcelWrite import EntityExcelWrite
from CreateTableSQLFileMake import CreateTableSQLFileMake
from FileOperation import FileOperation

#sg.theme_previewer()

# +-----------------------------------------------------------------------------------+
# + PysimpleGUI テーマ設定
# +-----------------------------------------------------------------------------------+
sg.theme('GreenMono')

# +-----------------------------------------------------------------------------------+
# + クラスインスタンス化
# +-----------------------------------------------------------------------------------+
settingEntityAccess = SettingEntityAccess()
entityMasterAccess = EntityMasterAccess()
columnMasterAccess = ColumnMasterAccess()
fileOperation = FileOperation()
entityRead = EntityRead()
configManager = ConfigManager()
entityRead = EntityRead()

# +-----------------------------------------------------------------------------------+
# + 初期データリスト
# +-----------------------------------------------------------------------------------+
# 登録されている設定データを全件取得する
setting_list = settingEntityAccess.entitySearchAll()
# Entity masterデータを全件取得する
entityMaster_list = entityMasterAccess.entityMasterSearchAll()

# Type区分を取得
typeValues = configManager.getSectionValus('TYPE')
typeDefaultValue = configManager.getSectionDefaultValu('TYPE')

# Dcument区分を取得
docTypeValues = configManager.getSectionValus('DOC_TYPE')
docTypeDefaultValue = configManager.getSectionDefaultValu('DOC_TYPE')

# テーブル区分を取得
tableTypeValues = configManager.getSectionValus('TEABLE_TYPES')
tableTypeDefaultValue = configManager.getSectionDefaultValu('TEABLE_TYPES')

# Versionを取得
appVersion = configManager.getAppVersion()

# ENTITY MASTER の最大行を取得する。
entityNoMax = entityMasterAccess.getEntityNoMax()

# Icon Pathを取得
icon_path = ".\FjiYama.ico"

# +-----------------------------------------------------------------------------------+
# + 行番号振りなおし
# +-----------------------------------------------------------------------------------+
def renumbering():
    row_no = 1
    for row in setting_list:
        row[0] = row_no
        row_no += 1

# +-----------------------------------------------------------------------------------+
# + 行番号振りなおし
# +-----------------------------------------------------------------------------------+
def dataRenumbering():
    row_no = 1
    print('---entityMaster_list[{}]'.format(entityMaster_list))
    for row in entityMaster_list:
        print('---row[1][{}]'.format(row[1]))
        row[1] = row_no
        row_no += 1

# +-----------------------------------------------------------------------------------+
# + エンティティ　追加項目　初期レイアウト設定
# +-----------------------------------------------------------------------------------+
def getEntityAddItemsLayout():

    rowMax = len(entityMaster_list) + 1

    index = '_Add'
    col1 = [[sg.Text('No', key='-T No{}-'.format(index))],[sg.Text(rowMax, key='-No{}-'.format(index))]]
    col2 = [[sg.Text('Type', key='-T Type{}-'.format(index))],[sg.Combo(typeValues, key='-Type Section{}-'.format(index), default_value=typeDefaultValue, readonly=True, size=(10, 1))]]
    col3 = [[sg.Text('Section', key='-T Table Section{}-'.format(index))],[sg.Combo(tableTypeValues,  key='-Entity Section{}-'.format(index), default_value=tableTypeDefaultValue, readonly=True, size=(10, 1))]]
    col4 = [[sg.Text('Entity Cd', key='-T Entity Cd{}-'.format(index))],[sg.InputText('', key='-Entity Cd{}-'.format(index), enable_events=True, size=(15, 1))]]
    col5 = [[sg.Text('Entity Name', key='-T Entity Name{}-'.format(index))],[sg.InputText('', key='-Entity Name{}-'.format(index), enable_events=True, size=(15, 1))]]
    col6 = [[sg.Text('Entity Explanation', key='-T Entity Explanation{}-'.format(index))],[sg.InputText('', key='-Entity Explanation{}-'.format(index), enable_events=True, size=(30, 1))]]


    cols = [sg.Column(col1, element_justification='center'),
            sg.Column(col2, element_justification='center'),
            sg.Column(col3, element_justification='center'),
            sg.Column(col4, element_justification='center'),
            sg.Column(col5, element_justification='center'),
            sg.Column(col6, element_justification='center')]

    # 初期表示は、非表示
    return [sg.Frame('Entity Add Items', [cols], key='-Entity Add Items-', visible=False)];


# +-----------------------------------------------------------------------------------+
# + エンティティ　検索項目　初期レイアウト設定
# +-----------------------------------------------------------------------------------+
def getEntitySearchItemsLayout():

    rowMax = len(entityMaster_list) + 1

    index = '_Search'
    col1 = [[sg.Text('Type', key='-T Type{}-'.format(index))],[sg.Combo(typeValues, key='-Type Section{}-'.format(index), default_value=typeDefaultValue, readonly=True, size=(10, 1))]]
    col2 = [[sg.Text('Section', key='-T Table Section{}-'.format(index))],[sg.Combo(tableTypeValues,  key='-Entity Section{}-'.format(index), default_value=tableTypeDefaultValue, readonly=True, size=(10, 1))]]
    col3 = [[sg.Text('Entity Cd', key='-T Entity Cd{}-'.format(index))],[sg.InputText('', key='-Entity Cd{}-'.format(index), enable_events=True, size=(15, 1))]]
    col4 = [[sg.Text('Entity Name', key='-T Entity Name{}-'.format(index))],[sg.InputText('', key='-Entity Name{}-'.format(index), enable_events=True, size=(15, 1))]]
    col5 = [[sg.Text('Column Cd', key='-T Column Cd{}-'.format(index))],[sg.InputText('', key='-Column Cd{}-'.format(index), enable_events=True, size=(15, 1))]]
    col6 = [[sg.Text('Column Name', key='-T Column Name{}-'.format(index))],[sg.InputText('', key='-Column Name{}-'.format(index), enable_events=True, size=(30, 1))]]


    cols = [sg.Column(col1, element_justification='center'),
            sg.Column(col2, element_justification='center'),
            sg.Column(col3, element_justification='center'),
            sg.Column(col4, element_justification='center'),
            sg.Column(col5, element_justification='center'),
            sg.Column(col6, element_justification='center')
            ]

    # 初期表示は、非表示
    return [sg.Frame('Entity Search Items', [cols,
                [sg.Button('Search', key='-Entity Search-'),
                sg.Button('Clear', key='-Entity Clear-')]
                ], key='-Entity Search Items-', visible=True)];

# +-----------------------------------------------------------------------------------+
# + エンティティ　追加項目　クリア
# +-----------------------------------------------------------------------------------+
def clearEntityAddItems():

    rowMax = len(entityMaster_list) + 1

    index = '_Add'
    window['-No{}-'.format(index)].update(rowMax)
    window['-Type Section{}-'.format(index)].update('')
    window['-Entity Section{}-'.format(index)].update('')
    window['-Entity Cd{}-'.format(index)].update('')
    window['-Entity Name{}-'.format(index)].update('')
    window['-Entity Explanation{}-'.format(index)].update('')

#--------------------------
# validateおよび行追加
#--------------------------
def validateAdd(values):
    type_scetion_add = values['-Type Section_Add-']
    entity_section_add = values['-Entity Section_Add-']
    entity_cd_add = values['-Entity Cd_Add-']
    entity_name_add = values['-Entity Name_Add-']
    entity_Explanation_add = values['-Entity Explanation_Add-']

    skip_flg = True
    if type_scetion_add and entity_section_add and entity_cd_add and entity_name_add:
        skip_flg = True

    else:
        sg.popup_ok('Type,Section,Entity Cd,Entity Name のいずれかが未設定です', title = 'Validate Error');
        skip_flg = False

    return skip_flg

# +-----------------------------------------------------------------------------------+
# + エンティティ　検索項目　クリア
# +-----------------------------------------------------------------------------------+
def clearEntitySearchItems():

    index = '_Search'
    window['-Type Section{}-'.format(index)].update('')
    window['-Entity Section{}-'.format(index)].update('')
    window['-Entity Cd{}-'.format(index)].update('')
    window['-Entity Name{}-'.format(index)].update('')
    window['-Column Cd{}-'.format(index)].update('')
    window['-Column Name{}-'.format(index)].update('')

# +-----------------------------------------------------------------------------------+
# + レイアウト設定
# +-----------------------------------------------------------------------------------+
# ------ Menu Definition ------ #
menu_def = [['File', ['Open', ['Folder Open', 'Entity Open'],'Quit']],
            ['Run', ['Reload', ['Reload FolderPath', 'Reload Entity', ],['Reflection',['Setting Reflection', 'Entity Reflection', ]]]],
            ['Help', 'About app...'], ]

# +-----------------------------------------------------------------------------------+
# + ヘッダー表示リスト作成
# +-----------------------------------------------------------------------------------+
# Sttingデータ表示ヘッダー
setting_header =  ['No', 'Type', 'Doc Type', 'Import Folder Path', 'Register']
# Entity Masterデータ表示ヘッダー
entity_master_header = ['Mark',
                        'No',
                        'Type',
                        'Section',
                        'Entity Cd',
                        'Entity Name',
                        'Full Doc Path',
                        'Ref',
                        'Del Type',
                        'Type Section',
                        'Del',
                        'Id',
                        'Entity No',
                        'Section value',
                        'Explanation']

# Entity Masterデータ表示制御
visible_column_maps = [True,
                     True,
                     True,
                     True,
                     True,
                     True,
                     True,
                     True,
                     False,
                     False,
                     False,
                     False,
                     True,
                     False,
                     False]

# Entity Masterデータ表示幅
col_widthss = [5,
               3,
               6,
               8,
               16,
               16,
               33,
               5,
               5,
               5,
               5,
               5,
               8,
               8,
               30]

# radio button 設定値を辞書にて設定
radio_dic = {
                '-radio Open-': ['Open Entity', True, (None,None)],
                '-radio Add-': ['Add Entity', False, ('#d3d3d3','#d3d3d3')],
                '-radio Del-': ['Del Entity', False, ('#d3d3d3','#d3d3d3')],
                '-radio CreateFile-': ['Create File', False, ('#d3d3d3','#d3d3d3')],
            }

# +-----------------------------------------------------------------------------------+
# + ラジオボタンLayout
# +-----------------------------------------------------------------------------------+
radio_layout = [sg.Radio(item[1][0],
                key=item[0],
                group_id='-Radio change-',
                default=item[1][1],
                enable_events=True) for item in radio_dic.items()]

# +-----------------------------------------------------------------------------------+
# + 全選択・全解除チェックボックスLayout
# +-----------------------------------------------------------------------------------+
checkbox_layout = [sg.Checkbox('All Mark Select',
                    key='-All Mark Select-',
                    enable_events=True,
                    default=False,
                    disabled=True,
                    visible=False)]

control_layout = [sg.Frame('Entity Control Items', [radio_layout,checkbox_layout],
                    key='-Entity Control Items-', visible=True)]

search_layout = getEntitySearchItemsLayout()


# ------ Tab1 Definition ------ #
t1 = sg.Tab('Entity Master' ,[[sg.Button('Quit',key='Quit'),
        sg.Button('Entity Reload', key='-Entity Reload-', pad=((640, 0),(0,0)))],
        search_layout,
        control_layout,
        [sg.Table(
            values=entityMaster_list,
            headings=entity_master_header,
            auto_size_columns=False,
            col_widths=col_widthss,
            visible_column_map=visible_column_maps,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            justification='left',
            enable_events=True,
            text_color='#000000',
            background_color='#cccccc',
            alternating_row_color='#ffffff',
            header_text_color='#0000ff',
            header_background_color='#cccccc',
            vertical_scroll_only=False,
            key='-Entity Table-',
            size=(850, 10),
            )],
            [sg.Button('Entity Open',key='-Entity Open-',disabled=False,disabled_button_color=radio_dic['-radio Add-'][2]),
             sg.Button('Entity Add',key='-Entity Add-',disabled=True,disabled_button_color=radio_dic['-radio Add-'][2]),
             sg.Button('Entity Del',key='-Entity Del-',disabled=True,disabled_button_color=radio_dic['-radio Del-'][2]),
             sg.Button('CreateSql File',key='-CreateSql File-',disabled=True,disabled_button_color=radio_dic['-radio CreateFile-'][2]),
             sg.Button('CreateExcel File',key='-CreateExcel File-',disabled=True,disabled_button_color=radio_dic['-radio CreateFile-'][2]),
             sg.Button('Folder Open',key='-Folder Open-',disabled=False, disabled_button_color=radio_dic['-radio Add-'][2])
             ],
            getEntityAddItemsLayout(),
            [sg.Button('Entity Reflection',key='-Entity Ref-',disabled=True, disabled_button_color=radio_dic['-radio Add-'][2], pad=((680, 0),(0,0)))]
            ])

# ------ Tab2 Definition ------ #
t2 = sg.Tab('Import Folder' ,[[sg.Button('Quit',key='Quit'),sg.Button('Reload',key='Reload', pad=((640, 0),(0,0)))],
        [sg.Table(
            values=setting_list,
            headings=setting_header,
            auto_size_columns=False,
            col_widths=[5, 8, 15, 60, 10],
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            justification='left',
            enable_events=True,
            text_color='#000000',
            background_color='#cccccc',
            alternating_row_color='#ffffff',
            header_text_color='#0000ff',
            header_background_color='#cccccc',
            key='-Settig Table-',
            size=(800, 10),
            )],
            [sg.Button('Add',key='Add'),sg.Button('Del',key='Del'),sg.Button('Reflection', key='Ref', pad=((600, 0),(0,0)))],
            [sg.Text("Import Type         :"),sg.Combo(typeValues, default_value=typeDefaultValue, key='-SET_Combo TYPE-', size=(10,1))],
            [sg.Text("Import Doc Type   :"),sg.Combo(docTypeValues, default_value=docTypeDefaultValue, key='-SET_Combo DOC_TYPE-', size=(20,1))],
            [sg.Text("Import Folder Path:"),sg.Input(key='-IFP-'),sg.FolderBrowse('Select')]]
            )

Layout = [[sg.Menu(menu_def, key='menu1')],
         [sg.TabGroup([[t1,t2]], size = (950, 600))]]

# +-----------------------------------------------------------------------------------+
# + ウィンドウ作成
# +-----------------------------------------------------------------------------------+
window = sg.Window('-- Entity Document Maker --', Layout, resizable=True, size=(960, 650), icon=icon_path)

# +-----------------------------------------------------------------------------------+
# + Windowsイベント処理ループ
# +-----------------------------------------------------------------------------------+
while True:
    # イベントの読み取り（イベント待ち）
    event, values = window.read()
    # 終了条件（None:クローズボタン）
    if event in (sg.WIN_CLOSED, 'Quit'):
        break

    # EntityCd入力制限　半角英数文字
    if event == '-Entity Cd_Search-' and values['-Entity Cd_Search-'] and not re.search(r"[a-zA-Z0-9_]+", values['-Entity Cd_Search-'][-1]):
        window['-Entity Cd_Search-'].update(values['-Entity Cd_Search-'][:-1])

    if event == '-Entity Cd_Search-' and len(values['-Entity Cd_Search-']) > 31:
        window['-Entity Cd_Search-'].update(values['-Entity Cd_Search-'][:-1])

    # EntityName入力制限　UTF-8での256文字まで有効
    if event == '-Entity Name_Search-' and len(values['-Entity Name_Search-'].encode('utf-8')) > 257:
        window['-Entity Name_Search-'].update(values['-Entity Name_Search-'][:-1])

    # Column　Cd入力制限　半角英数文字
    if event == '-Column Cd_Search-' and values['-Column Cd_Search-'] and not re.search(r"[a-zA-Z0-9_]+", values['-Column Cd_Search-'][-1]):
        window['-Column Cd_Search-'].update(values['-Column Cd_Search-'][:-1])

    if event == '-Column Cd_Search-' and len(values['-Column Cd_Search-']) > 31:
        window['-Column Cd_Search-'].update(values['-Column Cd_Search-'][:-1])

    # Column　Name入力制限　UTF-8での256文字まで有効
    if event == '-Column Name_Search-' and len(values['-Column Name_Search-'].encode('utf-8')) > 257:
        window['-Column Name_Search-'].update(values['-Column Name_Search-'][:-1])

    # EntityCd入力制限　半角英数文字
    if event == '-Entity Cd_Add-' and values['-Entity Cd_Add-'] and not re.search(r"[a-zA-Z0-9_]+", values['-Entity Cd_Add-'][-1]):
        window['-Entity Cd_Add-'].update(values['-Entity Cd_Add-'][:-1])

    if event == '-Entity Cd_Add-' and len(values['-Entity Cd_Add-']) > 31:
        window['-Entity Cd_Add-'].update(values['-Entity Cd_Add-'][:-1])

    # EntityName入力制限　UTF-8での256文字まで有効
    if event == '-Entity Name_Add-' and len(values['-Entity Name_Add-'].encode('utf-8')) > 257:
        window['-Entity Name_Add-'].update(values['-Entity Name_Add-'][:-1])

    # 検索
    if event == '-Entity Search-':
        print('--------Search')
        # 検索項目取得
        type_in=values['-Type Section_Search-']
        section=values['-Entity Section_Search-']
        entity_cd=values['-Entity Cd_Search-']
        entity_name=values['-Entity Name_Search-']
        column_cd=values['-Column Cd_Search-']
        column_name=values['-Column Name_Search-']

        # Entity検索
        entityMaster_list = entityMasterAccess.entitySearch(type_in=type_in,
                                                            section=section,
                                                            entity_cd=entity_cd,
                                                            entity_name=entity_name,
                                                            column_cd=column_cd,
                                                            column_name=column_name)

        # ウィンドウ更新
        window['-Entity Table-'].update(values=entityMaster_list)

    # 検索clear
    if event == '-Entity Clear-':
        clearEntitySearchItems()

    # 仮登録
    if event == 'Add':
        # print(len(setting_list))
        # 最大行を取得する
        max_row = len(setting_list) + 1

        # 選択された取込先フォルダパスを取得する
        folder_path = values['-IFP-']
        typeSectionKey = values['-SET_Combo TYPE-']
        docTypeSectionKey =values['-SET_Combo DOC_TYPE-']
        # 取込先フォルダパスが設定されていれば、行追加
        if typeSectionKey and docTypeSectionKey and folder_path:
            typeSectionValue = configManager.getTypeSectionValue(typeSectionKey)
            docTypeSectionValue = configManager.getDocTypeSectionValue(docTypeSectionKey)

            # 新規行を追加　⇒一時仮設定のため、Id（自動採番のため）はNoneとしておく
            setting_list.append([str(max_row), typeSectionKey, docTypeSectionKey, folder_path.replace('/', '\\'), '未済', None, typeSectionValue, docTypeSectionValue])
        else:
            # フォルダ未設定の場合は、選択を即すメッセージをポップアップ表示
            sg.popup_error('タイプもしくは、フォルダを選択してください。',title = 'error')
        # Windowウィジェットに対してデータ配列を再設定
        window['-Settig Table-'].update(values=setting_list)

    # 削除処理
    if event == 'Del':
        # 行選択判定
        if values['-Settig Table-']:

            # 選択行のセルデータを取得（ジェネレータ）
            gen = (i for i in values['-Settig Table-'])
            for num in gen:
                # 登録済みの場合、確認後、削除
                if setting_list[num][4]:
                    # 削除確認
                    mess = sg.popup_ok_cancel('登録済みのデータですが、No.{}を削除しますか？'.format(setting_list[num][0]),title = 'delete confirm')
                    if mess == "OK":
                        print("---選択行:{}----".format(setting_list[num][1]))
                        type_name = setting_list[num][2]
                        del setting_list[num]
                        # 設定リストのNoを再振り直し
                        renumbering()
                        sg.popup_ok('Type={}を削除しました。'.format(type_name),title = 'delete confirm');
                        window['-Settig Table-'].update(values=setting_list)
                    else:
                        break;

                # 未登録の場合、即削除
                else:
                    print("---選択行:{}----".format(setting_list[num][1]))
                    type_name = setting_list[num][2]
                    del setting_list[num]
                    renumbering()
                    sg.popup_ok('Type={}を削除しました。'.format(type_name),title = 'delete results');
                    window['-Settig Table-'].update(values=setting_list)

        # 行未選択の場合、選択メッセージを表示
        else:
            sg.popup_error('削除行を選択してください。',title = 'error')

    # DB反映処理
    if event == 'Ref' or values['menu1'] == 'Setting Reflection':
        if len(setting_list) < 1:
            mess = sg.popup_ok_cancel('完全全削除を実施しますか？',title = 'Delete confirm')
            if mess == "OK":
                # 設定情報の削除
                settingEntityAccess.entityAllDelete()
        else:
            mess = sg.popup_ok_cancel('反映処理を実施しますか？',title = 'Reflection confirm')
            if mess == "OK":
                # 設定情報の登録処理
                settingEntityAccess.entityInsert(setting_list)
                sg.popup_ok('{}件 正常に反映処理が終了しました。'.format(str(len(setting_list))),title = 'Reflection results')
                # 設定エンティティ全件取得
                setting_list = settingEntityAccess.entitySearchAll()
                # windowsウィジェット再設定
                window['-Settig Table-'].update(values=setting_list)
            else:
                sg.popup_ok('反映処理を中止しました。',title = 'Reflection stop')

    # 設定データ再読み込み処理
    if event == 'Reload' or values['menu1'] == 'Reload FolderPath':
        #再読み込み実施
        if len(setting_list) > 0:
            # 設定エンティティ全件取得
            setting_list = settingEntityAccess.entitySearchAll()
            # windowsウィジェット再設定
            window['-Settig Table-'].update(values=setting_list)
            sg.popup_ok('再設定読み込み件数 {}件です。'.format(str(len(setting_list))),title='reload..')
        else:
            sg.popup_ok('再設定読み込み件数 0件です。',title = 'reload results')

    # Entityデータ全再読み込み処理（注意！全件再上書きされる）
    if event == '-Entity Reload-' or values['menu1'] == 'Reload Entity':

            # # 未反映処理データチェック
            # skip_flg = False
            # for i,datas in enumerate(entityMaster_list):
            #     if entityMaster_list[i][7] == '未済':
            #         skip_flg = True
            #
            # # 未反映処理データがある場合は、Reloadは実施しない
            # if skip_flg:
            #     mess=sg.popup_ok_cancel('未反映データがあります。\n再読み込みを実行しますか？',title='Warning..')
            #     if mess == "Cancel":
            #         continue
            mess=sg.popup_ok_cancel('Entityデータが再読み込みデータに上書きされます。'+\
                                    '\n新規登録データは、一括削除されます。'+\
                                    '\n再読み込みを実行しますか？',title='Warning..')
            if mess == "Cancel":
                continue

            # エンティティ定義書一括読み込み
            # Settingで登録されたエンティティ定義書読み込みFolderより、
            # Entityデータを再読込。
            count = entityRead.startRead()
            sg.popup_ok('定義書読込み件数 {}件です。'.format(str(count),title='reload..'))

            # エンティティマスター全件取得
            entityMaster_list = entityMasterAccess.entityMasterSearchAll()
            if len(entityMaster_list) > 0:

                for i,datas in enumerate(entityMaster_list):
                    entityMaster_list[i][0] = '☐'

                # ウィンドウ更新
                window['-Entity Table-'].update(values=entityMaster_list)

            else:
                sg.popup_ok('定義書読込み件数 0件です。',title = 'reload results')

            # button制御
            window['-Entity Open-'].update(disabled=False, disabled_button_color=(None,None))
            window['-Entity Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateSql File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateExcel File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

            # ラジオボタン Open
            window['-radio Open-'].update(True)
            # Entity items Add 全非表示
            window['-Entity Add Items-'].update(visible=False)
            clearEntityAddItems()

            # 全選択チェックボックス　チェックなし・無効・非表示
            window['-All Mark Select-'].update(False, disabled=True, visible=False)

    # このアプリについて
    if values['menu1'] == 'About app...':

        # About Setting
        messg = '＜MIT License＞\n\n' + \
                'Entity Document Maker version {} \n\n'.format(appVersion) + \
                'Copyright (c) 2022 G-jon FujiYama\n\n' + \
                'The OS used is Windows only\n'

        sg.popup_ok(messg, title = 'About app...')

    # エンティティ　カラムマスターOPEN
    if values['menu1'] == "Entity Open" or event == '-Entity Open-':
        print('-----valus:{}'.format(values))
        ragio_open = values['-radio Open-']

        if ragio_open:
            num = 0
            open_flg = False
            for index,data in enumerate(entityMaster_list):
                if data[0] == '☑':
                    num = index
                    open_flg = True

            if open_flg:
                # ファイルフルパスを取得
                id = entityMaster_list[num][11]
                entity_no = entityMaster_list[num][12]
                entity_cd = entityMaster_list[num][4]
                entity_name = entityMaster_list[num][5]
                # ref取得
                entity_ref = entityMaster_list[num][7]
                if entity_ref == '済':
                    # フォルダOPEN確認
                    mess = sg.popup_ok_cancel('{}を開きますか？'.format(entity_name),title = 'Confirm Open Entity')
                    if mess == "OK":
                        print("---選択行:{}----".format(entityMaster_list[num][4]))
                        # フォルダOPEN処理
                        subWindows = SubWindows(id=id , entity_cd=entity_cd, entity_name=entity_name, entity_no=entity_no)
                        subWindows.windowsOpen()
                else:
                    mess = sg.popup_ok('Entity未反映はOPEN出来ません。\n\nReflectionを押下してください。',
                                        title = 'Warning Entity Open')
            else:
                mess = sg.popup_ok('OpenするEntityを選択してください。',title = 'Warning Entity Open')
        else:
            mess = sg.popup_ok('Open Entity を指定してください。',title = 'Warning Open Entity')

    # エンティティデータ追加（仮追加）
    if event == '-Entity Add-':
        print('--------Add')

        if not entityNoMax:
            entityNoMax = entityMasterAccess.getEntityNoMax()

        entityNoMax += 1

        # 仮新規登録データを設定
        mark='☒'
        row_count=len(entityMaster_list)+1
        type_section_name=values['-Type Section_Add-']
        entity_section_name=values['-Entity Section_Add-']
        entity_cd=values['-Entity Cd_Add-']
        entity_name=values['-Entity Name_Add-']
        entity_document_path = '-- No file due to new registration --'
        ref='未済'
        del_type=''
        entity_section=configManager.getTableTypeSectionValue(entity_section_name)
        del_flg=0
        id=0
        entity_no=entityNoMax
        type_section=configManager.getTypeSectionValue(type_section_name)
        explanation=values['-Entity Explanation_Add-']

        # print('---------------------------')
        # print(mark)
        # print(row_count)
        # print(type_section_name)
        # print(entity_section_name)
        # print(entity_cd)
        # print(entity_name)
        # print(entity_document_path)
        # print(ref)
        # print(del_type)
        # print(entity_section)
        # print(del_flg)
        # print(id)
        # print(entity_no)
        # print(type_section)
        # print(explanation)
        # print('---------------------------')

        # 仮登録データのvalidateチェック
        if validateAdd(values):
            entityMaster_data = []
            entityMaster_data.append(mark)
            entityMaster_data.append(row_count)
            entityMaster_data.append(type_section_name)
            entityMaster_data.append(entity_section_name)
            entityMaster_data.append(entity_cd)
            entityMaster_data.append(entity_name)
            entityMaster_data.append(entity_document_path)
            entityMaster_data.append(ref)
            entityMaster_data.append(del_type)
            entityMaster_data.append(type_section)
            entityMaster_data.append(del_flg)
            entityMaster_data.append(id)
            entityMaster_data.append(entity_no)
            entityMaster_data.append(entity_section)
            entityMaster_data.append(explanation)

            # Entity データリスト追加
            entityMaster_list.append(entityMaster_data)
            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)
            clearEntityAddItems()

    # エンティティデータ削除（仮削除）
    if event == '-Entity Del-':
        print('--------Del')
        indexs = []
        for index,data in enumerate(entityMaster_list):
            if data[0] == '☑':
                indexs.append(index)
            data[7] = '未済'

        if len(indexs) > 0:

            mess = sg.popup_ok_cancel('{}件 仮削除しますがよろしいですか？\n削除確定はReflectionを実施してください。'.format(len(indexs)),
                                        title = 'Confirm...')
            if mess == "OK":
                # NumPy配列ndarrayにて一括削除
                del_data_list = np.delete(entityMaster_list, indexs, 0)

                # NumPy配列ndarrayをリストに変換: tolist()
                entityMaster_list = del_data_list.tolist()

                # Entity_Noの振り直し
                dataRenumbering()

                # ウィンドウ更新
                window['-Entity Table-'].update(values=entityMaster_list)

        else:
            mess = sg.popup_ok('仮削除するEntityを選択してください。',title = 'Warning Entity Del')

    # エンティティデータ　Create　SQLファイル出力
    if event == '-CreateSql File-':
        print('--------CreateSql File')
        createSqlFilePath = configManager.getCreateSqlFilePath()

        # OutputFolder存在チェック
        if not os.path.isdir(createSqlFilePath):
            os.mkdir(createSqlFilePath)

        # 反映済み、未済のデータのリストアップ
        entity_selects = {}
        entity_names=''
        no_entity_names=''
        for index,data in enumerate(entityMaster_list):
            if data[0] == '☑' and data[7] == '済':
                entity_selects.update({data[12]:data[4]})
                entity_names += '{}\n'.format(data[4])
            elif data[0] == '☑' and data[7] == '未済':
                no_entity_names += '{}\n'.format(data[4])

        # 未反映データメッセージ
        if no_entity_names:
            mess = sg.popup_ok('以下、未反映のEntityは出力されません。\n\n{}'.format(no_entity_names),
                                                                                title = 'Warning Sql Output')
        # 反映済みデータのみ出力
        if len(entity_selects) > 0:
            mess = sg.popup_ok_cancel('{}のCreate文を以下に出力します。\n{}'.format(entity_names,
                                                                                createSqlFilePath),
                                                                                title = 'Confirm Sql Output')
            if mess == "OK":

                # print('----createSqlFilePath[{}]'.format(createSqlFilePath))
                # print('----entity_selects[{}]'.format(entity_selects))

                # SqlFile一括出力（選択行）
                createTableSQLFileMake = CreateTableSQLFileMake(0)
                createTableSQLFileMake.createTableSelect(file_path=createSqlFilePath,
                                                        entity_selects=entity_selects)

                mess = sg.popup_ok('{}のCreate文を以下に出力しました。\n{}'.format(entity_names,
                                                                                createSqlFilePath),
                                                                                title = 'Complete Sql Output')
        else:
            mess = sg.popup_ok('出力するEntityを選択してください。',title = 'Warning Sql Output')

    # エンティティデータ　エンティティ定義書出力
    if event == '-CreateExcel File-':
        print('--------CreateExcel File')
        entityExcelOutputPath = configManager.getEntityExcelOutputPath()

        # OutputFolder存在チェック
        if not os.path.isdir(entityExcelOutputPath):
            os.mkdir(entityExcelOutputPath)

        # 反映済み、未済のデータのリストアップ
        entity_selects = {}
        entity_names=''
        no_entity_names=''
        for index,data in enumerate(entityMaster_list):
            if data[0] == '☑' and data[7] == '済':
                entity_selects.update({data[12]:data[4]})
                entity_names += '{}\n'.format(data[4])
            elif data[0] == '☑' and data[7] == '未済':
                no_entity_names += '{}\n'.format(data[4])

        # 未反映データメッセージ
        if no_entity_names:
            mess = sg.popup_ok('以下、未反映のEntityは出力されません。\n\n{}'.format(no_entity_names),
                                                                                title = 'Warning Sql Output')

        # 反映済みデータのみ出力
        if len(entity_selects) > 0:
            mess = sg.popup_ok_cancel('{}のエンティティ定義書を以下に出力します。\n{}'.format(entity_names,
                                                                                entityExcelOutputPath),
                                                                                title = 'Confirm Excel Entity')
            if mess == "OK":

                # エンティティ定義書書き込み処理（選択行一括）
                entityWrite = EntityExcelWrite(0)
                entityWrite.entitySelecttWrite(full_path=entityExcelOutputPath,
                                                entity_selects=entity_selects)

                mess = sg.popup_ok('{}のエンティティ定義書を以下に出力しました。\n{}'.format(entity_names,
                                                                                entityExcelOutputPath),
                                                                                title = 'Complete Excel Output')
        else:
            mess = sg.popup_ok('出力するEntityを選択してください。',title = 'Warning Excel Output')

    # Entity　Reflection
    if event == '-Entity Ref-' or values['menu1'] == 'Entity Reflection':
        print('--------Entity Reflection')

        # ラジオボタン Openおよびファイル作成選択の場合、反映処理スキップ
        if values['-radio Open-'] or values['-radio CreateFile-']:
            mess = sg.popup_ok('Open、ファイル作成選択の場合、反映処理は出来ません。', title = 'Warning...')
            continue

        # 削除対象ではない仮登録中のEntity Dataをリストアップ
        notarget_entity_nos = []
        for index,data in enumerate(entityMaster_list):
             notarget_entity_nos.append(int(data[12]))

        # print('--------notarget_entity_nos{}'.format(notarget_entity_nos))
        # Entity Master 削除対象検索
        target_entity_nos = entityMasterAccess.entityDelTargetSearch(notarget_entity_nos=notarget_entity_nos)

        # print('--------target_entity_nos{}'.format(target_entity_nos))
        # 削除対象　1件以上あった場合のみColumnマスターを削除実施
        if len(target_entity_nos) > 0:
            # Column Master 選択削除
            columnMasterAccess.columnDeleteEntityNo(entity_nos=target_entity_nos)

        # entity Master 一括削除
        entityMasterAccess.entityMasterAllDelete()

        # entity Master 仮登録中（未済）→全再登録
        entityMasterAccess.entityMasterInsert(entityMaster_list=entityMaster_list)

        # statusを反映済みに一括更新
        for index,data in enumerate(entityMaster_list):
            entityMaster_list[index][7] = '済'

        # ウィンドウ更新
        window['-Entity Table-'].update(entityMaster_list)

        mess = sg.popup_ok('{}件　反映処理を実施しました。'.format(len(entityMaster_list)),
                                                                title = 'Complete Reflection...')

    if values['menu1'] == "Folder Open" or event == '-Folder Open-':
        print('--------Folder Open')
        ragio_open = values['-radio Open-']

        if ragio_open:
            num = 0
            open_flg = False
            for index,data in enumerate(entityMaster_list):
                if data[0] == '☑':
                    num = index
                    open_flg = True

            if open_flg:

                # ファイルフルパスを取得
                file_full_path = entityMaster_list[num][6]
                # フルパスよりディレクトリパスを取得
                dir_path = fileOperation.getFolderPath(file_full_path)
                # フォルダOPEN確認
                mess = sg.popup_ok_cancel('フォルダ：{}を開きますか？'.format(dir_path),title = 'Confirm...')
                if mess == "OK":
                    print("---選択行:{}----".format(entityMaster_list[num][1]))
                    # フォルダOPEN処理
                    fileOperation.folderOpen(dir_path)

            # 行未選択の場合、選択メッセージを表示
            else:
                sg.popup_error('行を選択してください。',title = 'error')

        # 行未選択の場合、選択メッセージを表示
        else:
            sg.popup_error('Radio Openを選択してください。',title = 'error')


    # カラムTable選択イベント markのチェック更新処理を実施
    if event == '-Entity Table-':
        # Table　クリックイベントをハンドリング後、選択行を取得するために
        # ジェネレータを取得
        # 【注意！】ジェネレータは、IF文中に1回のみ実行可能
        #          ELSEで判定すると分岐連続では判定に使用できない
        gen = (i for i in values['-Entity Table-'])
        # ジェネレートをループし、選択行番号を取得
        for num in gen:

            # ラジオボタン　削除選択時
            if values['-radio Del-'] or values['-radio CreateFile-']:
                # Mark判定処理
                mark = entityMaster_list[num][0]
                if mark == '☐':
                    entityMaster_list[num][0] = '☑'
                if mark == '☑':
                    entityMaster_list[num][0] = '☐'

            # ラジオボタン　Open選択時
            elif  values['-radio Open-']:
                # Mark一括更新
                for i,datas in enumerate(entityMaster_list):
                    entityMaster_list[i][0] = '☐'

                # 選択行のみ、チェックありに更新
                entityMaster_list[num][0] = '☑'

            # ラジオボタン　追加選択時
            else:
                # Mark一括更新（チェック無効）
                for i,datas in enumerate(entityMaster_list):
                    entityMaster_list[i][0] = '☒'

            # ウィンドウ更新
            window['-Entity Table-'].update(entityMaster_list)

    #  ラジオボタンイベント
    if '-radio' in event:
        # ラジオボタン 追加選択時
        if event == '-radio Open-':

            # Entity items Add 表示
            window['-Entity Search Items-'].update(visible=True)

            # button制御
            window['-Entity Open-'].update(disabled=False, disabled_button_color=(None,None))
            window['-Entity Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateSql File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateExcel File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Folder Open-'].update(disabled=False, disabled_button_color=(None,None))

            window['-Entity Ref-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))


            # Mark一括更新
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☐'

            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # 全選択チェックボックス　チェックなし・無効・非表示
            window['-All Mark Select-'].update(False, disabled=True, visible=False)

            # Entity items Add 非表示
            window['-Entity Add Items-'].update(visible=False)
            clearEntityAddItems()

        # ラジオボタン 追加選択時
        elif event == '-radio Add-':

            # Entity masterデータを全件取得する
            entityMaster_list = entityMasterAccess.entityMasterSearchAll()
            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # Entity items Add 表示
            window['-Entity Search Items-'].update(visible=False)

            # button制御
            window['-Entity Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Add-'].update(disabled=False, disabled_button_color=(None,None))
            window['-Entity Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateSql File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateExcel File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Folder Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

            window['-Entity Ref-'].update(disabled=False, disabled_button_color=(None,None))

            # Mark一括更新
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☒'

            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # 全選択チェックボックス　チェックなし・無効・非表示
            window['-All Mark Select-'].update(False, disabled=True, visible=False)

            # Entity items Add 表示
            window['-Entity Add Items-'].update(visible=True)
            clearEntityAddItems()


        # ラジオボタン 削除選択時
        elif event == '-radio Del-':

            # Entity masterデータを全件取得する
            entityMaster_list = entityMasterAccess.entityMasterSearchAll()
            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # Entity items Add 表示
            window['-Entity Search Items-'].update(visible=False)

            # button制御
            window['-Entity Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Del-'].update(disabled=False, disabled_button_color=(None,None))
            window['-CreateSql File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateExcel File-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Folder Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

            window['-Entity Ref-'].update(disabled=False, disabled_button_color=(None,None))

            # Mark一括更新
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☐'

            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # 全選択チェックボックス　チェックなし・有効・表示
            window['-All Mark Select-'].update(False, disabled=False, visible=True)

            # Entity items Add 非表示
            window['-Entity Add Items-'].update(visible=False)
            clearEntityAddItems()

        # ラジオボタン 選択時
        else:

            # Entity items Add 表示
            window['-Entity Search Items-'].update(visible=True)

            # button制御
            window['-Entity Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Add-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-Entity Del-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))
            window['-CreateSql File-'].update(disabled=False, disabled_button_color=(None,None))
            window['-CreateExcel File-'].update(disabled=False, disabled_button_color=(None,None))
            window['-Folder Open-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

            window['-Entity Ref-'].update(disabled=True, disabled_button_color=('#d3d3d3','#d3d3d3'))

            # Mark一括更新
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☐'

            # ウィンドウ更新
            window['-Entity Table-'].update(values=entityMaster_list)

            # 全選択チェックボックス　チェックなし・有効・表示
            window['-All Mark Select-'].update(False, disabled=False, visible=True)

            # Entity items Add 非表示
            window['-Entity Add Items-'].update(visible=False)
            clearEntityAddItems()

    # チェックボックス　一覧チェックボックス全選択・解除イベント
    if event == '-All Mark Select-':
        selection_flg = values['-All Mark Select-']
        print('--------All Mark Select:{}'.format(selection_flg))
        # チェックありの場合
        if selection_flg:
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☑'
        # チェックなしの場合
        else:
            for i,datas in enumerate(entityMaster_list):
                entityMaster_list[i][0] = '☐'

        # ウィンドウ更新
        window['-Entity Table-'].update(values=entityMaster_list)

window.close()
