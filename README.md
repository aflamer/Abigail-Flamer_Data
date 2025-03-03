# Data-Eng_challenge

### The actual instructions are in the challenge.py


### Also please download the repo and work on it offline so that other candidates do not see your work.


### Please check the original email for instructions about how to submit your finished code


### Changes/added features: I first included my get_code_description() and solution() functions, which satisfy the basic requirements for the Data-Eng challenge. This way, it can be seen that the output of my solution function exactly matches the expected output. I did change the solution function to allow for the output list to be sorted by "patient_id," "diagnoses," "malformed_diagnoses," or "priority_diagnoses" (the default). If a user tries to sort on anything other than these four, the output will just be sorted by priority_diagnoses. I then added two additional functions, called add_diagnoses() and cured(). The former allows an inputted ICD-10 code to be added to a specified patient's list of diagnoses in patient_data (or patient_data2, which I created so that I could test these extra functions without altering the original patient_data). If the specified patient does not exist in patient_data, they are added to the list of dictionaries and the ICD-10 code is included in their list of diagnoses. The latter function, cured(), removes the inputted ICD-10 code from a patient's diagnoses list in patient_data and adds it to a new resolved_diagnoses list, given that the the ICD-10 code exists in the patient's diagnoses list and is not a malformed diagnosis. I then added a color_coded_table() function, which returns a table with columns "Patient ID," "ICD-10 Codes," and "Diagnoses." In the table, priority, non-priority, malformed, and resolved diagnoses are color-coded for ease of distinction. Users can change which diagnoses they want to be included in the table, what colors they want for each type of diagnosis, how to sort the table, and whether they want to see data for all patients or just one specific patient. My solution2() function is very similar to the original solution() function, but each patient dictionary in the output includes a list of resolved diagnoses, and the output list can be sorted by number of resolved diagnoses. 

## I spent around 11 hours on this project. 
