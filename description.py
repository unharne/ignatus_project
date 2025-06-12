from data import *
from constructor import constructor
import random

def edit_text(s :dict):
    lst = []
    
    for i in s.values():
            if i.startswith("!"):
                y = i.split("!")[1]
                lst.append(y)
            else:
                lst.append(i)
    return lst

def generate_description(result) -> str:
    name = random.choice(names)

    s = result["random_symptoms"]
    all_symptoms = []

    all_symptoms = edit_text(s)

    descriptions = []
    for symptom,description in symptoms_description.items():
        if symptom in all_symptoms:
            descriptions.append(description)

    if len(all_symptoms) > 3:
        state = "достаточно печально"
    elif len(all_symptoms) == 0:
        state = "хорошо"
    else:
        state = "плохо"     

    if len(all_symptoms) == 0:
        description = f"{name} чувствует себя {state}.Идеально здоров..."
    else:
        description = f"{name} чувствует себя {state}.У него {", ".join(descriptions)}..."

    return description
