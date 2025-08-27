from openai import OpenAI
import pandas as pd
import json

questionContext = """Now, For the following security control safeguard asset class, security function and description enclosed in the curly braces, extract the following information: observable, class, evaluation_method, measure and metric.
You should provide a comprehensive list of metrics and measures to assess the enforcement quality of the below security control safeguard. Format the output as JSON with the following keys:

Observable
Class
Class.explanation
Evaluation_Method
Evaluation_Method.explanation
Metric
Metric.defination
Metric.measure.description
Metric.measure.id
Metric.equation"""

safeguards = pd.read_csv("Standards.csv")

with open("api_key.txt") as file:
    key = file.read()

with open("fewshot-cot-prompting.txt") as file:
    systemPrompt = file.read()

# Connect with deepseek-r1
def cot_prompt(prompt: str, question: str) -> dict:
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": question},
        ],
        stream=False,
        response_format={
        'type': 'json_object'
        }
    )

    json_response = json.loads(response.choices[0].message.content)
    print(json_response)
    return json_response

responses = []
i = 0
length=len(safeguards)
while i < length:
    safeguard = safeguards.loc[i]
    question = questionContext + f"\n\n{{Asset Class: {safeguard["Asset Class"]}\n, Security Function: {safeguard["Security Function"]}\n, Safeguard: {safeguard["Description"]}}}"
    try:
        responses.append(cot_prompt(systemPrompt, question))
        i += 1
    except:
        pass

with open("responses.json", "w") as file:
    json.dump(responses, file)