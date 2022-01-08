#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs
import os
import glob
import db

import datetime
from sqlalchemy import distinct
from sqlalchemy import and_, or_, not_

from models import *

# ColumnMaster アクセスクラス
class ColumnMasterAccess():

    # 全件取得処理
    def columnMasterSearch(self, entity_cd, entity_no):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 設定マスタを全取得
        columnMaster = db.session.query(ColumnMaster).filter(ColumnMaster.entity_no == entity_no, ColumnMaster.entity_cd == entity_cd).order_by(ColumnMaster.id).all()
        #　データベース.セッションをクローズ
        db.session.close()

        return columnMaster;

    # 登録処理
    def columnMasterInsert(self, data_list, entity_cd, entity_no):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # ColumnMaster Delete
        db.session.query(ColumnMaster).filter(ColumnMaster.entity_no == entity_no, ColumnMaster.entity_cd == entity_cd).delete()
        db.session.commit()  # データベースコミット

        # 現在日時取得
        # now = datetime.datetime.now()
        now = datetime.now()

        # 設定データループ
        for datas in data_list:
            column_no_add = datas[1]
            column_cd_add = datas[2]
            column_name_add = datas[3]
            model_add = datas[4]
            digit_add = datas[5]
            acc_add = datas[6]
            not_null_add = datas[7]
            pk_add = datas[8]
            explanation_add = datas[9]
            dbCons_add = datas[10]
            remarks_add = datas[11]
            del_flg_add = datas[12]

            not_null = 0
            if not_null_add == '〇':
                not_null = 1

            pk = 0
            if pk_add == '〇':
                pk = 1

            del_flg = 0
            if del_flg_add == '削除':
                del_flg = 1

            columnMaster = ColumnMaster(entity_cd=entity_cd,
                                        column_cd=column_cd_add,
                                        column_name=column_name_add,
                                        ref_entity_cd='',
                                        ref_entity_name='',
                                        column_no=column_no_add,
                                        modl=model_add,
                                        digit=digit_add,
                                        accuracy=acc_add,
                                        not_null_flg=not_null,
                                        primary_key_flg=pk,
                                        explanation=explanation_add,
                                        db_constraint=dbCons_add,
                                        remarks=remarks_add,
                                        del_flg=del_flg,
                                        entity_no=entity_no,
                                        register_date=now,
                                        register_cd='ColumnMasterAccess',
                                        update_date=now,
                                        update_cd='ColumnMasterAccess')

            # ColumnMasterデータ登録
            db.session.add(columnMaster)  # 追加
            db.session.commit()  # データベースコミット

        #　データベース.セッションをクローズ
        db.session.close()

    # 選択一括削除処理
    def columnDeleteEntityNo(self, entity_nos):

        # Delete　SQL構築
        L=[]
        # L.append("SELECT DISTINCT(entity_no) FROM COLUMN_MASTER ")
        L.append("DELETE FROM COLUMN_MASTER ")
        if len(entity_nos) > 0:
            L.append("WHERE 1<>1 ")
            pass

        for entity_no in entity_nos:
            L.append(" OR entity_no = {} ".format(entity_no))


        sql = ''.join(L)

        print(sql)

        db.session.execute(sql)
        db.session.commit()  # データベースコミット

# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    entity_nos=[1, 4, 7]
    # ファイルパス読み取り処理
    cma = ColumnMasterAccess()
    # clms = cma.entityMasterSearchAll()
    clms = cma.columnDeleteEntityNo(entity_nos=entity_nos)

    # print(list(clms))
    # print(type(clms))
    # print(list(clms))
