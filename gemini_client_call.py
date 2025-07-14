# %%

from client.gemini_client import gemini_call


text = gemini_call(model="gemini-2.5-flash",
                   prompt="당신은 뉴스 리포터 입니다.",
                   question="오늘의 날씨를 보고해주세요.")

print(f"Translated text: {text}")


# %%
