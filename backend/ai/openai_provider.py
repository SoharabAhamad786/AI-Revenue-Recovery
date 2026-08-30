"""OpenAI provider for RecoverAI."""
import json
import os
from .base import SYSTEM_PROMPT


class OpenAIProvider:
    """Real AI provider using OpenAI API."""

    MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    def analyze(self, context: dict) -> dict:
        """Call OpenAI API for invoice analysis."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            user_prompt = f"Analyze the following invoice and customer data, then provide your recovery recommendation:\n\n{json.dumps(context, indent=2)}"

            response = client.chat.completions.create(
                model=self.MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
