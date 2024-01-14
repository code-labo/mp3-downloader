# MP3 downloader from Youtube

## Abstract
youtube上に作成したプレイリストをmp3形式でダウンロードするスクリプト

## Usage

### 1. 必要なライブラリのインストール
~~~bash
pip install -r requirements.txt
~~~

### 2. パスの設定
`main/envs.py`に以下の変数を設定する.  
ここでいうchromeのユーザー名はプレイリストを作成したアカウントのこと.

|    変数名     |                  説明                  |
| :-----------: | :------------------------------------: |
| PROFILE_PATH  |   chromeのユーザープロフィールのパス   |
| PROFILE_NAME  |           chromeのユーザー名           |
| DOWNLOAD_PATH | デフォルトのダウンロードフォルダのパス |

例）
~~~python
PROFILE_PATH="C:/Users/user_name/AppData/Local/Google/Chrome/User Data"
PROFILE_NAME="Profile 2"
DOWNLOAD_PATH=r"C:\Users\user_name\Downloads"
~~~

### 3. 実行
youtubeのプレイリストのurlを指定して実行.  
mp3は`output/mp3`内にダウンロードされる.  
※urlはダブルクォート「""」でくくらないとダメ. そうしないとプレイリストじゃなくて, 動画単品へのアクセスになる.

~~~bash
python main\\main.py --playlist_url "https://www.youtube.com/watch?v=ZRtdQ81jPUQ&list=PLVA9oq_5voOzf_NNE26JWy5azAPSgzHPm"
~~~

## Appendix
chromeに拡張機能としてAdblockを入れといたほうがいいかもしれない.  
youtubeの動画をダウンロードするサイトはかなりグレーなサイトなので広告がうるさい.