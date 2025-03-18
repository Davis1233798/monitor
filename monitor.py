import requests
from bs4 import BeautifulSoup
import os
import re
import time

# 從環境變量中獲取 Telegram Token 和 Chat ID
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.serv00.com/"
URL2 = "https://www.ct8.pl/"

# 檢查環境變量是否有效
if not TOKEN or not CHAT_ID:
    raise ValueError(f"環境變量未正確設置 - TOKEN: {TOKEN}, CHAT_ID: {CHAT_ID}")


def get_numbers(url, retries=3, timeout=15):
    """獲取網頁中的數字，包含重試機制和超時設置"""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            span = soup.find("span", class_="button is-large is-flexible")
            if not span:
                raise ValueError(f"無法找到指定的 span 標籤，URL: {url}")
            text = span.get_text(strip=True)
            match = re.search(r"(\d+)\s*/\s*(\d+)", text)
            if not match:
                raise ValueError(f"無法從文本中提取數字，URL: {url}")
            xxxxx = int(match.group(1))
            ooooo = int(match.group(2))
            return xxxxx, ooooo
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2)  # 重試前等待 2 秒
                continue
            else:
                raise e


def send_message(message):
    """發送 Telegram 通知"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()


def main():
    """主函數，執行監測並處理異常"""
    try:
        xxxxx, ooooo = get_numbers(URL)
        xx, oo = get_numbers(URL2)
        difference = ooooo - xxxxx
        dif = oo - xx

        if difference > 2:
            message = (
                f"警告：ooooo - xxxxx = {difference} > 2\n當前值：{xxxxx} / {ooooo}"
            )
            send_message(message)
        if dif > 2:
            message = f"警告：oo - xx = {dif} > 2\n當前值：{xx} / {oo}"
            send_message(message)

        if difference > 2 or dif > 2:
            message = (
                f"Respority:Davis1233798/monitor.py\n"
                f"github acrtions\n"
                f"網站網址: {URL}\n"
                f"網站網址: {URL2}\n"
                f"{URL} 目前可註冊數量: {difference}\n"
                f"{URL2} 目前可註冊數量: {dif}"
            )
            send_message(message)

    except requests.exceptions.Timeout:
        error_message = (
            f"Respority:Davis1233798/monitor.py\n"
            f"github acrtions\n"
            f"請求超時：{URL} 或 {URL2}"
        )
        send_message(error_message)
    except requests.exceptions.ConnectionError:
        error_message = (
            f"Respority:Davis1233798/monitor.py\n"
            f"github acrtions\n"
            f"請求超時：{URL} 或 {URL2}"
        )
        send_message(error_message)
    except requests.exceptions.ConnectionError:
        error_message = (
            f"Respority:Davis1233798/monitor.py\n"
            f"github acrtions\n"
            f"監測腳本出現錯誤：{str(e)}"
        )
        send_message(error_message)


if __name__ == "__main__":
    main()
