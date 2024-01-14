import sys
from pathlib import Path
PARENT=str(Path(__file__).parent)
ROOT=str(Path(__file__).parent.parent)
sys.path.append(ROOT)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_driver(profile_path,profile_name):

    ##バックグラウンドで実行する際のオプション
    ##コメント外すとバックグラウンドで実行される
    # options=Options()
    options= webdriver.ChromeOptions()

    # >> 新しいタイプのselenium >>
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_name}")
    # options.add_argument("--headless=new") #selenium4.8 以降のheadlessはこうやって設定する
    options.add_argument('--no-sandbox')
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument("--disable-dev-shm-usage") 
    # options.add_argument("disable-gpu")
    options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
    options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
    options.add_argument("--ignore-certificate-errors")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # options.add_experimental_option("prefs", {
    #     "profile.default_content_settings.popups": 0,  
    #     "download.default_directory": r"C:/dev/projects/python-projects/mp3-downloader/output",
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    # })
 
    driver=webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options,
    )
    # << 新しいタイプのselenium <<

    driver.set_window_size(1280,720)
    driver.implicitly_wait(5)
    time.sleep(3)

    return driver


if __name__=="__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from envs import *

    driver=init_driver(
        PROFILE_PATH,PROFILE_NAME
    )
    driver.get("https://twitter.com/home")
    time.sleep(5)
    driver.quit()