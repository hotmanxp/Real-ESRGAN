import sys
import openai


openai.api_key = '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'

promote = sys.argv[1]


def ask(question: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0.3,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.8,
        best_of=1,
        max_tokens=1024)

    # print(response.choices[0].text)
    for res in response.choices:
        print(res.text)
        print('==========end=========')


if __name__ == '__main__':
    if promote:
        print('Waiting...')
        ask(promote)
