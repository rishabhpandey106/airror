import os
import json
from dotenv import load_dotenv

from llm.prompts import DEBUG_PROMPT

load_dotenv()


class LLMExplainer:

    def __init__(self, provider="gemini"):
        self.provider = provider

        if provider == "gemini":
            from google import genai

            api_key = os.getenv("GEMINI_API_KEY")
            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.5-flash"

        elif provider == "groq":
            from groq import Groq

            api_key = os.getenv("GROQ_API_KEY")
            self.client = Groq(api_key=api_key)
            self.model = "llama3-8b-8192"

    def format_code_snippets(self, snippets):
        """
        Convert search results into readable text for the prompt.
        """

        formatted = []

        for s in snippets:
            block = f"""
File: {s['file_path']}
Function: {s['function_name']}
Line: {s['line_number']}

{s['code_snippet']}
"""
            formatted.append(block)

        return "\n\n".join(formatted)

    def explain(self, error: str, snippets: list):

        code_context = self.format_code_snippets(snippets)

        prompt = DEBUG_PROMPT.format(
            error=error,
            code=code_context
        )

        if self.provider == "gemini":
            return self._gemini_call(prompt)

        if self.provider == "groq":
            return self._groq_call(prompt)

    def _gemini_call(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        text = response.text

        # try:
        #     return json.loads(text)
        # except:
        #     return {
        #         "explanation": text,
        #         "suggested_fix": ""
        #     }
        try:
            # Quick tip: Sometimes LLMs wrap JSON in markdown blockquotes like ```json ... ```
            # Stripping them helps prevent json.loads from crashing
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
            
        except json.JSONDecodeError:
            return {
                "explanation": text,
                "suggested_fix": ""
            }

    def _groq_call(self, prompt):

        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content

        try:
            return json.loads(text)
        except:
            return {
                "explanation": text,
                "suggested_fix": ""
            }