import re
import json
import requests
from bs4 import BeautifulSoup
from time import sleep

def parser():
    counter = -1
    with open("responses.json", "r") as json_file:
        data = json.load(json_file) # Prompted safeguard ontology + metrics.
    list_of_safeguards = []   
    for i in range(1,19):
        url = f"https://cas8.docs.cisecurity.org/en/latest/source/Controls{i}/#"

        sleep(0.2)
        response = requests.get(url)
        html_data = response.content

        soup = BeautifulSoup(html_data, 'html.parser')
        
        ul_tag = soup.find('ul', class_ = 'current').find('li', class_= 'toctree-l1 current').find_next('ul')
        
        toctree_list = ul_tag.find_all('li', class_ = 'toctree-l2', recursive=False)
        safeguards_count = len(toctree_list)

        # I found a typo in html in the toctree of Control 13.
        # Following code is for dealing with it.
        text_list = [li.get_text(strip=True) for li in toctree_list]
        prefix = str(i)
        not_matching = [item for item in text_list if not item.startswith(prefix)]
        if len(not_matching) != 0:
            safeguards_count = len(toctree_list)-len(not_matching)
        
        for j in range(0, safeguards_count):
            safeguard = {
            "Observable": None,
            "Class": None,
            "Class.explanation": None,
            "Evaluation_Method": None,
            "Evaluation_Method.explanation": None,
            "Inputs": [],
            "Operations": [],
            "Metric_as_text": [],
            "Metric": []
            }

            counter += 1
            # Fill out 4 first values in the safeguard dictionary.
            parse_json(data, counter, safeguard)

            # Inputs
            if j == 0:
                input_header = soup.find(id = "inputs")
            else:
                input_header = soup.find(id = f"inputs_{j}")

            input_ol_tag = input_header.find_next('ol')
            inputs = []
            for input_item in input_ol_tag.find_all('li'):
                inputs.append(input_item.text.replace("\n", ""))
            safeguard["Inputs"].append(inputs)

            # Operations
            if j == 0:
                op_header = soup.find(id = "operations")
            else:
                op_header = soup.find(id = f"operations_{j}")
            op_ol_tag = op_header.find_next('ol')
            #operations = []
            #for op_item in op_ol_tag.find_all('li'):
            #    operations.append(op_item.text.replace("\n", ""))
            #safeguard["Operations"].append(operations)
            
            nested_list = parse_list(op_ol_tag)
            safeguard["Operations"] = nested_list


            # Measures
            if j == 0:
                measure_header = soup.find(id = "measures")
            else:
                measure_header = soup.find(id = f"measures_{j}")
            
            # Check if there are measures left.
            if measure_header is None:
                continue 

            measure_ul_tag = measure_header.find_next('ul')
            measures = []
            for measure in measure_ul_tag.find_all('li'):
                measures.append(measure.text.replace("\n", ""))           

            # Metrics
            if j == 0:
                metrics_header = soup.find(id = "metrics")
            else:
                metrics_header = soup.find(id = f"metrics_{j}")

            next_state = metrics_header.find_next()
            if next_state.name == 'ul':
                metric_ul_tag = metrics_header.find_next('ul')
                soup_state = metric_ul_tag.find_next_sibling()
                               
                parse_metrics_as_text(safeguard, metric_ul_tag)

                if soup_state != None and (soup_state.name == 'div' or soup_state.name == 'h4' or soup_state.name == 'h3'):
                    soup_state = soup_state.find_next("table")
                else:
                    list_of_safeguards.append(safeguard)
                    continue

            if i == 18 and j==3:
                print()
            if next_state.name == 'table' or next_state.name == 'h4' or next_state.name == 'h3':
                soup_state = next_state           

            if metric_ul_tag != None:
                while True:               
                    metric_info = {
                    "definition": None,
                    #"inputs": [],
                    "measure.description": [],
                    "measure.id": [],
                    "equation": None
                    }
                    
                    if soup_state.name == 'h4' or soup_state.name == 'h3':
                        soup_state = soup_state.find_next('table')
                    
                    metric_info["definition"] = soup_state.find_next("th").find_next("th").text
                    soup_state = soup_state.find_next("td").find_next("td")
                    metric_info["equation"] = soup_state.text

                    metric_info["measure.id"] = re.findall(r'M\d+', metric_info["equation"])
                    for measure_id in metric_info["measure.id"]:
                        # Check if the element was already added to avoid adding the same one.
                        if measures[int(measure_id[1:])-1] not in metric_info["measure.description"]:
                            metric_info["measure.description"].append(measures[int(measure_id[1:])-1])               
                            measure = metric_info["measure.description"][-1]
                            #metric_info["inputs"].append(input_extractor(measure, inputs))
                    
                    safeguard["Metric"].append(metric_info)
                    list_of_safeguards.append(safeguard)

                    next_state = soup_state.find_next()
                    if next_state == 'table':
                        soup_state = next_state
                    else:
                        next_state = next_state.find_next()
                        if next_state.name != 'h4' or next_state.name != 'table' or next_state.name != 'h3' or next_state.text != "Procedural Review":
                            break
                        else:
                            soup_state = next_state

    with open("parsed_1.json", "w") as file:
        json.dump(list_of_safeguards, file)

# Parse inputs that are used in the equation.
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


def parse_json(data: json, object_number: int, safeguard: dict):
    obj = data[object_number]
    safeguard["Observable"] = obj["Observable"]
    safeguard["Class"] = obj["Class"]
    safeguard["Class.explanation"] = (
        obj["Class.explanation"] if "Class.explanation" in obj.keys() 
        else obj["Class"][0]["explanation"]
    )        
    safeguard["Evaluation_Method"] = obj["Evaluation_Method"]
    safeguard["Evaluation_Method.explanation"] = (
        obj["Evaluation_Method.explanation"] if "Evaluation_Method.explanation" in obj.keys()
        else obj["Evaluation_Method"][0]["explanation"]
    )

def parse_metrics_as_text(safeguard: dict, metric_ul_tag):
    metric_list = metric_ul_tag.find_all('li', recursive=False)
    text_list = [li.get_text(strip=True) for li in metric_list]
    safeguard["Metric_as_text"].append(text_list)

# Functions for parsing Operations as a nested list.
def extract_text(tag):
    return ''.join(
        child.get_text() if hasattr(child, 'get_text') else str(child)
        for child in tag.contents
    ).strip()

def parse_list(ol):
    result = []
    for li in ol.find_all('li', recursive=False):
        text_node = li.find('p') or li
        text = extract_text(text_node)

        nested_ol = li.find('ol')
        if nested_ol:
            result.append([text, parse_list(nested_ol)])
        else:
            result.append(text)
    return result

parser()