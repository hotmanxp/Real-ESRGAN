import sys
import os
import openai

openai.api_key = os.environ['OPEN_AI_KEY']
prompt = sys.argv[1]


def ask(question: str):
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=question, temperature=0.3, top_p=1, frequency_penalty=0.5, max_tokens=1024)

    for res in response.choices:
        print(res.text)
        print('==========end=========')


if __name__ == '__main__':
    print('Waiting...')
    ask(prompt)
