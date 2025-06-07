import os
from typing import Optional

from sqlalchemy.orm import Session

import google.generativeai as genai
from dotenv import load_dotenv

from schemas.aiwi import AiwiCreate
from schemas.aiwi_log import AiwiLogCreate
from services.naver_api import search_naver_shopping
from crud.aiwi import create_aiwi
from crud.aiwi_log import create_aiwi_log
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def gemini_search(query: str) -> str:
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"에러 발생: {str(e)}"

def three_stage_conversion(query: str):
    # 키로 바로 접근하기 위해서 dictionary를 사용
    outputs = {}

    try:
        first_answer = gemini_search(query + "정리는 한줄 정도")
        outputs["첫번째 분기 응답"] = first_answer
        second_answer = gemini_search(first_answer)
        outputs["두번째 분기 응답"] = second_answer
        third_answer = gemini_search(second_answer + "한줄로 요점만 요약해줘")
        outputs["세번째 분기 응답"] = third_answer
        return outputs
    except Exception as e:
        return {"error": f"{e}"}

def process_user_input(
        query: str,
        chat_id: Optional[int],
        user_id: int,
        db:Session):

    # 만약 첫 채팅이면 생성해서 DB에 저장한다.
    if chat_id is None:
        new_chat = AiwiCreate(
            title=query,
            user_id=user_id,
        )
        chat_id_temp = create_aiwi(db ,new_chat).chat_id
    else:
        chat_id_temp = chat_id
    #여기서 분기마다 나온 아웃풋을 저장하게 된다.
    brunch_outputs = three_stage_conversion(query)
    if not isinstance(brunch_outputs, dict) or "세번째 분기 응답" not in brunch_outputs:
        return {"error": "AI 응답 생성 실패"}

    #네이버 API로 값을 전달한다.
    try:
        response = search_naver_shopping(brunch_outputs["세번째 분기 응답"])
        if not response or "error" in response:
            return {"error": "네이버 쇼핑 API 오류 또는 응답 없음 " + brunch_outputs["세번째 분기 응답"]}
        log_data = AiwiLogCreate(
            user_input=query,
            chat_id=chat_id_temp,
            ai_output1=brunch_outputs["첫번째 분기 응답"],
            ai_output2=brunch_outputs["두번째 분기 응답"],
            ai_output3=brunch_outputs["세번째 분기 응답"],
        )
        create_aiwi_log(db, log_data)
        return {
            "status": "ok",
            "final_result": response,
            "chat_id": chat_id_temp
        }
    except Exception as e:
        return {"error발생!!!!": str(e)}


