import os
from src.openaibot.openai_bot import OpenAIBot
# https://medium.com/@kaljessy/chating-with-openai-using-python-3ae5a14b4501

def my_callback(response):
    print("Received response:", response)

def run_bot():
    import asyncio
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key is None:
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)

    openai_bot = OpenAIBot(openai_key)
    while True:
        user_input = input("Enter your question:")
        if user_input == "exit":
            break
        asyncio.run(openai_bot.get_response(user_input, my_callback))


if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(e)










