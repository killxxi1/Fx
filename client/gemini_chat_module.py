# gemini_chat_module.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# GEMINI_API_KEY 가져오기
api_key = os.getenv("GEMINI_API_KEY")

# API 키가 없으면 예외 발생
if not api_key:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file. Please create a .env file with GEMINI_API_KEY='your_key_here'")

# Gemini API 설정
genai.configure(api_key=api_key)

def start_gemini_chat(model_name: str, initial_prompt: str):
    """
    Gemini 모델과의 새로운 채팅 세션을 시작하고 초기 프롬프트를 설정합니다.
    이 초기 프롬프트는 대화의 첫 번째 메시지로 전송되어 모델이 컨텍스트를 기억하게 합니다.

    Args:
        model_name (str): 사용할 Gemini 모델 이름 (예: "gemini-2.5-flash", "gemini-1.5-pro").
        initial_prompt (str): 대화의 시작 컨텍스트를 설정하는 초기 프롬프트.
                              (예: "당신은 전문 번역가입니다. 사용자의 요청에 따라 한국어와 영어 사이를 번역해주세요.")

    Returns:
        genai.ChatSession: 대화 기록을 관리하는 ChatSession 객체.
                           이 객체를 통해 멀티턴 대화를 이어갈 수 있습니다.
    """
    try:
        model = genai.GenerativeModel(model_name)
        # 빈 대화 기록으로 채팅 세션 시작
        chat = model.start_chat(history=[])
        # 초기 프롬프트를 첫 메시지로 보내 모델이 컨텍스트를 학습하게 함
        chat.send_message(initial_prompt)
        return chat
    except Exception as e:
        print(f"Error starting chat session: {e}")
        raise # 예외를 다시 발생시켜 호출하는 쪽에서 처리할 수 있도록 함

def send_chat_message(chat_session: genai.ChatSession, message: str) -> str:
    """
    진행 중인 채팅 세션에 메시지를 보내고 모델의 응답을 받습니다.
    이 함수는 이전 대화 기록을 자동으로 포함하여 멀티턴 대화를 가능하게 합니다.

    Args:
        chat_session (genai.ChatSession): `start_gemini_chat`으로 얻은 ChatSession 객체.
        message (str): 사용자(또는 시스템)의 새로운 메시지.

    Returns:
        str: 모델의 응답 텍스트. API 호출 실패 시 오류 메시지를 반환합니다.
    """
    try:
        response = chat_session.send_message(message)
        return response.text
    except Exception as e:
        return f"An error occurred during the Gemini API call: {e}"

if __name__ == '__main__':
    print("--- Gemini 멀티턴 대화 모듈 테스트 ---")
    print("번역 챗봇을 시작합니다. '종료'를 입력하면 대화가 끝납니다.")

    try:
        # 번역가 챗봇 세션 시작
        translator_chat = start_gemini_chat(
            model_name="gemini-2.5-flash", # 또는 "gemini-1.5-pro" 등 적절한 모델 선택
            initial_prompt="당신은 전문 번역가입니다. 사용자의 요청에 따라 한국어와 영어 사이를 번역해주세요. 예시: 'Hello'를 한국어로 번역해줘 -> 안녕하세요"
        )
        print("\n번역가 챗봇: 안녕하세요! 무엇을 번역해 드릴까요?")

        while True:
            user_input = input("사용자: ")
            if user_input.lower() == '종료':
                print("번역 챗봇: 대화를 종료합니다. 다음에 또 만나요!")
                break

            response_text = send_chat_message(translator_chat, user_input)
            print(f"번역 챗봇: {response_text}")

            # 선택 사항: 대화 기록 확인
            # print("\n--- 현재 대화 기록 ---")
            # for msg in translator_chat.history:
            #     print(f"  {msg.role}: {msg.parts[0].text}")
            # print("----------------------\n")

    except ValueError as ve:
        print(f"초기화 오류: {ve}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")