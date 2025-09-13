from openai import OpenAI
import pandas as pd
import json

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


with open("api_key.txt") as file:
    key = file.read()

with open("evaluation-prompt.txt") as file:
    systemPrompt = file.read()

golden_dataset = pd.read_json("parsed.json")
generated_dataset = pd.read_json("responses.json")
safeguards = pd.read_csv("Standards.csv")
safeguards_number = len(golden_dataset)
responses = []
i = 0
while i < safeguards_number:
    safeguard = safeguards.loc[i]
    question = (
        f"{{Context: {safeguard["Description"]}\n LLM-Generated: {generated_dataset.loc[i]}\n Golden dataset: {golden_dataset.loc[i]}\n}}"
    )
    question += (
        """Format the output with the following JSON keys:
            Criteria.name
            Criteria.score
            Criteria.explanation"""
    )
    try:
        print(i)
        responses.append(cot_prompt(systemPrompt, question))
        i += 1
    except:
        pass
    with open("evaluation.json", "w") as file:
        json.dump(responses, file)