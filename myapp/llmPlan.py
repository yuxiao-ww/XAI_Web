import openai
import os


openai.api_key = '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'
# openai.api_key = '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'

prefix = 'I am solving the planning problem. /n' \
         'I will give you some english sentences and you should extract the keywords in the english sentences, ' \
         'convert them into the format I provide, and then tag them with time steps. /n' \
         'Here is an example: /n' \
         'My plan is I first unstack the block A from the block B, then I put the block A down, ' \
         'and I pick the block B up, in the end i stack the block B on the block A. /n' \
         'Give me the results like this (in one line WITHOUT other explanations): /n' \
         "unstack_A_B_0, putdown_A_1, pickup_B_2, stack_B_A_3" \
         'Remember tag each of them with number which means the time step. /n'

query = 'Now do the same and add the time steps in the given order for the following plan: /n' \
        'Give me only the resulting indexed plan. /n'


def completion_func_gpt(content):
    prompt = prefix + content
    completion = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message


gpt = completion_func_gpt('I want to put the block A down, and pick the block B up, then I will stack the block B on the block A')
output = gpt['content']
# print(output)
