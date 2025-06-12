import random
from colorama import Fore, Style
from data import symptoms, male_names, female_names, health

def constructor(health: dict) -> dict:
    # Выбор пола
    gender = random.choice(['мужчина', 'женщина'])
    if gender == 'мужчина':
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    random_health = {key: random.choice(values) for key, values in health.items()}
    health = random_health

    head = Fore.RED if health['head'] == "Больная" else Fore.GREEN
    arms = Fore.RED if health['arms'] == "Больная" else Fore.GREEN
    body = Fore.RED if health['body'] == "Больная" else Fore.GREEN
    legs = Fore.RED if health['legs'] == "Больная" else Fore.GREEN

    model = f"""
        {head}   O   {Style.RESET_ALL}
        {arms}  /|\\  {Style.RESET_ALL}
        {body}   |    {Style.RESET_ALL}
        {legs}  / \\  {Style.RESET_ALL}
        Имя: {name}
        Пол: {gender.capitalize()}
        """
    
    random_symptoms = {}

    for part, state in health.items():
        if state == "Больная":
            random_symptoms[part] = random.choice(symptoms[part])
    
    is_human = True
    for symptome in random_symptoms.values():
        if symptome.startswith("!"):
            is_human = False
            break

    result = dict(
        health=health,
        model=model,
        random_symptoms=random_symptoms,
        is_human=is_human,
        gender=gender,
        name=name
    )

    return result