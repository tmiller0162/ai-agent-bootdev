import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": str(args.user_prompt),
        },
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if not response.usage or not response.choices[0]:
            return "Did not recieve response"
        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"User prompt: {args.user_prompt}")
        response_message = response.choices[0].message
        messages.append(response_message)
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("No content in function call return")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(response_message.content)
            return
    print("AI looped 20 times, exiting")
    exit(1)


if __name__ == "__main__":
    main()
