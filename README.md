# EntityDocumentMaker Version 1.00
After importing the entity definition (Excel file), store the data in sqlite3.  

エンティティ定義（Excelファイル）をインポートした後、データをsqlite3に保存します。  

# DEMO

![demo_EntityDocumentMake__](https://user-images.githubusercontent.com/95132992/148678091-35d72a0a-4c7f-4139-8c0c-e372fdf5392a.gif)  

# Features

1)データベース エンティティ定義書(Excelファイル)を読み込み、SQLite3に登録できます。  
2)登録データをTabelとColumnで管理（検索、登録、削除、更新）が出来ます。  
3)登録データを元にエンティティ定義書とCreate Table文を作成します。  
4)Python環境を構築せずに実行する事が出来ます。  
　・EntityDocumentMaker.exeをクリックしてください！

# Requirement

* python 3.10.0  
* numpy 1.21.5  
* openpyxl 3.0.9  
* SQLAlchemy 1.4.26  
* pyinstaller 4.7  
* PySimpleGUI 4.55.1  

# Usage

１）リソース起動の場合は、以下を行ってください。  

　1)任意の場所にEntityDocumentMakerフォルダを配置します。  
　  
　2)以下、コマンドを実行して下さい。  
```bash
cd [任意の場所]/EntityDocumentMaker
python .\EntityDocumentMaker.py
```
　  
２）Python環境を構築せずに実行する場合  
　  
　1)下記のファイルとフォルダをEntityDocumentMaker.exeと同階層に配置してください。  
　　・FjiYama.ico  
　　・config.ini  
　　・EntityTemplateExcelフォルダ  
　  
　2)[任意の場所]\EntityDocumentMaker.exeをクリックしてください。  
　  
　■exeファイル作成は、以下コマンド実行  
```bash
cd [任意の場所]/EntityDocumentMaker
pyinstaller --onefile --icon=FjiYama.ico .\EntityDocumentMaker.py --noconsole
```
　  
# Note
　  
※exeファイル作成の場合の注意点  
・EntityDocumentMaker.pyと同階層に以下を配置してください。  
　・FjiYama.ico  
　・config.ini  
　・EntityTemplateExcelフォルダ  
　　（同フォルダには、エンティティ定義書出力に必要なテンプレートファイルがあります）  
　  
・以下のフォルダは、デモ用のエンティティ定義書のサンプルです。  
　・(〇〇)エンティティ定義書フォルダ配下のエンティティ定義書(.xlsxファイル)  
　・(標準)エンティティ定義書フォルダ配下のエンティティ定義書(.xlsxファイル)  
　  
・取込するエンティティ定義書は、上記のサンプル形式で読み込みます。  
　・「エンティティ定義書_」の接頭辞が付与された.xlsxファイル  
　・上記、サンプルのエンティティ定義書の形式内容でテーブル名、カラム名を取込みます。  
　・Sttingタブにて指定フォルダ内の上記、対象ファイルのみ取込みます  
　  
# Author

* 作成者 Fuji
* 所属 X
* E-mail None

# License

"EntityDocumentMaker" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).  

## ////改修履歴/////////  
2022/01/03 Version 1.00  
・新規登録  
2022/01/08  
・FolderOpnen機能追加  
2033/01/09  
・DEMO動画 COMMIT    
・取込条件で取込対象拡張子,ファイル接頭辞を追加修正    
・EntityDocumentMaker.exeを配置  
・EntityDocumentMaker\EntityDocumentMaker.specを配置  
