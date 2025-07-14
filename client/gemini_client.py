# gemini_translator.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def gemini_call(model: str, prompt: str, question: str) -> str:
    """
    Makes a call to the Google Gemini API for translation.

    Args:
        model (str): The Gemini model to use (e.g., "gemini-2.5-flash").
        prompt (str): The initial prompt to set the context for the model
                      (e.g., "당신은 전문 번역가입니다.").
        question (str): The specific question or text to be processed
                        (e.g., "'Hello, world!'를 한국어로 번역해줘.").

    Returns:
        str: The translated or processed text from the Gemini API,
             or an error message if the call fails.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY not found in .env file."

    # Configure the Gemini API with your API key
    genai.configure(api_key=api_key)

    try:
        # Initialize the generative model
        model_instance = genai.GenerativeModel(model)

        # Combine the prompt and question for the API call
        full_query = f"{prompt}\n{question}"

        # Generate content using the model
        response = model_instance.generate_content(full_query)

        # Return the translated text
        return response.text

    except Exception as e:
        return f"An error occurred during the Gemini API call: {e}"

if __name__ == '__main__':
    # Example usage when running this file directly
    print("--- Example Usage ---")
