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
    name = result.get("name", "Пациент")
    gender = result.get("gender", "мужчина")
    s = result["random_symptoms"]
    all_symptoms = edit_text(s)
    descriptions = []
    for symptom, description_text in symptoms_description.items():
        if symptom in all_symptoms:
            descriptions.append(description_text)

    if len(all_symptoms) > 3:
        state = "достаточно печально"
    elif len(all_symptoms) == 0:
        state = "хорошо"
    else:
        state = "плохо"

    # Родовая формулировка
    if gender == "женщина":
        pronoun = "у неё"
        feels = "чувствует себя"
    else:
        pronoun = "у него"
        feels = "чувствует себя"

    if len(all_symptoms) == 0:
        description = f"{name} {feels} {state}. Идеально здорова..." if gender == "женщина" else f"{name} {feels} {state}. Идеально здоров..."
    else:
        description = f"{name} {feels} {state}. {pronoun} {', '.join(descriptions)}..."

    return description
