from typing import List, Dict, Any

from pydantic import BaseModel


class ChatInput(BaseModel):
    chat_id: int
    user_input: str

class Recommendation(BaseModel):
    keyword: str
    category: str
    summary: str

class Node1Output(BaseModel):

    question: str
    checklist: List[str]
    keywords: List[Dict[str, str]]
    checklist_message: str

class Node2Output(BaseModel):
    keywords: List[Dict[str, str]]
    search_results: List[Dict[str, Any]]

class Node4Output(BaseModel):
    search_results: List[Dict[str, any]]  # 필요 시 더 정교하게 정의 가능
    recommendations: List[Recommendation]