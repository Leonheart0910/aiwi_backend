import requests
import os

# 네이버 오픈API 자격 증명
# 실제 서비스에선 아래 키를 .env 등 외부 설정으로 관리하는 것이 안전합니다
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "Mrr2UMiNyTchLj0oFvhY")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "nAiQnJzbqu")

def search_naver_shopping(query: str):
    """
    네이버 쇼핑 API를 이용해 상품 검색 결과를 가져오는 함수

    Args:
        query (str): 검색어 (예: "선풍기", "아이패드", "책상")

    Returns:
        dict: 검색 결과 JSON 응답. 실패 시 None 반환
    """
    url = "https://openapi.naver.com/v1/search/shop.json"  # 요청 URL

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    params = {
        "query": query,        # 검색어
        "display": 10,         # 검색 결과 개수 (최대 100)
        "start": 1,            # 검색 시작 위치 (1 ~ 1000)
        "sort": "sim"          # 정렬 방식: sim(정확도), date(날짜), asc(가격↑), dsc(가격↓)
    }

    # API 호출
    response = requests.get(url, headers=headers, params=params)

    # 응답 상태 코드가 200(성공)이면 JSON 반환
    if response.status_code == 200:
        return response.json()
    else:
        # 실패 시 로그 출력
        print(f"[❌ Naver API 오류] {response.status_code}: {response.text}")
        return None
