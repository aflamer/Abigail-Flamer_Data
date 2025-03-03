# Welcome!
#
# Your task is to use the NIH ICD-10 API to create a function that transforms raw patient data into a more human readable format. 
# You will do this by filling out the TODO stub in the function description. the filled out solution function, when given patient_data, should 
# return an output identical to expected_output (non-trivially, that is, through a series of transformations using the api and the provided 
# priority diagnosis substrings)

#   In brief, the motivation is that you will:
#  1) make the patient data human readable by including each code's description using the API
#  2) identify malformed codes (codes that are not valid ICD-10)
#  3) flag patients that have codes where the description contains "covid" or "respiratory failure" as priority_diagnoses
#
# output:
# The expected output is a list containing elements of the following format.
# It should be sorted in descending order based on the number of 'priority_diagnoses'.
#
# {'id': 0,
#  'diagnoses': [
#      ('U07.1', 'COVID-19'),
#      ('N18.30', 'Chronic kidney disease, stage 3 unspecified')]
#  'priority_diagnoses': ['COVID-19'],
#  'malformed_diagnoses': []
# 
# API docs: https://clinicaltables.nlm.nih.gov/apidoc/icd10cm/v3/doc.html

import requests
from tabulate import tabulate
from termcolor import colored

base_url = ("https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
            "?sf={search_fields}&terms={search_term}&maxList={max_list}")

# used for basic implementation
patient_data = [
    {"patient_id": 0,
     "diagnoses": ["I10", "K21.9"]},
    {"patient_id": 1,
     "diagnoses": ["E78.5", "ABC.123", "U07.1", "J96.00"]},
    {"patient_id": 2,
     "diagnoses": []},
    {"patient_id": 3,
     "diagnoses": ["U07.1", "N18.30"]},
    {"patient_id": 4,
     "diagnoses": ["I10", "E66.9", "745.902"]},
    {"patient_id": 5,
     "diagnoses": ["G47.33", "I73.9", "N18.30", 1]}
]

# used for more advanced implementation
patient_data2 = [
    {"patient_id": 0,
     "diagnoses": ["I10", "K21.9"]},
    {"patient_id": 1,
     "diagnoses": ["E78.5", "ABC.123", "U07.1", "J96.00"]},
    {"patient_id": 2,
     "diagnoses": []},
    {"patient_id": 3,
     "diagnoses": ["U07.1", "N18.30"]},
    {"patient_id": 4,
     "diagnoses": ["I10", "E66.9", "745.902"]},
    {"patient_id": 5,
     "diagnoses": ["G47.33", "I73.9", "N18.30", 1]}
]

def get_code_description(search_term, search_fields="code", max_list=1):
    'Returns the description of a code if it is a valid ICD-10 and None otherwise'

    url = base_url.format(search_fields=search_fields, search_term=search_term, max_list=max_list)
    
    response = requests.get(url)
 
    if response.status_code == 200:
        code_data = response.json()
        # print(f"API Response for {search_term}: {code_data}")

        # if the number of search results is greater than 0, return the code description
        if code_data[0] > 0:  
            return code_data[3][0][1]
    
    return None

#print(get_code_description("I10"))

def solution(data, sort_by="priority_diagnoses", desc=True):
    ... # TODO: transform the input into a more readable format that looks like expected_output
    priority_descriptions = ["covid", "respiratory failure"]

    patient_data = []

    for patient in data:
        patient_id = patient["patient_id"]
        diagnoses = patient["diagnoses"]
        priority_diagnoses = []
        valid_diagnoses = []
        malformed_diagnoses = []

        for code in diagnoses: 
            code_description = get_code_description(code)

            # if the code is valid ICD-10, add the description to priority_diagnoses
            if code_description: 
                valid_diagnoses.append((code, code_description))

            # if the description includes "covid" or "respiratory failure", add the description to priority_diagnoses
                if any(word in code_description.lower() for word in priority_descriptions):
                    priority_diagnoses.append(code_description)

            # if the code is not valid ICD-10, add the code to malformed_diagnoses
            else: 
                malformed_diagnoses.append(code)

        # create a patient entry 
        patient_entry = {
            'patient_id': patient_id,
            'diagnoses': valid_diagnoses,
            'priority_diagnoses': priority_diagnoses,
            'malformed_diagnoses': malformed_diagnoses
        }

        # add the patient entry to patient_data
        patient_data.append(patient_entry)

    # sort patient_data based on the value of sort and desc input values

    if sort_by in ["patient_id", "diagnoses", "malformed_diagnoses", "priority_diagnoses"]:
        if sort_by != "patient_id":
            patient_data.sort(key=lambda patient: len(patient[sort_by]), reverse=desc)
        else:
            patient_data.sort(key=lambda patient: patient["patient_id"], reverse=desc)

    else:
        patient_data.sort(key=lambda patient: len(patient["priority_diagnoses"]), reverse=desc)

    return patient_data


# print(solution(patient_data, sort_by="patient_id"))



output = solution(patient_data)

expected_output = [
        {'patient_id': 1,
         'diagnoses': [
             ('E78.5', 'Hyperlipidemia, unspecified'),
             ('U07.1', 'COVID-19'),
             ('J96.00', 'Acute respiratory failure, unspecified whether with hypoxia or hypercapnia')],
         'priority_diagnoses': [
             'COVID-19', 'Acute respiratory failure, unspecified whether with hypoxia or hypercapnia'],
         'malformed_diagnoses': ['ABC.123']
        },
        {'patient_id': 3,
         'diagnoses': [
             ('U07.1', 'COVID-19'),
             ('N18.30', 'Chronic kidney disease, stage 3 unspecified')],
         'priority_diagnoses': ['COVID-19'],
         'malformed_diagnoses': []
        },
        {'patient_id': 0,
         'diagnoses': [
             ('I10', 'Essential (primary) hypertension'),
             ('K21.9', 'Gastro-esophageal reflux disease without esophagitis')],
         'priority_diagnoses': [],
         'malformed_diagnoses': []
        },
        {'patient_id': 2, 'diagnoses': [],
         'priority_diagnoses': [],
         'malformed_diagnoses': []
        },
        {'patient_id': 4,
         'diagnoses': [
             ('I10', 'Essential (primary) hypertension'),
             ('E66.9', 'Obesity, unspecified')],
         'priority_diagnoses': [],
         'malformed_diagnoses': ['745.902']
        },
        {'patient_id': 5,
         'diagnoses': [
             ('G47.33', 'Obstructive sleep apnea (adult) (pediatric)'),
             ('I73.9', 'Peripheral vascular disease, unspecified'),
             ('N18.30', 'Chronic kidney disease, stage 3 unspecified')],
         'priority_diagnoses': [],
         'malformed_diagnoses': [1]
        }
    ]
try:
    assert(output == expected_output)
except AssertionError:
    print('error: your output does not match the expected output')
else:
    print('success!')





# more advanced implementation (added features)

def solution2(data, sort_by="priority_diagnoses", desc=True):
    '''Transforms the input into a more readable format that looks similar to expected_output, with the addition of a 
    resolved_diagnoses list for each patient'''
    priority_descriptions = ["covid", "respiratory failure"]

    patient_data = []

    # ensure all patients have a "resolved_diagnoses" list
    for patient in data:
        if "resolved_diagnoses" not in patient:
            patient["resolved_diagnoses"] = []

    for patient in data:
        patient_id = patient["patient_id"]
        diagnoses = patient["diagnoses"]
        priority_diagnoses = []
        valid_diagnoses = []
        malformed_diagnoses = []
        resolved_codes = patient["resolved_diagnoses"]
        resolved_diagnoses = []

        for code in diagnoses: 
            code_description = get_code_description(code)

            # if the code is valid ICD-10, add the description to valid_diagnoses
            if code_description: 
                valid_diagnoses.append((code, code_description))

            # if the description includes "covid" or "respiratory failure", add the description to priority_diagnoses
                if any(word in code_description.lower() for word in priority_descriptions):
                    priority_diagnoses.append(code_description)

            # if the code is not valid ICD-10, add the code to malformed_diagnoses
            else: 
                malformed_diagnoses.append(code)

        for code in resolved_codes:
            resolved_diagnoses.append((code, get_code_description(code)))

        # create a patient entry 
        patient_entry = {
            'patient_id': patient_id,
            'diagnoses': valid_diagnoses,
            'priority_diagnoses': priority_diagnoses,
            'malformed_diagnoses': malformed_diagnoses,
            'resolved_diagnoses': resolved_diagnoses
        }

        # add the patient entry to patient_data
        patient_data.append(patient_entry)

    # sort patient_data based on the value of sort and desc input values
    if sort_by in ["patient_id", "diagnoses", "malformed_diagnoses", "priority_diagnoses", "resolved_diagnoses"]:
        if sort_by != "patient_id":
            patient_data.sort(key=lambda patient: len(patient[sort_by]), reverse=desc)
        else:
            patient_data.sort(key=lambda patient: patient["patient_id"], reverse=desc)

    else:
        patient_data.sort(key=lambda patient: len(patient["priority_diagnoses"]), reverse=desc)

    return patient_data

def color_coded_table(patient_data, 
                      priority=True, priority_color='red', 
                      non_priority=True,  non_priority_color='yellow', 
                      malformed=True, malformed_color='magenta', 
                      resolved=True, resolved_color='green',
                      sort="priority_diagnoses", 
                      one_patient=False, patient_id=None):
    
    '''Creates a table using patient data and color codes the different types of diagnoses (priority, non-priority, malformed, and resolved). 
    User can change which diagnoses they want to include, what colors they want, how to sort the table, and whether they want 
    to see data for all patients or just one specific patient.'''

    if not priority and not non_priority and not malformed and not resolved:
        return("No data to organize")

    for patient in patient_data:
        if "resolved_diagnoses" not in patient:
            patient["resolved_diagnoses"] = []

        try:
            table_data = []

            patients = solution2(patient_data, sort_by=sort)
            if one_patient:
                patients = [p for p in patients if p["patient_id"] == patient_id]

            for patient in patients:
                patient_id = patient['patient_id']
                diagnoses = patient['diagnoses']
                priority_diagnoses = patient['priority_diagnoses']
                malformed_diagnoses = patient['malformed_diagnoses']
                resolved_diagnoses = patient['resolved_diagnoses']
                
                # Color code: red for priority diagnoses, green for non-priority valid diagnoses, magenta for malformed ICD-10 codes
                colored_codes = []
                colored_diagnoses = []
            
                for code, description in diagnoses:
                    if description in priority_diagnoses and priority:
                            colored_codes.append(colored(f"{code}", f'{priority_color}'))
                            colored_diagnoses.append(colored(f"{description}", f'{priority_color}'))

                    else:
                        if non_priority:
                            colored_codes.append(colored(f"{code}", f'{non_priority_color}'))
                            colored_diagnoses.append(colored(f"{description}", f'{non_priority_color}'))
    
                for code in malformed_diagnoses:
                    if malformed: 
                        colored_codes.append(colored(f"{code}", f'{malformed_color}'))
                        colored_diagnoses.append(colored("Diagnosis unavailable", f'{malformed_color}'))

                for code, description in resolved_diagnoses:
                    if resolved:
                        colored_codes.append(colored(f"{code}", f'{resolved_color}'))
                        colored_diagnoses.append(colored(f"{description}", f'{resolved_color}'))

                table_data.append([patient_id, '\n'.join(colored_codes), '\n'.join(colored_diagnoses)])

            # Display table using tabulate 
            headers = ["Patient ID", "ICD-10 Codes", "Diagnoses"]
            return(tabulate(table_data, headers=headers, tablefmt='simple'))  

        except Exception as e:
            return(f"Input data formatted incorrectly: {e}")
        

#print(color_coded_table(patient_data2, priority_color="blue"))
#print(color_coded_table(patient_data2, priority=False,non_priority=False, malformed=False, resolved=False))
#print(color_coded_table(patient_data2, priority=False,non_priority=False, sort="resolved_diagnoses"))


def add_diagnoses(patient_data, patient_id, code): 
    '''If a patient with the given patient_id already exists in patient_data, adds the inputted ICD-10 code to their list of diagnoses. 
    If the given patient is not in patient_data, creates a new entry with their patient_id and the given ICD-10 code'''
    for patient in patient_data: 
        if patient["patient_id"] == patient_id:
            if code not in patient["diagnoses"]:
                patient["diagnoses"].append(code)
            return patient_data 
        
    patient_entry = {"patient_id": patient_id, 
                     "diagnoses": [code]}
    
    patient_data.append(patient_entry)

    return patient_data

#print(add_diagnoses(patient_data2, 7, 'I95'))
#print(add_diagnoses(patient_data2, 2, 'K21.9'))
#print(patient_data2)
#print(solution(patient_data2))


def cured(patient_data, patient_id, code):
    "Removes the inputted ICD-10 code from a patient's diagnoses list in patient_data and adds it to a new resolved_diagnoses list"
    # ensure all patients in patient_data have a resolved_diagnoses list 
    for patient in patient_data:  
        if "resolved_diagnoses" not in patient:
            patient["resolved_diagnoses"] = []

        if patient["patient_id"] == patient_id:
            for diagnosis in patient["diagnoses"][:]:
                # Check if the diagnosis code matches and is not in malformed_diagnoses
                if diagnosis == code and get_code_description(code):
                    # Remove the diagnosis from the patient's diagnoses list
                    patient["diagnoses"].remove(diagnosis)
                    # Add the diagnosis to the patient's resolved_diagnoses list
                    patient["resolved_diagnoses"].append(diagnosis)

                    # Return updated data
                    return patient_data  

    # If the code or patient is not found, print an invalid entry message
    print("Invalid code or patient entry")
    return patient_data

#print(cured(patient_data2, 1, "E78.5"))
#print(cured(patient_data2, 5, "1"))
#print(patient_data2)



#print(cured(patient_data2, 1, "E78.5"))
#print(solution2(patient_data2))
#print(add_diagnoses(patient_data2, 5, "35"))

#print(color_coded_table(patient_data2, one_patient=True, patient_id=1))
#print(color_coded_table(patient_data2, malformed_color="scsdv"))

#add_diagnoses(patient_data2, 4, "I10")
#add_diagnoses(patient_data2, 4, "E78.5")
#cured(patient_data2, 4, "I10")
#print(color_coded_table(patient_data2))
#print(solution2(patient_data2))

#rint(color_coded_table(patient_data, malformed=False))
#print(color_coded_table(patient_data, sort="patient_id"))
#print(color_coded_table(patient_data, sort="fev"))
