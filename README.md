# fukuda-alarm-analysis
## About
フクダ電子製セントラルモニタ DS8900, DS8700 からエクスポートしたアラーム履歴ファイルを解析するPythonスクリプトです．

## 目的
アラーム履歴を分析することで不要なアラームを削減するためのインサイトを得て， 次のアクションを決定するために使用します．

## 使い方
### アラームログデータのエクスポート
セントラルモニタから「設定ファイル」と呼ばれるデータ(この中にログファイル群が格納されています)をCFカード等にエクスポートします．
なお， サンプルデータもリポジトリ内においているので，実機からデータをエクスポートせずとも，解析処理の動作は確認してもらえます．

### リポジトリのクローン または ダウンロード
本リポジトリをcloneするか， 「Code」ボタンをクリックして表示されるメニューからzipアーカイブをダウンロードします．

### 実行
スクリプトはJupyterLab形式になっていますので， JupyterLab or JupyterNotebookから実行します．

## ファイルの説明
### [01.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/01.ipynb)
アラームログを読み込んで先頭数行を表示します．

### [02.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/02.ipynb)
アラーム別・CH別のアラーム件数をヒートマップで表示します．

### [03.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/03.ipynb)
CH別の各アラームの継続時間の代表値（平均値・中央値）を表示します．

### [04.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/04.ipynb)
1時間毎のCH別のバイタルアラーム数を積み上げ棒グラフで表示します．

### [05.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/05.ipynb)
CHとアラームを指定して，計測値とアラーム閾値との差のヒストグラムを表示します．
特定の閾値を指定して，　その閾値でアラームが鳴った時の計測値のヒストグラムを表示します．

### [06.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/06.ipynb)
アラームの継続時間の情報を利用して，　全記録時間に占めるアラーム鳴動時間の割合を算出します．

### [07.ipynb](https://github.com/cepop/fukuda-alarm-analysis/blob/main/07.ipynb)
CH毎にアラームの計測時間のヒストグラムを表示します． 

### [FukudaCsv.py](https://github.com/cepop/fukuda-alarm-analysis/blob/main/FukudaCsv.py)
CSVの読み込み処理, 前処理などの共通する処理をモジュール化しています．　

## システム要件
| Package                       | Version      |
| ----------------------------  | ------------ |
| python                        | 3.8.12 |
| jupyterlab                    | 3.2.8 |
| matplotlib                    | 3.5.0 |
| numpy                         | 1.22.3 |
| pandas                        | 1.3.4 |
| seaborn                       | 0.11.2 |
