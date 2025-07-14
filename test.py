# %%

from client.gemini_client import gemini_call


translated_text = gemini_call(
    model="gemini-2.5-flash",
    prompt="당신은 전문 번역가입니다.",
    question="'Hello, world!'를 한국어로 번역해줘."
)

print(f"Translated text: {translated_text}")


# %%
