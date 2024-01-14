import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

import argparse

import time
import pandas as pd
from tqdm import tqdm
import os
import shutil
import re

from selenium.webdriver.common.by import By
from src import init_driver
from envs import *

# url="https://www.youtube.com/watch?v=ZRtdQ81jPUQ&list=PLVA9oq_5voOzf_NNE26JWy5azAPSgzHPm"

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--playlist_url",
                        type=str,
                        help="youtubeのプレイリストのurl.必ずダブルクォートをつける.",
                        default="https://www.youtube.com/watch?v=ZRtdQ81jPUQ&list=PLVA9oq_5voOzf_NNE26JWy5azAPSgzHPm",
                        )
    args=parser.parse_args()

    try:

        #>> youtubeのプレイリスト上からアイテムのタイトルとurlをCSVとして取ってくる >>
        print("=== finding playlist items on Youtube ===")
        driver=init_driver(
            PROFILE_PATH,PROFILE_NAME
        )
        playlist_url=args.playlist_url
        driver.get(playlist_url)

        time.sleep(5)
        
        playlists=[]

        playlist_resources=driver.find_elements(by=By.TAG_NAME, value="ytd-playlist-panel-video-renderer")
        for item in playlist_resources:
            item_url=item.find_element(by=By.TAG_NAME,value="a").get_attribute(name="href")
            item_title=item.find_element(by=By.TAG_NAME,value="h4").find_element(by=By.TAG_NAME,value="span").get_attribute(name="title")
            playlists.append(
                [item_title,item_url]
            )

        print(playlists)
        print("")
        pd.DataFrame(playlists,columns=["title","url"]).to_csv(f"{ROOT}/output/playlist.csv",index=False,encoding="utf-8")
        #>> youtubeのプレイリスト上からアイテムのタイトルとurlをCSVとして取ってくる >>


        #>> urlからmp3にしてダウンロードする >>
        print("\n=== now download playlist itmes from youtube to local===")
        for item in tqdm(playlists):
            downloader_url="https://www.y2mate.com"
            driver.get(downloader_url)
            time.sleep(1)

            form_element=driver.find_element(by=By.TAG_NAME,value="input") #form要素見つける
            form_buttom=driver.find_element(by=By.ID,value="btn-submit") #form送信ボタン

            item_title,item_url=item
            form_element.clear()
            form_element.send_keys(item_url)
            form_buttom.click()
            time.sleep(2)
            
            driver.find_elements(by=By.CLASS_NAME,value="nav-link")[1].click() #audioタブに移動
            time.sleep(1)

            audio_tab=driver.find_element(by=By.ID,value="audio")
            audio_tab.find_element(by=By.TAG_NAME,value="button").click() #convert
            time.sleep(3)

            driver.find_element(by=By.ID,value="process-result").click() #downloadボタンをクリック

            time.sleep(5)
        time.sleep(10)
        #>> urlからmp3にしてダウンロードする >>
            
        #>> downloadフォルダから移動 >>
        print("=== moving .mp3 files from download dir to output dir ===")
        download_dir=DOWNLOAD_PATH
        downlaod_files=os.listdir(download_dir)

        if not os.path.exists(f"{ROOT}/output/mp3"):
            os.mkdir(f"{ROOT}/output/mp3")

        for file in tqdm(downlaod_files):
            if ".mp3" in file and "y2mate.com" in file and not ".crdownload" in file:
                new_file_name=re.sub("y2mate.com - ","",f"{ROOT}/output/mp3/{file}")
                if os.path.exists(new_file_name):
                    os.remove(new_file_name)

                shutil.move(f"{download_dir}/{file}",new_file_name)
        #>> downloadフォルダから移動 >>
                
    except Exception as e:
        print(e)

    finally:
        driver.quit()


if __name__=="__main__":
    main()

