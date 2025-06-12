import os
import random
from colorama import Fore, Style
from constructor import constructor
from data import *
from description import generate_description, edit_text


def clear_console():
    """Очищает консоль в зависимости от операционной системы."""
    if os.name == 'nt':
        os.system('cls')

def evaluate_symptoms(shuffled_values: list, real_symptoms: dict):
    """Оценивает симптомы персонажа, но не принимает решения до конца всех вопросов."""
    local_score = 0
    
    for symptom in shuffled_values:
        while True:
            answer = input(f"{Fore.YELLOW}Есть ли у него симптом '{symptom}'? (да/нет): {Style.RESET_ALL}").strip().lower()
            if answer == 'да' or answer == 'нет':
                break
            else:
                print(f"{Fore.RED}Пожалуйста, введите 'да' или 'нет'.{Style.RESET_ALL}")

        if answer == 'да' and symptom in real_symptoms:
            local_score+= 1
            print(f"{Fore.GREEN}Да, это совпадает с симптомом.{Style.RESET_ALL}")
        
        elif answer == 'нет' and symptom not in real_symptoms:
            local_score+= 1
            print(f"{Fore.GREEN}Вы верно ответили.{Style.RESET_ALL}")
        
        elif answer == 'да' and symptom not in real_symptoms:
            local_score-= 1
            print(f"{Fore.RED}Вы ошиблись, этого симптома у него нет.{Style.RESET_ALL}")

        elif answer == 'нет' and symptom  in real_symptoms:
            local_score-= 1
            print(f"{Fore.RED}Вы ошиблись, этот симптом есть.{Style.RESET_ALL}")       

    return local_score

def get_player_decision():
    while True:
        decision = input(f"\n{Fore.YELLOW}Вы хотите пропустить или убить? (пропустить/убить): {Style.RESET_ALL}").strip().lower()
        if decision == 'пропустить' or decision == 'убить':
            return decision
        else:
            print(f"{Fore.RED}Пожалуйста, введите 'пропустить' или 'убить'.{Style.RESET_ALL}")

def start_game():
    """Основной цикл игры."""
    current_score = 0
    day = 1
    while True:
        clear_console()
        print(f"{Fore.CYAN}День {day}{Style.RESET_ALL}")

        print(f"{Fore.MAGENTA}Пропускай или убивай.{Style.RESET_ALL}")

        result = constructor(health)
        description = generate_description(result)
        is_human = result['is_human']

        print(result['model'])
        print(description)

        really_symptoms = result['random_symptoms']
        real_symptoms = edit_text(really_symptoms)
        random_symptoms =  []
        cnt = 3
        while cnt != 0:
            list_symptoms = random.choice(list(symptoms.values()))
            random_symptom = random.choice(list_symptoms)
            
            if random_symptom.startswith("!"):
                x = random_symptom.split("!")[1]
                if x not in real_symptoms:
                    random_symptoms.append(x)
                    cnt -= 1
            else:
                if random_symptom not in real_symptoms:
                    random_symptoms.append(random_symptom)
                    cnt -= 1

        combined_values = real_symptoms + random_symptoms
        shuffled_values = random.sample(combined_values, len(combined_values))
        score = evaluate_symptoms(shuffled_values, real_symptoms)
        current_score += score
        decision = get_player_decision()

        if decision == 'пропустить':
            if is_human == True:
                print(f"{Fore.GREEN}Человек пропущен.{Style.RESET_ALL}")
                current_score += 1
            else:
                print(f"{Fore.RED}Вы ошиблись, гость проник в больницу!.{Style.RESET_ALL}")
                current_score -= 1

        if decision == 'убить':
            if is_human == False:
                print(f"{Fore.GREEN}Гость был убит!{Style.RESET_ALL}")
                current_score += 1
            else:
                print(f"{Fore.RED}Вы ошиблись в диагнозе и убили невиновного.{Style.RESET_ALL}")
                current_score -= 1

        if day % 7 == 0:
            print(f"\n{Fore.CYAN}Баллы Игната Минибро: {current_score}{Style.RESET_ALL}")

        if input(f"\n{Fore.YELLOW}Продолжить? (да/нет): {Style.RESET_ALL}").strip().lower() == 'нет':
            print(f"\n{Fore.CYAN}Баллы Игната Минибро: {current_score}{Style.RESET_ALL}")
            break

        day += 1