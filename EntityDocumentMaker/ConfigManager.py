# coding: utf-8
import configparser
import json
from distutils.util import strtobool

# ファイルの存在チェック用モジュール
import os
import errno

class ConfigManager():

    # インスタンス化メソッド
    # 　を設定しない
    def __init__(self):
        # iniファイルの読み込み
        self.config_ini = configparser.ConfigParser()
        self.config_ini_path = 'config.ini'

        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(self.config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)

        # 設定ファイル読み込み
        self.config_ini.read(self.config_ini_path, encoding='utf-8')

        # タイプ配列初期設定
        self.typeSections = self.getSectionDicts('TYPE')
        self.docTypeSections = self.getSectionDicts('DOC_TYPE')
        self.tableTypeSections = self.getSectionDicts('TEABLE_TYPES')

        # system Path
        self.systemPath = dict(self.config_ini.items('SYSTEM_PATHS'))

        # Application version
        self.appVersion = dict(self.config_ini.items('VER'))

    # Application version
    def getAppVersion(self):
        return self.appVersion.get('version')

    # 値配列取得
    def getSectionValus(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        result_list = []
        for v in sectionItems.values():
            v_list = v.split(',')
            result_list.append(v_list[0])
        return result_list;

    # デフォルト値取得
    def getSectionDefaultValu(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        for v in sectionItems.values():
            v_list = v.split(',')
            if strtobool(v_list[2]):
                return v_list[0]

        return '';

    # 区分辞書作成
    def getSectionDicts(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        result_dict = {}
        for v in sectionItems.values():
            v_list = v.split(',')
            result_dict.setdefault(v_list[0], v_list[1])
        return result_dict;

    # タイプ値取得
    def getTypeSectionValue(self, key):
        return self.typeSections.get(key)

    # Tableタイプ Value値取得
    def getTypeSectionKey(self, Value):
        key = [k for k, v in self.typeSections.items() if v == Value][0]
        return key


    # DOCタイプ値取得
    def getDocTypeSectionValue(self, key):
        return self.docTypeSections.get(key)

    # Tableタイプ Value値取得
    def getTableTypeSectionValue(self, key):
        return self.tableTypeSections.get(key)

    # Tableタイプ Value値取得
    def getTableTypeSectionKey(self, Value):
        key = [k for k, v in self.tableTypeSections.items() if v == Value][0]
        return key

    # エンティティ定義書パス取得
    def getEntityDocTemplatePath(self):
        return self.systemPath.get('entity_doc_template_path')

    # エンティティ定義書設定シート名
    def getEntitySheetName(self):
        return self.systemPath.get('enttity_sheet_name')

    # エンティティ定義書変更履歴シート名
    def getRevisionHistorySheetName(self):
        return self.systemPath.get('revision_history_sheet_name')

    # CreateSQLファイル出力先フォルダパス取得
    def getCreateSqlFilePath(self):
        return self.systemPath.get('create_sql_file_path')

    # エンティティ定義書ファイル出力先フォルダパス取得
    def getEntityExcelOutputPath(self):
        return self.systemPath.get('entity_excel_output_path')
