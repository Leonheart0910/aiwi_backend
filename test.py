import requests

# ✅ 발급받은 키 입력
CLIENT_ID = "Mrr2UMiNyTchLj0oFvhY"
CLIENT_SECRET = "nAiQnJzbqu"

# ✅ 검색어 및 파라미터 구성
query = "선풍기"
url = "https://openapi.naver.com/v1/search/shop.json"

params = {
    "query": query,
    "display": 10,
    "start": 1,
    "sort": "sim"  # sim(정확도순), date, asc(가격↑), dsc(가격↓)
}

headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET
}

# ✅ API 요청
response = requests.get(url, headers=headers, params=params)

# ✅ 응답 처리
if response.status_code == 200:
    data = response.json()
    for i, item in enumerate(data["items"], 1):
        print(f"[{i}] 🛒 {item['title']} | 💰 {item['lprice']}원 | 🏬 {item['mallName']}")
        print(f"     🔗 {item['link']}")
else:
    print(f"❌ 요청 실패: {response.status_code} - {response.text}")
