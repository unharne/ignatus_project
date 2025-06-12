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

    # Определяем, будет ли это демон (30% шанс)
    is_demon = random.random() < 0.3

    # Если это демон, гарантируем хотя бы один симптом с "!"
    if is_demon:
        random_health = {}
        # Сначала выбираем случайную часть тела для симптома с "!"
        demon_part = random.choice(list(health.keys()))
        random_health[demon_part] = "Больная"
        
        # Для остальных частей тела случайный выбор
        for part in health.keys():
            if part != demon_part:
                random_health[part] = random.choice(health[part])
    else:
        # Для обычного человека просто случайный выбор
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
            if is_demon and part == demon_part:
                # Для демона выбираем только симптомы с "!"
                demon_symptoms = [s for s in symptoms[part] if s.startswith("!")]
                random_symptoms[part] = random.choice(demon_symptoms)
            else:
                random_symptoms[part] = random.choice(symptoms[part])

    result = dict(
        health=health,
        model=model,
        random_symptoms=random_symptoms,
        is_human=not is_demon,
        gender=gender,
        name=name
    )

    return result