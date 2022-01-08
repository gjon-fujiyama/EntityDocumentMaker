from datetime import datetime

from db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./EDS.sqlite3"

class EntityMaster(Base):
    """
    エンティティマスタ:ENTITY_MASTER

    物理エンティティコード:entity_cd
    論理エンティティ名:entity_name
    エンティティNo:entity_no
    説明:explanation
    エンティティ区分:entity_section
    削除フラグ:del_flg
    エンティティ定義書パス:entity_document_path
    タイプ:type_section
    タイプ名:type_section_name
    登録日時:register_date
    登録者:register_cd
    更新日時:update_date
    更新者:update_cd
    """
    __tablename__ = 'ENTITY_MASTER'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    entity_cd = Column(
        'entity_cd',
        String(20),
        # primary_key=True
    )
    entity_name = Column('entity_name', String(40))
    entity_no = Column('entity_no', INTEGER(4))
    explanation = Column('explanation', String(256))
    entity_section = Column('entity_section', String(2))
    del_flg = Column(
        'del_flg',
        INTEGER(1),
        nullable=False,)
    entity_document_path = Column('entity_document_path', String(256))
    type_section = Column('type_section', String(2))
    type_section_name = Column('type_section_name', String(256))
    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                entity_cd: str,
                entity_name: str,
                entity_no: int,
                explanation: str,
                entity_section: str,
                del_flg: int,
                entity_document_path: str,
                type_section: str,
                type_section_name: str,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.entity_cd = entity_cd
        self.entity_name = entity_name
        self.entity_no = entity_no
        self.explanation = explanation
        self.entity_section = entity_section
        self.del_flg = del_flg
        self.entity_document_path = entity_document_path
        self.type_section = type_section
        self.type_section_name = type_section_name
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd

    def __str__(self):
        return ' entity_cd -> ' + self.entity_cd + \
               ', entity_name -> ' + self.entity_name + \
               ', entity_no -> ' + str(self.entity_no) + \
               ', explanation -> ' + self.explanation + \
               ', entity_section -> ' + self.entity_section + \
               ', del_flg -> ' + str(self.del_flg) + \
               ', entity_document_path -> ' + self.entity_document_path + \
               ', type_section -> ' + self.type_section + \
               ', type_section_name -> ' + self.type_section_name + \
               ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', register_cd -> ' + self.register_cd + \
               ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', update_cd -> ' + self.update_cd

class ColumnMaster(Base):
    """
    カラムマスタ:COLUMN_MASTER

    物理エンティティコード:entity_cd
    物理カラムコード:column_cd
    論理カラム名:column_name
    参照元物理エンティティコード:ref_entity_cd
    参照元論理エンティティ名:ref_entity_name
    カラムNo:column_no
    型:modl
    桁:digit
    精度:accuracy
    NOT NULL フラグ:not_null_flg
    主キーフラグ:primary_key_flg
    説明:explanation
    DB制約:db_constraint
    特記事項:remarks
    削除フラグ:del_flg
    エンティティNo:entity_no
    登録日時:register_date
    登録者:register_cd
    更新日時:update_date
    更新者:update_cd
    """
    __tablename__ = 'COLUMN_MASTER'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    entity_cd = Column(
        'entity_cd',
        String(10),
        # primary_key=True,
    )
    column_cd = Column(
        'column_cd',
        String(20),
        # primary_key=True,
    )
    column_name = Column('column_name', String(40))
    ref_entity_cd = Column('ref_entity_cd', String(20))
    ref_entity_name = Column('ref_entity_name', String(40))
    column_no = Column('column_no', INTEGER(4))

    modl = Column('modl', String(20))
    digit = Column('digit', String(4))
    accuracy = Column('accuracy', String(2))
    not_null_flg = Column('not_null_flg', INTEGER(1))
    primary_key_flg = Column('primary_key_flg', INTEGER(1))

    explanation = Column('explanation', String(256))
    db_constraint = Column('db_constraint', String(256))
    remarks = Column('remarks', String(256))
    del_flg = Column('del_flg', INTEGER(1))

    entity_no = Column('entity_no', INTEGER(4))

    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                entity_cd: str,
                column_cd: str,
                column_name: str,
                ref_entity_cd: str,
                ref_entity_name: str,
                column_no: int,
                modl:str,
                digit: str,
                accuracy: str,
                not_null_flg: int,
                primary_key_flg: int,
                explanation: str,
                db_constraint: str,
                remarks: str,
                del_flg: int,
                entity_no: int,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.entity_cd = entity_cd
        self.column_cd = column_cd
        self.column_name = column_name
        self.ref_entity_cd = ref_entity_cd
        self.ref_entity_name = ref_entity_name
        self.column_no = column_no
        self.modl = modl
        self.digit = digit
        self.accuracy = accuracy
        self.not_null_flg = not_null_flg
        self.primary_key_flg = primary_key_flg
        self.explanation = explanation
        self.db_constraint = db_constraint
        self.remarks = remarks
        self.del_flg = del_flg
        self.entity_no = entity_no
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd
        # print(self.explanation)

    def __str__(self):
        return ': entity_cd -> ' + self.entity_cd + \
                ': column_cd -> ' + self.column_cd + \
                ', column_name -> ' + self.column_name + \
                ', ref_entity_cd -> ' + self.ref_entity_cd + \
                ', ref_entity_name -> ' + self.ref_entity_name + \
                ', column_no -> ' + str(self.column_no) + \
                ', modl -> ' + self.modl + \
                ', digit -> ' + str(self.digit) + \
                ', accuracy -> ' + str(self.accuracy) + \
                ', not_null_flg -> ' + str(self.not_null_flg) + \
                ', primary_key_flg -> ' + str(self.primary_key_flg) + \
                ', explanation -> ' + self.explanation + \
                ', db_constraint -> ' + self.db_constraint + \
                ', remarks -> ' + self.remarks + \
                ', del_flg -> ' + str(self.del_flg) + \
                ', entity_no -> ' + str(self.entity_no) + \
                ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
                ', register_cd -> ' + self.register_cd + \
                ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
                ', update_cd -> ' + self.update_cd

class SettingMaster(Base):
    """
    設定マスタ:SETTING_MASTER

    id:id
    タイプ:type_section
    タイプ名:type_section_name
    タイプ:doc_type_section
    タイプ名:doc_type_section_name
    取込先パス設定:set_import_path
    登録日時:register_date
    登録者:register_cd
    更新日時:update_date
    更新者:update_cd
    """
    __tablename__ = 'SETTING_MASTER'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    type_section = Column('type_section', String(2))
    type_section_name = Column('type_section_name', String(256))
    doc_type_section = Column('doc_type_section', String(2))
    doc_type_section_name = Column('doc_type_section_name', String(256))
    set_import_path = Column('set_import_path', String(256))
    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                type_section: str,
                type_section_name: str,
                doc_type_section: str,
                doc_type_section_name: str,
                set_import_path: str,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.type_section = type_section
        self.type_section_name = type_section_name
        self.doc_type_section = doc_type_section
        self.doc_type_section_name = doc_type_section_name
        self.set_import_path = set_import_path
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd

    def __str__(self):
        return ' id -> ' + str(self.id) + \
               ', type_section -> ' + self.type_section + \
               ', type_section_name -> ' + self.type_section_name + \
               ', doc_type_section_name -> ' + self.doc_type_section_name + \
               ', doc_type_section_name -> ' + self.doc_type_section_name + \
               ', set_import_path -> ' + self.set_import_path + \
               ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', register_cd -> ' + self.register_cd + \
               ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', update_cd -> ' + self.update_cd

class FilePathTran(Base):
    """
    ファイルパス:FILE_PATH_TRAN

    id:id
    タイプ:type_section
    タイプ名:type_section_name
    タイプ:doc_type_section
    タイプ名:doc_type_section_name
    ファイル名：file_name
    フルファイルパス:fll_file_path
    フォルダパス:folder_path
    登録日時:register_date
    登録者:register_cd
    更新日時:update_date
    更新者:update_cd
    """
    __tablename__ = 'FILE_PATH_TRAN'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    type_section = Column('type_section', String(2))
    type_section_name = Column('type_section_name', String(256))
    doc_type_section = Column('doc_type_section', String(2))
    doc_type_section_name = Column('doc_type_section_name', String(256))
    file_name = Column('file_name', String(256))
    fll_file_path = Column('fll_file_path', String(256))
    folder_path = Column('folder_path', String(256))
    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                type_section: str,
                type_section_name: str,
                doc_type_section: str,
                doc_type_section_name: str,
                file_name: str,
                fll_file_path: str,
                folder_path: str,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.type_section = type_section
        self.type_section_name = type_section_name
        self.doc_type_section = type_section
        self.doc_type_section_name = type_section_name
        self.file_name = file_name
        self.fll_file_path = fll_file_path
        self.folder_path = folder_path
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd

    def __str__(self):
        return ' id -> ' + str(self.id) + \
               ', type_section -> ' + self.type_section + \
               ', type_section_name -> ' + self.type_section_name + \
               ', doc_type_section -> ' + self.doc_type_section + \
               ', doc_type_section_name -> ' + self.doc_type_section_name + \
               ', file_name -> ' + self.file_name + \
               ', fll_file_path -> ' + self.fll_file_path + \
               ', folder_path -> ' + self.folder_path + \
               ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', register_cd -> ' + self.register_cd + \
               ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', update_cd -> ' + self.update_cd
