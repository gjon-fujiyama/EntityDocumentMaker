# -*- coding: utf-8 -*-
import os
import db

from sqlalchemy import and_, or_, not_

from models import EntityMaster, ColumnMaster
from SettingEntityAccess import SettingEntityAccess

from ConfigManager import ConfigManager

from models import *

# エンティティ定義書書き込みクラス
class CreateTableSQLFileMake(): #クラス名

    # インスタンス化メソッド
    def __init__(self, del_flg_skp):
        self.del_flg_skp = del_flg_skp

    # Entity選択メソッド
    def createTableSelect(self, file_path, entity_selects):

        # 辞書ループ
        for key,value in entity_selects.items():

            entity_no = key
            entity_cd = value

            # 設定マスタを全取得
            entityMasters = db.session.query(EntityMaster).\
                                filter(and_(EntityMaster.entity_no == entity_no, EntityMaster.entity_cd == entity_cd)).\
                                order_by(EntityMaster.id).all()

            #　データベース.セッションをクローズ
            # db.session.close()

            for entityMaster in entityMasters:
                self.createTableSql(file_path=file_path,
                                entity_no=entityMaster.entity_no,
                                entity_cd=entityMaster.entity_cd,
                                entity_name=entityMaster.entity_name,
                                type_section_name=entityMaster.type_section_name)

    def createTableSql(self, file_path, entity_no, entity_cd, entity_name, type_section_name):

        full_file_path = r'{}\No{}_({})_{}{}'.format(file_path, f'{entity_no:03}', type_section_name, entity_cd, '.sql')

        # 設定マスタを全取得
        columnMasters = db.session.query(ColumnMaster).\
                            filter(and_(ColumnMaster.entity_no == entity_no, ColumnMaster.entity_cd == entity_cd)).\
                            order_by(ColumnMaster.id).all()

        if os.path.isfile(full_file_path):
            # 既存ファイル削除
            os.remove(full_file_path)

        indent = '             '
        sql = 'CREATE TABLE {} (\n'.format(entity_cd)

        # Columnマスタのループ
        primary_key_list = []
        for index,columnMaster in enumerate(columnMasters):
            # 削除フラグスキップ＞０かつ削除フラグ＞０の場合、スキップ
            if self.del_flg_skp > 0 and columnMaster.del_flg > 0:
                continue;

            not_null = ''
            if columnMaster.not_null_flg > 0:
                not_null = ' NOT NULL'

            if columnMaster.primary_key_flg > 0:
                primary_key_list.append(columnMaster.column_cd)

            digit = ''
            if columnMaster.modl in ('NUMBER'):
                digit = '({},{})'.format(columnMaster.digit, columnMaster.accuracy)

            if columnMaster.modl in ('VARCHAR2', 'VARCHAR3','CHAR'):
                digit = '({})'.format(columnMaster.digit)

            sql += '{}{} {}{}{},\n'.format(indent,
                                        columnMaster.column_cd,
                                        columnMaster.modl,
                                        digit,
                                        not_null)

        if len(primary_key_list) > 0:
            sql += '{}PRIMARY KEY ({})\n{})\n/\n'.format(indent, ",".join(primary_key_list),indent)

        # コメントループ
        for index,columnMaster in enumerate(columnMasters):
            # 削除フラグスキップ＞０かつ削除フラグ＞０の場合、スキップ
            if self.del_flg_skp > 0 and columnMaster.del_flg > 0:
                continue;

            sql += '{}COMMENT ON COLUMN {}.{} IS \'{}\'\n/\n'.format(indent,
                                                                    entity_cd,
                                                                    columnMaster.column_cd,
                                                                    columnMaster.column_name)

        # ファイル出力
        if not os.path.isfile(full_file_path):
            with open(full_file_path, mode='w') as f:
                f.write(sql)

# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    file_path = r'C:\Entity_Document_Search\sqloutput'

    entity_no = 7
    entity_cd = 'SUPPLIERS_MASTER'

    entity_selects = { entity_no : entity_cd }

    entity_no = 6
    entity_cd = 'USER_MASTER'

    entity_selects.update({entity_no:entity_cd})

    # エンティティ定義書書き込み処理
    createTableSQLFileMake = CreateTableSQLFileMake(0)
    createTableSQLFileMake.createTableSelect(file_path=file_path, entity_selects=entity_selects)
