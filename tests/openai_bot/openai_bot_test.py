import os

from src.openai.async_openai_bot import AsyncOpenAIBot
from src.openai.openai_bot import OpenAIBot


# https://medium.com/@kaljessy/chating-with-openai-using-python-3ae5a14b4501

def my_callback(response):
    print("OpenAISync response:", response)


def run_bot_async():
    import asyncio
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = AsyncOpenAIBot(openai_key)
    while True:
        user_input = input("Enter your question:").lower()
        if user_input == "exit":
            break
        asyncio.run(openai_bot.get_response_async(user_input, my_callback))


def run_bot():
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = OpenAIBot(openai_key)
    response = openai_bot.get_response("1+1?")
    print("OpenAI Response:", response)


if __name__ == "__main__":
    try:
        run_bot_async()
        # run_bot()
    except Exception as e:
        print(e)
