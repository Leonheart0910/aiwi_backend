import requests
import os

# 발급받은 Google API 키
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_google_api_key")

def call_gemini_api(user_input: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    # 프롬프트 구성 (예시 prompt 템플릿)
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""사용자가 다음과 같은 구매 요구를 입력했습니다: "{user_input}"

다음 세 가지 항목으로 응답해주세요:
1. 상황에 맞는 제품 카테고리 추천
2. 해당 조건에 적합한 검색 키워드
3. 제품들의 특성 비교 및 요약

각 항목을 구분된 문자열로 출력해주세요.
"""
                    }
                ]
            }
        ]
    }

    # API 호출
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

        # 결과 분리: 구분자 기준으로 나눔
        lines = result_text.strip().split("\n")
        output1 = next((line for line in lines if line.startswith("1.")), "1. 없음")
        output2 = next((line for line in lines if line.startswith("2.")), "2. 없음")
        output3 = next((line for line in lines if line.startswith("3.")), "3. 없음")

        return {
            "ai_output1": output1.replace("1. ", ""),
            "ai_output2": output2.replace("2. ", ""),
            "ai_output3": output3.replace("3. ", "")
        }

    else:
        print(f"[❌ Gemini API 오류] {response.status_code}: {response.text}")
        return {
            "ai_output1": "API 호출 실패",
            "ai_output2": "",
            "ai_output3": ""
        }
