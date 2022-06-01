import math
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


# Pandasのオプション
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
plt.rcParams["font.size"] = 18
pd.options.display.float_format = '{:.1f}'.format   # 小数点第１位まで表示

CMAP = "tab20c"

# アラームコードとアラーム名称のdictionary
ALARM_CODE = {
    '0x000E': '呼吸数(IMP)上限',
    '0x000F' : '無呼吸上限',
    '0x0001' : '心拍数上限',
    '0x0800' : 'TACHY',
    '0x0801' : 'BRADY',
    '0x0804' : 'ＳＬＯＷ　ＶＴ',
    '0x0808' : 'RUN',
    '0x0809' : 'ＶＴ',
    '0x080A' : 'ＶＦ',
    '0x080B' : 'ASYSTOLE',
    '0x100E' : '呼吸数(IMP)下限',
    '0x1001' : '心拍数下限',
    '0x1010' : 'SpO2下限',
    '0x112E' : 'EXT_SpO2下限',
    '0x200C' : 'DS-LAN接続確認',
    '0x2000' : '電極確認',
    '0x2006' : 'SpO2センサ確認',
    '0x2038' : 'SpO2コネクタ抜け',
    '0x201E' : '心電低振幅',
    '0x2020' : '心電図１低振幅',
    '0x201F' : '心電図ノイズ混入',
    '0x2022' : '心電図１ノイズ混入',
    '0x6004' : 'モニタ中断開始',
    '0x6005' : 'モニタ中断解除',
    '0x6000' : '退床'
}
# 生体情報アラームのコード一覧（バイタルアラーム）
VITAL_ALARM_CODE = {
    '0x000E' : '呼吸数(IMP)上限',
    '0x000F' : '無呼吸上限',
    '0x0001' : '心拍数上限',
    '0x0800' : 'TACHY',
    '0x0801' : 'BRADY',
    '0x0804' : 'ＳＬＯＷ　ＶＴ',
    '0x0808' : 'RUN',
    '0x0809' : 'ＶＴ',
    '0x080A' : 'ＶＦ',
    '0x080B' : 'ASYSTOLE',
    '0x100E' : '呼吸数(IMP)下限',
    '0x1001' : '心拍数下限',
    '0x1010' : 'SpO2下限',
    '0x112E' : 'EXT_SpO2下限',
}
VITAL_LINK_ALARM_CODE = {
    '0x0809' : 'ＶＴ',
    '0x080A' : 'ＶＦ',
    '0x080B' : 'ASYSTOLE',
}
# 機器情報アラームのコード一覧
TECH_ALARM_CODE = {
    '0x200C' : 'DS-LAN接続確認',
    '0x2000' : '電極確認',
    '0x2006' : 'SpO2センサ確認',
    '0x2038' : 'SpO2コネクタ抜け',
    '0x201E' : '心電低振幅',
    '0x2020' : '心電図１低振幅',
    '0x201F' : '心電図ノイズ混入',
    '0x2022' : '心電図１ノイズ混入',
}

# アラーム種別を示す定数
ALARM_TYPE = {
    'VITAL' : VITAL_ALARM_CODE,
    'VITAL_LINK' : VITAL_LINK_ALARM_CODE,
    'TECH'  : TECH_ALARM_CODE,
    'ALL'   : ALARM_CODE
}


#######################
# CSVロード処理
#######################

# フクダ電子のDS8900のアラーム履歴出力ファイルをロードしマージして、PandasのDataFrameで返す
def load(dir_path_to_process):
    """ALMLOGディレクトリ内のCSVファイル(アラームログ)を読み込んで前処理した後に, Pandas.DataFrame オブジェクトを返す.
    :param dir_path_to_process: ALMLOGディレクトリまでのパス
    :type param1: string
    :returns: CSVを結合したDataFrameを返す
    :rtype: Pandas.DataFrame
    """

    # TODO: キャッシュ処理
    
    ########## CSVのロード ##########
    if len(dir_path_to_process):
        
        # アラームファイルが格納されているディレクトリを指定してアラームログファイル一覧を得る
        p = Path(dir_path_to_process)

        # 指定されたディレクトリが存在しない場合はメッセージを表示してスクリプトの実行を終了する．
        if not p.exists():
            print ("*************************************************************")
            print ("ALMLOGディレクトリが見つかりません． ALMLOGのフォルダパスを正しく指定してください")
            print ("*************************************************************")
            assert(False)

        # 指定されたディレクトリ内の拡張子(suffix)がcsvのファイルのリストを作成する．
        csvList = [str(x) for x in p.iterdir() if x.suffix[1:].lower() == "csv"]

        # 上記で作成したリストの件数(CSVファイルの個数)が 0 ならスクリプトの実行を中断する
        if len(csvList) == 0:
            print("CSVファイルがありません， ALMLOGフォルダを指定してください")
            assert(False)

        # CSVファイルをソートしておく
        csvList.sort()
        print(f"ディレクトリ（{dir_path_to_process}）内のアラームログファイル数 : {len(csvList)}")

        # CSVファイルを全てロードし， ひとつのDataFrameにまとめる
        li = []
        for csv in csvList:
            df_csv = pd.read_csv(csv, skiprows=3, encoding = "shift-jis", usecols=[0, 1, 3, 4, 5, 6, 7, 8])
            li.append(df_csv)

        df = pd.concat(li, axis=0, ignore_index=True)
    
    else :
        # ALMLOGディレクトリパスが指定されていない場合はサンプルのCSVのデータを読む
        df = pd.read_csv("sample.csv", encoding = "shift-jis")
        
    
    
    ########## 前処理 ##########
    
    # カラム名の先頭に半角スペースが含まれているので削除
    df.columns=df.columns.str.replace(' ','');

    # 時刻カラムはdatetimeにしておく
    df['時刻'] = pd.to_datetime(df['時刻'], errors='coerce')
    
    # 各要素の値の先頭に半角スペースがついているので削除
    df = df.applymap(lambda x: str(x).strip())

    # 削除対象のDataFrameのindexを格納するリスト． 後続の処理で削除対象のindexを格納していく
    indexesToDel = []

    # 時刻がNaTである行は削除対象
    indexesToDel.extend(df[(df["時刻"] == "NaT")].index)

    # CSVの最後にくっついてる不要な行は削除対象
    indexesToDel.extend(df[(df["No."] == "[END]")].index)

    # 下記のアラームは削除対象
    alarmCodeToDelete = [
        # 設定変更や操作ログの類は削除
        "0x201A", # モニタ中断タイマ
        "0x3001", # (設定変更 閾値) 心拍数上限設定変更	
        "0x3100", # (設定変更 閾値) ＣＯ2−Ｅ上限設定変更(mmHg)
        "0x3201", # (設定変更 閾値) 心拍数下限設定変更
        "0x3210", # (設定変更 閾値) ＳｐＯ2下限設定変更
        "0x340F", # (設定変更 ONOFF) 無呼吸全体ON/OFF変更
        "0x3410", # (設定変更 ONOFF) ＳｐＯ2全体ON/OFF変更
        "0x3425", # (設定変更 ONOFF) ＢＰ１（Ｄ）全体ON/OFF変更(mmHg)
        "0x3426", # (設定変更 ONOFF) ＢＰ１（Ｍ）全体ON/OFF変更(mmHg)
        "0x3443", # (設定変更 ONOFF) ＩＣＰ（Ｍ）全体ON/OFF変更(mmHg)
        "0x34BB", # (設定変更 ONOFF) ＮＩＢＰ（Ｄ）全体ON/OFF変更(mmHg)
        "0x34BC", # (設定変更 ONOFF) ＮＩＢＰ（Ｍ）全体ON/OFF変更(mmHg)
        "0x3500", # (設定変更 ONOFF) ＣＯ2−Ｅ全体ON/OFF変更(mmHg)
        "0x3530", # (設定変更 ONOFF) EXT_SpO2 全体ON/OFF設定変更
        "0x3A10", # (設定変更 閾値) Ext Tachy 設定変更
        "0x3A11", # (設定変更 閾値) Ext Brady 設定変更
        "0x3B08", # (設定変更 ONOFF) ＲＵＮ　ON/OFF変更
        "0x3B0C", # (設定変更 ONOFF) Ext Tachy ON/OFF設定変更
        "0x3B0D", # (設定変更 ONOFF) Ext Brady ON/OFF設定変更
        "0x4000", # (全体ｱﾗｰﾑ変更) アラーム音中断開始）
        "0x4002", # (全体ｱﾗｰﾑ変更) アラーム中断開始） 
        "0x4003", # (全体ｱﾗｰﾑ変更) アラーム中断解除）
        "0x4006", # (全体ｱﾗｰﾑ変更) アラーム音レベル
        "0x6000", # ■退床
        "0x6004", # ■モニタ中断開始
        "0x6005", # ■モニタ中断解除
        
        # 不整脈アラームの内，　計測値アラームでも同様のものがログとして残るため削除
        "0x0800",  # TACHY
        "0x0801",  # BRADY
    ]
    for code in alarmCodeToDelete:
        indexesToDel.extend(df[(df['コード'] == code)].index)

    # DataFrameから削除対象の行を削除する    
    df.drop(indexesToDel, inplace=True)
    
    # CSVでは，アラーム名称の前に必ず「(ｱﾗｰﾑ発生) 」が存在する． 視認性が悪くなるだけなので削除
    df['発生要因'] = df.apply(lambda x: x['発生要因'].replace('(ｱﾗｰﾑ発生) ', ''), axis=1)
    
    # 厳密には異なるが解析上同じでも支障のないアラームはまとめる
    df.replace({'0x2022': '0x201F', '心電図１ノイズ混入': '心電図ノイズ混入'}, inplace=True)
    df.replace({'0x2020': '0x201E', '心電図１低振幅': '心電低振幅'}, inplace=True)
    df.replace({'0x2001': '0x2000', '電極確認（Ｒ／ＲＡ）': '電極確認'}, inplace=True)
    df.replace({'0x2003': '0x2000', '電極確認（Ｆ／ＬＬ）': '電極確認'}, inplace=True)
    df.replace({'0x112E': '0x1010', 'EXT_SpO2下限': 'ＳｐＯ2下限'}, inplace=True)

    # 継続時間のデータ型をintに変更
    df['継続時間int'] = pd.to_numeric(df['継続時間'], errors="coerce")
    #df['継続時間'] = df.apply(lambda x: x['継続時間'].replace('', '0'), axis=1)
    df['継続時間'] = pd.to_numeric(df['継続時間'], errors="coerce")
    df['継続時間'] = df['継続時間'].astype('int')

    # 時刻のHHを値にもつhour列を作成する．
    df['hour'] = df.apply(lambda x: x['時刻'][11:13], axis=1)
    # 日付をDDHHに変換した列を作成する．
    df['dayhour'] = df.apply(lambda x: x['時刻'][5:13].replace('-', '月').replace(' ', '日') + '時', axis=1)
    # 日付を DDHHX0分台 に変換した列を作成する．　（例： 09日10時50分台）
    df['dayhour10min'] = df.apply(lambda x: x['時刻'][8:13].replace(' ', '日') + '時' + x['時刻'][14:15] + '0分台', axis=1)
    
    # アラームレベルをアルファベット一文字で表す列を追加
    df['alarm_level'] = df.apply(lambda x: x['レベル'][0:1], axis=1)
    
    # アラーム種別の列を追加
    df['alarm_type'] = df.apply(lambda x: x['レベル'][1:], axis=1)

    df['時刻'] = pd.to_datetime(df['時刻'], format='%Y-%m-%d %H:%M:%S', infer_datetime_format=True)
    df.sort_values(by = '時刻', ascending = True, inplace = True)
    
    # 経過時間（CSVに記載されている最初のアラートの記録時刻を 0秒 or 0分とした時の）の列を追加する
    log_start_time = df['時刻'].min()
    df['start_datetime'] = log_start_time   # 最初のアラートの記録時刻
    df['diff_datetime'] = df['時刻'] - df['start_datetime']   # 経過時刻（秒）を取得
    df['diff_sec'] = df['diff_datetime'].map(lambda x: x.total_seconds())   # 経過時刻（分）に変換
    df['diff_min'] = df['diff_datetime'].map(lambda x: math.floor( x.total_seconds() / 60))   # 経過時刻（分）に変換
    
    print(f"記録時刻:{df['時刻'].min()} 〜 {df['時刻'].max()},  {df['diff_datetime'].max()} ({math.floor(df['diff_min'].max() / 60)}時間)")
    
    # 前処理後のCSVファイルをmerged.csvというファイル名でアラームログCSVファイルと同じディレクトリに保存する
    # merged_csv_file_path = dir_path_to_process.replace(os.sep, '/') + os.sep + "merged.csv"
    # df.to_csv(merged_csv_file_path)
    
    return df


#######################
# データ取得系関数
#######################
def getAlarmHistoryByAlarmType(df, alarm_type):
    '''
     * alarm_typeで指定されたアラーム種別のみを含むDataFrameを返す
    '''

    # 残すアラーム履歴のindexを得る
    indexesToLeave = []
    for code in alarm_type:
        indexesToLeave.extend(df[(df['コード'] == code)].index)

    # 全体のリストとの差分（削除対象）を得る
    diff_list = set(df.index) ^ set(indexesToLeave)

    # DataFrameから削除対象の行を削除する    
    df.drop(diff_list, inplace=True)
    
    return df

#######################
# 集計・グラフ描画系関数
#######################
def pivotTableByHour(df):
    '''
     * 全アラームの日時(○日○時)別のCH別アラーム件数をPivotテーブルで表示する
     * df : DataFrame
    '''
    d = pd.pivot_table(df, index=['dayhour'], columns='床番号', values='コード', aggfunc=len, fill_value=0, margins=True)
    patient_count = len(df['床番号'].unique())
    print(f"患者数 = {patient_count}")
    d['回/患者'] = d['All'] / patient_count
    
    return d


def pivotTableByHourByAlarm(df, code_to_analyze, patient_count):
    '''
     * 指定されたアラームの日時(○日○時)別のCH別アラーム件数をPivotテーブルで表示する
     * df : DataFrame
     * code_to_analyze : アラームコード
    '''
    d = pd.pivot_table(df.query(f'コード == "{code_to_analyze}"'), index=['dayhour'], columns='床番号', values='コード', aggfunc=len, fill_value=0, margins=True)
    print(f"患者数 = {patient_count}")
    d['回/患者'] = d['All'] / patient_count
    
    return d


def plotBarByHour(df):
    '''
        鳴動したアラームの時間（h)別の合計アラーム件数の棒グラフを表示する．アラームデータが複数日に渡る場合は，時間別に合算する．
        df : DataFrame
    '''
    pt = df[['dayhour']].groupby('dayhour').size()
    pt.plot.bar(figsize=(20, 8), fontsize=14, title=f"全アラームの hour 別の合計件数", color=CMAP)
    

def plotBarByHourByAlarm(df, code_to_analyze):
    '''
        指定されたアラームの時間（h)別の合計アラーム件数の棒グラフを表示する．アラームデータが複数日に渡る場合は，時間別に合算する．
        df : DataFrame
        code_to_analyze : アラームコード
    '''
    pt = df.query(f'コード == "{code_to_analyze}"')[['dayhour']].groupby('dayhour').size()
    pt.plot.bar(figsize=(20, 8), fontsize=14, title=f"{ALARM_CODE[code_to_analyze]}の hour 別の合計件数")

    
def plotBarByHourByChannelByAlarm(df, code_to_analyze):
    '''
     * 指定されたアラームの時間（h)別のCH別の合計アラーム件数の棒グラフを表示する
     * df : DataFrame
     * code_to_analyze : アラームコード
    '''
    pt = pd.pivot_table(df.query(f'コード == "{code_to_analyze}"'), index=['dayhour'], columns='床番号', values='コード', aggfunc=len, fill_value=0)
    ch_list = df.query(f'コード == "{code_to_analyze}"')['床番号'].unique()

    fig = plt.figure(figsize=(12, 24))
    fig.suptitle = f"{ALARM_CODE[code_to_analyze]}アラームのch別のhour別件数"

    for i in range(len(ch_list)):
        ch = ch_list[i]
        plt.subplot(math.ceil(len(ch_list)/1), 1, i+1)
        plt.legend(ch)
        plt.ylim(0, 20)
        plt.xticks(rotation=90, fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.bar(pt.index, pt[ch], label=ch)
        plt.legend()

    plt.tight_layout()
    
    
def plotBarByHourByChannel(df):
    '''
     * 指定されたアラームの時間（h)別のCH別の合計アラーム件数の棒グラフを表示する
     * df : DataFrame
     * code_to_analyze : アラームコード
    '''
    pt = pd.pivot_table(df, index=['dayhour'], columns='床番号', values='コード', aggfunc=len, fill_value=0)
    ch_list = df['床番号'].unique()

    fig = plt.figure(figsize=(12, 36))
    #fig.suptitle = f"{ALARM_CODE[code_to_analyze]}アラームのch別のhour別件数"
    fig.suptitle = f"アラームのch別のhour別件数"

    for i in range(len(ch_list)):
        ch = ch_list[i]
        plt.subplot(math.ceil(len(ch_list)/1), 1, i+1)
        plt.legend(ch)
        plt.ylim(0, 100)
        plt.xticks(rotation=90, fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.bar(pt.index, pt[ch], label=ch)
        plt.legend()

    plt.tight_layout()