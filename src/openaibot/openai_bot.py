import openai
from openai import AsyncOpenAI
from typing import Callable, Any
class OpenAIBot:

    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key = api_key)

    async def get_response(self, prompt:str, callback: Callable[[Any], None], model: str = "gpt-3.5-turbo"):
        try:

            response = await  self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user","content": prompt},
                {"role": "system","content": "You are a helpful assistant that provides concise and accurate information." }]
            )

            callback(response.choices[0].message.content.strip())

        except openai.RateLimitError as e:
            raise Exception(f"Rate limit exceeded. Please try again later. {e}");
        except openai.AuthenticationError as e :
            raise Exception(f"Authentication failed. Please check your API key. {e}");
        except openai.OpenAIError as e:
            raise Exception(f"An error occurred:. {e}");
