import os
import openai

openai.api_key = os.environ['OPEN_AI_KEY']


def ask():
    next_answer = input('我: ')
    print('Waiting...')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=next_answer,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0.5,
        max_tokens=1024,
        stop=None)

    print('GPT：')
    # print(response)
    for res in response.choices:
        print(res.text)
    print('End...')

    ask()


if __name__ == '__main__':
    ask()
