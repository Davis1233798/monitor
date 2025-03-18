import requests
from bs4 import BeautifulSoup
import os
import re

# 從環境變量中獲取 Telegram Token 和 Chat ID
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.serv00.com/"
URL2 = "https://www.ct8.pl/"

# 檢查環境變量是否有效
if not TOKEN or not CHAT_ID:
    raise ValueError(f"環境變量未正確設置 - TOKEN: {TOKEN}, CHAT_ID: {CHAT_ID}")

def get_numbers(url):
    # 抓取網頁內容，設置 5 秒超時
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    # 使用 lxml 解析器以提高效率
    soup = BeautifulSoup(response.text, "lxml")

    # 找到目標 span 標籤
    span = soup.find("span", class_="button is-large is-flexible")
    if not span:
        raise ValueError(f"無法找到指定的 span 標籤，URL: {url}")
    
    # 提取並解析 xxxxx / ooooo
    text = span.get_text(strip=True)
    match = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if not match:
        raise ValueError(f"無法從文本中提取數字，URL: {url}")
    
    xxxxx = int(match.group(1))  # 第一個數字
    ooooo = int(match.group(2))  # 第二個數字
    return xxxxx, ooooo

def send_message(message):
    # 發送 Telegram 通知
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()

def main():
    try:
        # 獲取兩個網頁的數字
        xxxxx, ooooo = get_numbers(URL)
        xx, oo = get_numbers(URL2)
        
        # 計算差異
        difference = ooooo - xxxxx
        dif = oo - xx
        
        # 發送 Telegram 通知
        if difference > 2:
            message = (
                f"警告：ooooo - xxxxx = {difference} > 2\n當前值：{xxxxx} / {ooooo}"
            )
            send_message(message)
        if dif > 2:
            message = f"警告：oo - xx = {dif} > 2\n當前值：{xx} / {oo}"
            send_message(message)
        
        # 運行結束後的輸出
        if difference > 2 or dif > 2:
            print(f"網站網址: {URL}")
            print(f"網站網址: {URL2}")
            print(f"{URL} 目前可註冊數量: {ooooo - xxxxx}")
            print(f"{URL2} 目前可註冊數量: {oo - xx}")
        else:
            print(f"目前 {URL} 及 {URL2} 皆無法註冊")

    except Exception as e:
        error_message = f"監測腳本出現錯誤：{str(e)}"
        send_message(error_message)
        print(f"錯誤：{str(e)}")

if __name__ == "__main__":
    main()
