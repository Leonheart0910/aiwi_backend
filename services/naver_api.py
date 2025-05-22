import os
from dotenv import load_dotenv
import requests

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET_KEY = os.getenv("NAVER_SECRET_KEY")


headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_SECRET_KEY,
}

def search_naver_shopping(query: str):

    url = "https://openapi.naver.com/v1/search/shop.json"

    params = {
        "query": query,
        "display": 5,
        "start": 1,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        print(f"[Naver API 오류] {response.status_code}: {response.text}")
        return None