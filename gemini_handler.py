import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Loaded API Key:", "FOUND" if api_key else "NOT FOUND")

genai.configure(api_key=api_key)

def gemini_summarize(text):
    try:
        print("Starting summarization...")
        print("Text length:", len(text))

        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""Summarize the following document in a concise yet informative way. 
Make it suitable for professional review. Text:
{text}
"""
        print("Sending prompt to Gemini...")

        response = model.generate_content(prompt)
        print("Raw Gemini response:", response)

        if hasattr(response, 'text'):
            print("Summary received successfully.")
            return response.text
        else:
            print("No 'text' attribute in Gemini response.")
            return "Summary generation failed."

    except Exception as e:
        print("Gemini error:", e)
        return "Summary generation failed."
