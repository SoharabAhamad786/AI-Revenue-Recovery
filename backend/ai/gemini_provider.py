"""Google Gemini provider for RecoverAI."""
import json
import os
from .base import SYSTEM_PROMPT


class GeminiProvider:
    """Real AI provider using Google Gemini API."""

    MODEL_NAME = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')

    def analyze(self, context: dict) -> dict:
        """Call Gemini API for invoice analysis."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

            model = genai.GenerativeModel(
                self.MODEL_NAME,
                system_instruction=SYSTEM_PROMPT,
            )

            user_prompt = f"Analyze the following invoice and customer data, then provide your recovery recommendation as valid JSON:\n\n{json.dumps(context, indent=2)}"

            response = model.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    response_mime_type="application/json",
                ),
            )

            result = json.loads(response.text)
            return result
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
