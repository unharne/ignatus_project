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

def generate_description(result):
    name = result["name"]
    gender = result["gender"]
    
    # Собираем все симптомы по категориям
    physical_symptoms = []
    movement_symptoms = []
    mental_symptoms = []
    actual_symptoms = []  # Список реальных симптомов для проверки
    
    for part in ["head", "arms", "body", "legs"]:
        if result["health"][part] == "Больная":
            part_symptoms = [s for s in symptoms[part] if s.startswith("!")]
            if part_symptoms:
                symptom = random.choice(part_symptoms)
                symptom_name = symptom.split("!")[1]
                actual_symptoms.append(symptom_name)  # Добавляем симптом в список реальных
                
                # Определяем категорию симптома
                if any(keyword in symptom.lower() for keyword in ["движение", "походка", "шаги", "дрожащие", "судорожные"]):
                    movement_symptoms.append(symptom)
                elif any(keyword in symptom.lower() for keyword in ["взгляд", "смех", "голос", "пение", "рычание", "шипение"]):
                    mental_symptoms.append(symptom)
                else:
                    physical_symptoms.append(symptom)
    
    # Формируем описание
    description = ""
    
    # Добавляем физические симптомы
    if physical_symptoms:
        description += "Физические признаки:"
        for symptom in physical_symptoms:
            symptom_name = symptom.split("!")[1]
            if symptom_name in symptoms_description:
                description += f"\n- {symptoms_description[symptom_name]}"
    
    # Добавляем психические симптомы
    if mental_symptoms:
        if description:  # Добавляем пустую строку, если уже есть описание
            description += "\n"
        description += "Психические признаки:"
        for symptom in mental_symptoms:
            symptom_name = symptom.split("!")[1]
            if symptom_name in symptoms_description:
                description += f"\n- {symptoms_description[symptom_name]}"
    
    # Добавляем симптомы движений
    if movement_symptoms:
        if description:  # Добавляем пустую строку, если уже есть описание
            description += "\n"
        description += "Особенности движений:"
        for symptom in movement_symptoms:
            symptom_name = symptom.split("!")[1]
            if symptom_name in symptoms_description:
                description += f"\n- {symptoms_description[symptom_name]}"
    
    # Добавляем заключение
    total_symptoms = len(physical_symptoms) + len(movement_symptoms) + len(mental_symptoms)
    if description:  # Добавляем пустую строку перед заключением, если есть описание
        description += "\n"
    if total_symptoms >= 3:
        description += "Ситуация требует внимания."
    elif total_symptoms == 2:
        description += "Требуется наблюдение."
    elif total_symptoms == 1:
        description += "Состояние в норме."
    else:
        description += "Внешне выглядит обычным человеком."
    
    return description, actual_symptoms  # Возвращаем и описание, и список реальных симптомов
