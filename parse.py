import re
import json
import requests
from bs4 import BeautifulSoup

def parser():
    list_of_metric_info = []
    for i in range(1,18):
        url = f"https://cas8.docs.cisecurity.org/en/latest/source/Controls{i}/#"

        response = requests.get(url)
        html_data = response.content

        soup = BeautifulSoup(html_data, 'html.parser')
        
        ul_tag = soup.find('ul', class_ = 'current').find('li', class_= 'toctree-l1 current').find_next('ul')
        
        safeguards_count = len(ul_tag.find_all('li', class_ = 'toctree-l2', recursive=False))

        for j in range(0, safeguards_count):
            # Measures
            if j == 0:
                measure_header = soup.find(id = "measures")
            else:
                measure_header = soup.find(id = f"measures_{j-1}")
            
            # Check if there are measures left
            if measure_header is None:
                break

            measure_ul_tag = measure_header.find_next('ul')
            measures = []
            for measure in measure_ul_tag.find_all('li'):
                measures.append(measure.text.replace("\n", ""))

            # Inputs
            if j == 0:
                input_header = soup.find(id = "inputs")
            else:
                input_header = soup.find(id = f"inputs_{j-1}")

            input_ol_tag = input_header.find_next('ol')
            inputs = []
            for input_item in input_ol_tag.find_all('li'):
                inputs.append(input_item.text.replace("\n", ""))

            # Metrics
            if j == 0:
                metrics_header = soup.find(id = "metrics")
            else:
                metrics_header = soup.find(id = f"metrics_{j-1}")

            metric_ul_tag = metrics_header.find_next('ul')
            metrics = []
            for metric in metric_ul_tag.find_all('li'):
                metrics.append(metric.text)
                        
            soup_state = metric_ul_tag
            for _ in range(0, len(metrics)):
                metric_info = {
                "definition": None,
                "inputs": [],
                "measure.description": [],
                "measure.id": [],
                "equation": None
                }

                soup_state = soup_state.find_next("table")
                metric_info["definition"] = soup_state.find_next("th").find_next("th").text
                soup_state = soup_state.find_next("td").find_next("td")
                metric_info["equation"] = soup_state.text

                metric_info["measure.id"] = re.findall(r'M\d+', metric_info["equation"])
                for measure_id in metric_info["measure.id"]:
                    # Check if the element was already added to avoid adding the same one.
                    if measures[int(measure_id[1:])-1] not in metric_info["measure.description"]:
                        metric_info["measure.description"].append(measures[int(measure_id[1:])-1])               
                        measure = metric_info["measure.description"][-1]
                        metric_info["inputs"].append(input_extractor(measure, inputs))

                list_of_metric_info.append(metric_info)

    with open("parsed.json", "w") as file:
        json.dump(list_of_metric_info, file)


def input_extractor(measure: str, inputs: list) -> list:
    metric_info_inputs = []
    pattern = r'(GV\d+|Input \d+)'
    matches = re.findall(pattern, measure)
    if matches != None:
        for input in matches:
            if "GV" in input:
                for item in inputs:
                    if input in item:
                        metric_info_inputs.append(item)
                        break
            else:
                ind = int(input[6:])-1
                metric_info_inputs.append(inputs[ind])
    return metric_info_inputs

parser()