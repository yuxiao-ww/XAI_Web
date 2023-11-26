import openai


# openai.api_key = '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'
openai.api_key = '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'

prefix = "convert those into natural language paragraph orderly. /n/n" \
         'Method: /n' \
         'make each line as an explanation, discard the time step(0,1,2,3...). /n' \
         'When there are three elements in a line like "[A,B,C]" which is a clause in CNF format, ' \
         'which means "A or B or C". /n' \
         'When there is a group of some three-part lines with same elements, then group ' \
         'them into one line, which means you only need to translate one of them. /n ' \
         'And every item had a time step, you should regard those items with the largest number of time step as goals. /n' \
         'Here is an example (in this example, the goals are those items with time step 4): /n' \
         "['on(B, A)_0'] /n" \
         "['on(B, A)_0', 'on(B, A)_1', 'stack_B_A_0'] /n" \
         "['on(B, A)_1', 'on(B, A)_2', 'stack_B_A_1'] /n" \
         "['on(B, A)_2', 'on(B, A)_3', 'stack_B_A_2'] /n" \
         "['on(C, B)_0']' /n" \
         "['on(C, B)_0', 'on(C, B)_1', 'stack_C_B_0'] /n" \
         "['on(C, B)_1', 'on(C, B)_2', 'stack_C_B_1'] /n" \
         "['on(C, B)_2', 'on(C, B)_3', 'stack_C_B_2'] /n" \
         "['on(C, B)_3', 'on(C, B)_4', 'stack_C_B_3'] /n" \
         "['on(B, A)_3', 'on(B, A)_4', 'stack_B_A_3'] /n" \
         "['on(B, A)_4'] /n" \
         "['on(C, B)_4'] /n" \
         'Give me the results like this (in one paragraph WITHOUT other explanations) but summarize it and make it readable: /n' \
         'At first, block c is on block b and block b is on block a. And since you are stacking block b on ' \
         'block a, so block b is not on the block a right now, but block b will be on block a in next step. ' \
         'When you are stacking block c on block b, so block b is not on the block a right now, but block b will ' \
         'be on block a in next step. Then, block c is on block b. When you are stacking block b on block a,' \
         'so block b is not on the block a right now, but block b will be on block a in next step.' \
         'And finally, block b is on block a. /n'

query = 'Now do the same in the given order for the following plan: /n' \
        'Give me only the result WITHOUT any explanation. /n'


def completion_func_gpt(content):
    prompt = prefix + content
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message


gpt = completion_func_gpt('')
output = gpt['content']
