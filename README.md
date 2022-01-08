# EntityDocumentMaker Version 1.00
After importing the entity definition (Excel file), store the data in sqlite3.  

エンティティ定義（Excelファイル）をインポートした後、データをsqlite3に保存します。  

# DEMO

## 準備中

# Features

1)データベース エンティティ定義書(Excelファイル)を読み込み、SQLite3に登録できます。  
2)登録データをTabelとColumnで管理（検索、登録、削除、更新）が出来ます。  
3)登録データを元にエンティティ定義書とCreate Table文を作成します。  

# Requirement

* huga 3.5.2  
* numpy 1.21.5  
* openpyxl 3.0.9  
* SQLAlchemy 1.4.26  
* pyinstaller 4.7  
* PySimpleGUI 4.55.1  

# Usage

※リソース起動の場合は、以下を行ってください。  

1)任意の場所にEntityDocumentMakerフォルダを配置します。  

2)以下、コマンドを実行して下さい。  
```bash
cd [任意の場所]/EntityDocumentMaker
python .\EntityDocumentMaker.py
```

# Note

※注意点  
・EntityDocumentMaker.pyと同階層に以下、設定ファイルとエンティティ定義書テンプレートフォルダは配置してください。  
　・config.ini  
　・EntityTemplateExcel  

・以下のフォルダは、デモ用のエンティティ定義書のサンプルです。  
　・(〇〇)エンティティ定義書フォルダ配下のエンティティ定義書  
　・(標準)エンティティ定義書フォルダ配下のエンティティ定義書  

# Author

* 作成者 G-jon Fujiyama
* 所属 Script Edit.
* E-mail None

# License

"hoge" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## ////改修履歴/////////  
2022/01/03 Version 1.00  
・新規登録  
