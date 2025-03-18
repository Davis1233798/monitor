# 從環境變量中獲取 Telegram Token 和 Chat ID

import requests
from bs4 import BeautifulSoup
import os
import re

# 從環境變量中獲取 Telegram Token 和 Chat ID

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHATID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.serv00.com/"
URL2 = "https://www.ct8.pl/"


def get_numbers(url):
    # 抓取網頁內容
    response = requests.get(url)  # 使用傳入的 url
    response.raise_for_status()  # 如果請求失敗，拋出異常
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到目標 span 標籤
    span = soup.find("span", class_="button is-large is-flexible")
    if not span:
        raise ValueError("無法找到指定的 span 標籤")

    # 提取並解析 xxxxx / ooooo
    text = span.get_text(strip=True)
    match = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if not match:
        raise ValueError("無法從文本中提取數字")

    xxxxx = int(match.group(1))  # 第一個數字
    ooooo = int(match.group(2))  # 第二個數字
    return xxxxx, ooooo


def send_message(message):
    # 發送 Telegram 通知
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHATID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()


def main():
    try:
        # 獲取數字並計算差異
        xxxxx, ooooo = get_numbers(URL)
        xx, oo = get_numbers(URL2)
        difference = ooooo - xxxxx
        dif = oo - xx
        if difference > 2:
            message = f"{URL} 可註冊 = {difference} > 2\n當前值：{xxxxx} / {ooooo}"
            send_message(message)
        elif difference < 0:
            message = f"{URL2} 可註冊 = {difference} < 0\n當前值：{xxxxx} / {ooooo}"
            send_message(message)
        else:
            message = f"目前可註冊數量：{difference}\n{URL}：{xxxxx} / {ooooo}\n{URL2}：{xx} / {oo}"
            send_message(message)

    except Exception as e:
        # 錯誤處理
        error_message = f"監測腳本出現錯誤：{str(e)}"
        send_message(error_message)


if __name__ == "__main__":
    main()
