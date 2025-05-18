from openai import OpenAI

with open("api_key.txt") as file:
    key = file.read()

systemPrompt = """{Observable: what object will be seen in the system if the safeguard is enforced or not enforced

Class: Checklist or verifiable or Measurable (A safeguard can belong to multiple classes). A checklist class means we can assess the safeguard through scripting, A verifiable class means we can verify the safeguard by checking system configuration, and A measurable class means we have to use data-driven analytics to assess the safeguard. You must also give the explanation for why you think a safeguard belongs to the detected class.

Evaluation_Method: Data-driven or  Model-based or Active testing (A safeguard can be evaluated using multiple evaluation methods). A Data-driven evaluation method indicates that we have to generate statistics from event logs, traffic flows, and user activities to evaluate the enforcement of the safeguard; A model-based evaluation approach indicates that we have to use the configuration of the system to evaluate the enforcement of the safeguard; A active testing evaluation method indicates that we have to probe the system to evaluate the enforcement of the safeguard. You must also explain why you think a safeguard can be assessed using the detected evaluation method.

Measure: What is to be measured to assess the safeguard? One or multiple measures are used to generate metric.

Metric: A metric for a security control safeguard defines how to assess corresponding security control safeguard. Each metric is the combination of multiple measures. We may need multiple metrics to assess multiple aspects of enforcement quality for a specific safeguard.}

Question: 
For the following security control safeguard description enclosed in the curly braces, extract the following information: observable, class, evaluation_method, measure and metric.
Safeguard: {Use a passive discovery tool to identify assets connected to the enterprise’s network. Review and use scans to update the enterprise’s asset inventory at least weekly or more frequently.}

Answer: 
Thought 1: If this safeguard is implemented, we will see the passive discovery tool’s scan result. Thus, we can measure the following things-
Measures:
M1 = Count of properly configured passive asset discovery tools
M2 = Count of improperly configured passive asset discovery tools
M3 = Count of organization’s networks that are covered by properly configured passive discovery tools
M4 = Count of organization’s networks that are not covered by properly configured passive discovery tools
M5 = Count of enterprise networks.
M6 = last scan time
M7 = 2nd last scan time
M8 = Time when asset inventory is updated

Thought 2: To assess the enforcement quality of the above-mentioned safeguard, we have to measure coverage, configuration compliance quality, scan rate and asset inventory update rate. To calculate the coverage score, you can combine measure  M3 and M4; to calculate the Configuration compliance quality, you can combine measure  M1 and M2; To calculate scan rate, we can use measure M6 and M7; To calculate Asset inventory update rate, we can use measure M8 and M6.

Metrics:
Coverage = M3 / (M3 + M4)
Configuration compliance quality = M1/(M1 + M2) 
Scan rate = time difference between two consecutive scan = M6 - M7
Assent inventory update rate (freshness) =  1/ (the time when asset inventory is updated - last scan time) = 1 / (M8 - M6)"""


question = """Now, For the following security control safeguard description enclosed in the curly braces, extract the following information: observable, class, evaluation_method, measure and metric.
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
Metric.equation

{Safeguard NIST CSF PR.AC-1: Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes}"""


client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": question},
    ],
    stream=False
)

print(response.choices[0].message.content)