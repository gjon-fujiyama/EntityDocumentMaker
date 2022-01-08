#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs
import os
import glob
import db
from ConfigManager import ConfigManager

import datetime
from sqlalchemy import distinct
from sqlalchemy import and_, or_, not_

from models import *

# エンティティマスター アクセスクラス
class EntityMasterAccess():

    def __init__(self):
        # ConfigManagerクラスをインスタンス化
        self.configManager = ConfigManager()

    # 全件取得処理
    # →　ENTITYデータ表示リストを返却
    def entityMasterSearchAll(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 設定マスタを全取得
        entityMasters = db.session.query(EntityMaster).order_by(EntityMaster.id).all()
        #　データベース.セッションをクローズ
        db.session.close()

        result_list = []
        row_count = 1
        for entityMaster in entityMasters:
            """
            エンティティマスタ:ENTITY_MASTER

            エンティティNo:entity_no
            エンティティ属性名:entity_section_name
            物理エンティティCD:entity_cd
            論理エンティティ名:entity_name
            タイプ名:type_section_name
            エンティティ定義書パス:entity_document_path
            削除区分:del_type
            エンティティ属性:entity_section
            削除フラグ:del_flg
            """
            # table区分をコンフィグクラスより取得
            # print('------------entityMaster.entity_section[{}]'.format(entityMaster.entity_section))
            table_section_name = self.configManager.getTableTypeSectionKey(entityMaster.entity_section)

            if entityMaster.del_flg == '1':
                del_type = '削除'
            else:
                del_type = ''

            result = [
                    '☐'
                    ,row_count
                    ,entityMaster.type_section_name
                    ,table_section_name
                    ,entityMaster.entity_cd
                    ,entityMaster.entity_name
                    ,entityMaster.entity_document_path
                    ,'済'
                    ,del_type
                    ,entityMaster.type_section
                    ,entityMaster.del_flg
                    ,entityMaster.id
                    ,entityMaster.entity_no
                    ,self.configManager.getTableTypeSectionValue(table_section_name)
                    ,entityMaster.explanation]
            row_count += 1
            result_list.append(result)

        return result_list;getTypeSectionKey

    # 削除対象Entity_no検索処理
    # 引数のEntity_noリスト以外を検索取得し、仮削除データをリストアップ
    def entityDelTargetSearch(self, notarget_entity_nos):

        # SELECT Sql構築
        L=[]
        L.append("SELECT entity_no FROM ENTITY_MASTER ")
        if len(notarget_entity_nos) > 0:
            L.append("WHERE 1 = 1 ")

        for entity_no in notarget_entity_nos:
            L.append("AND entity_no <> {} ".format(entity_no))

        sql = ''.join(L)

        results = []
        for r in db.session.execute(sql):
            results.append(r[0])
        # print(results)
        return results;

    # Entity_no現時点最大値処理
    def getEntityNoMax(self):

        results = []
        for r in db.session.execute("SELECT Max(entity_no) FROM ENTITY_MASTER "):
            results.append(r[0])
        print(results)
        return results[0];

    # Entityデータ一括新規登録処理
    def entityMasterInsert(self, entityMaster_list):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 現在日時取得
        now = datetime.now()

        for entityMaster in entityMaster_list:

            print(entityMaster)

            entity_cd=entityMaster[4] #Entity Cd
            entity_name=entityMaster[5] #Entity Name
            entityNo=entityMaster[12] #Entity No
            explanation=entityMaster[14] #Explanation
            entity_section=entityMaster[13] #Table Section
            full_path=entityMaster[6] #Full Doc Path
            type_section=entityMaster[9] #Type Section
            type_section_name=entityMaster[2] #Type
            del_flg=0

            # エンティティマスタ設定
            entityMaster = EntityMaster(entity_cd=entity_cd,
                                        entity_name=entity_name,
                                        entity_no=entityNo,
                                        explanation=explanation,
                                        entity_section=entity_section,
                                        del_flg=del_flg,
                                        entity_document_path=full_path,
                                        type_section=type_section,
                                        type_section_name=type_section_name,
                                        register_date=now,
                                        register_cd="EntityMasterAccess",
                                        update_date=now,
                                        update_cd="EntityMasterAccess")

            # エンティティマスタ　データ登録
            db.session.add(entityMaster)  # 追加

        db.session.commit()  # データベースコミット

    # Entityデータ全削除処理
    def entityMasterAllDelete(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        db.session.query(EntityMaster).delete()  # 全削除

    # EntityMaster検索
    def entitySearch(self, type_in, section, entity_cd, entity_name, column_cd, column_name):

        # SELECT Sql構築
        text = "SELECT " + \
                "Distinct em.type_section_name, " +\
                "em.entity_section, " +\
                "em.entity_cd, " +\
                "em.entity_name, " +\
                "em.entity_document_path, " +\
                "'済', " +\
                "em.del_flg, " +\
                "em.type_section, " +\
                "em.del_flg, " +\
                "em.id, " +\
                "em.entity_no, " +\
                "em.entity_section, " +\
                "em.explanation " +\
                "FROM ENTITY_MASTER em "

        if column_cd or column_name:
            text += "INNER JOIN COLUMN_MASTER cm " +\
                    "ON em.entity_no = cm.entity_no "

        L=[]

        text += "WHERE 1=1 "

        if type_in:
            print(type_in)
            type_secion = self.configManager.getTypeSectionValue(type_in)
            text += "AND em.type_section = '{}' ".format(type_secion)

        if section:
            table_section = self.configManager.getTableTypeSectionValue(section)
            text += "AND em.entity_section = '{}' ".format(table_section)

        if entity_cd:
            text += "AND em.entity_cd Like '%{}%' ".format(entity_cd)

        if entity_name:
            text += "AND em.entity_name Like '%{}%' ".format(entity_name)

        if column_cd:
            text += "AND cm.column_cd Like '%{}%' ".format(column_cd)


        if column_name:
            text += "AND cm.column_name Like '%{}%' ".format(column_name)

        L.append(text)

        sql = ''.join(L)

        results = []
        row_no = 1
        for r in db.session.execute(sql):
            result=[]
            result.append('☐') # Mark
            result.append(row_no)# No
            result.append(r[0]) #Type
            result.append(self.configManager.getTableTypeSectionKey(r[1])) # Section
            result.append(r[2]) # Entity Cd
            result.append(r[3]) # Entity Name
            result.append(r[4]) # Full Doc Path
            result.append(r[5]) # Ref

            if r[6] == '1':
                del_type = '削除'
            else:
                del_type = ''

            result.append(del_type) # Del Type
            result.append(r[7]) # Type Section
            result.append(r[8]) # Del
            result.append(r[9]) # Id
            result.append(r[10]) # Entity No
            result.append(r[11]) # Section value
            result.append(r[12]) # Explanation

            results.append(result)
            row_no += 1

        return results;

# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    # ids = []
    # notarget_entity_nos = [2,3,5,6]

    # ファイルパス読み取り処理
    ema = EntityMasterAccess()
    # ems = ema.entityDelTargetSearch(notarget_entity_nos=notarget_entity_nos)

    #　～～～～debugコード～～～
    # # ems = ema.entityMasterSearchAll()
    # print(len(ems))
    # print(list(ems))
    # tyep = self.configManager.getTypeSectionKey('〇〇')
    # section = self.configManager.getTableTypeSectionKey('Table')
    # type = '〇〇'
    # section = 'Table'
    # entity_cd = 'USER_MASTER'
    # entity_name = 'ザ'
    # column_cd = 'test'
    # column_name = 'ユ'

    type = ''
    section = ''
    entity_cd = ''
    entity_name = ''
    column_cd = ''
    column_name = ''

    ems = ema.entitySearch(type_in=type,
                            section=section,
                            entity_cd=entity_cd,
                            entity_name=entity_name,
                            column_cd=column_cd,
                            column_name=column_name)

    print(ems)
