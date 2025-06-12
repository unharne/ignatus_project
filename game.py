import os
import random
import json
from colorama import Fore, Style, init
from constructor import constructor
from data import *
from description import generate_description, edit_text

# Initialize colorama
init()

def clear_console():
    """Очищает консоль в зависимости от операционной системы."""
    if os.name == 'nt':
        os.system('cls')

def load_high_score():
    """Загружает рекорд из файла."""
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"score": 0, "day": 0}

def save_high_score(score, day):
    """Сохраняет рекорд в файл."""
    with open('high_score.json', 'w') as f:
        json.dump({"score": score, "day": day}, f)

def print_header():
    """Выводит красивый заголовок игры."""
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}👹 ИГНАТУС ПРОЕКТ - ДИАГНОСТИКА ОДЕРЖИМЫХ 👹")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def evaluate_symptoms(shuffled_values: list, real_symptoms: dict, difficulty: str):
    """Оценивает симптомы персонажа с учетом сложности."""
    local_score = 0
    max_attempts = 3 if difficulty == "сложный" else 2 if difficulty == "средний" else 1
    
    for symptom in shuffled_values:
        attempts = 0
        while attempts < max_attempts:
            print(f"{Fore.YELLOW}Есть ли у него симптом '{symptom}'?")
            print(f"  1 - Да\n  2 - Нет{Style.RESET_ALL}")
            answer = input("Ваш выбор (1/2): ").strip()
            if answer == '1' or answer == '2':
                break
            else:
                attempts += 1
                if attempts < max_attempts:
                    print(f"{Fore.RED}Пожалуйста, введите 1 или 2. Осталось попыток: {max_attempts - attempts}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Превышено количество попыток. Следующий симптом.{Style.RESET_ALL}")
                    break

        if answer == '1' and symptom in real_symptoms:
            local_score += 2 if difficulty == "сложный" else 1
            print(f"{Fore.GREEN}✓ Да, это совпадает с симптомом.{Style.RESET_ALL}")
        
        elif answer == '2' and symptom not in real_symptoms:
            local_score += 2 if difficulty == "сложный" else 1
            print(f"{Fore.GREEN}✓ Вы верно ответили.{Style.RESET_ALL}")
        
        elif answer == '1' and symptom not in real_symptoms:
            local_score -= 2 if difficulty == "сложный" else 1
            print(f"{Fore.RED}✗ Вы ошиблись, этого симптома у него нет.{Style.RESET_ALL}")

        elif answer == '2' and symptom in real_symptoms:
            local_score -= 2 if difficulty == "сложный" else 1
            print(f"{Fore.RED}✗ Вы ошиблись, этот симптом есть.{Style.RESET_ALL}")       

    return local_score

def get_player_decision():
    while True:
        print(f"\n{Fore.YELLOW}Ваше решение:")
        print(f"  1 - Пропустить\n  2 - Убить{Style.RESET_ALL}")
        decision = input("Ваш выбор (1/2): ").strip()
        if decision == '1' or decision == '2':
            return decision
        else:
            print(f"{Fore.RED}Пожалуйста, введите 1 или 2.{Style.RESET_ALL}")

def get_difficulty():
    while True:
        print(f"{Fore.YELLOW}Выберите сложность:")
        print(f"  1 - Легкий\n  2 - Средний\n  3 - Сложный{Style.RESET_ALL}")
        difficulty = input("Ваш выбор (1/2/3): ").strip()
        if difficulty == '1':
            return "легкий"
        elif difficulty == '2':
            return "средний"
        elif difficulty == '3':
            return "сложный"
        else:
            print(f"{Fore.RED}Пожалуйста, выберите 1, 2 или 3.{Style.RESET_ALL}")

def start_game():
    """Основной цикл игры."""
    clear_console()
    print_header()
    
    high_score = load_high_score()
    print(f"{Fore.MAGENTA}Текущий рекорд: {high_score['score']} очков (день {high_score['day']}){Style.RESET_ALL}\n")
    
    difficulty = get_difficulty()
    current_score = 0
    day = 1
    correct_decisions = 0
    total_decisions = 0
    
    while True:
        clear_console()
        print_header()
        print(f"{Fore.CYAN}День {day} | Сложность: {difficulty.capitalize()} | Очки: {current_score}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Пропускай или убивай.{Style.RESET_ALL}")

        result = constructor(health)
        description = generate_description(result)
        is_human = result['is_human']

        print(f"\n{Fore.CYAN}Пациент:{Style.RESET_ALL}")
        print(result['model'])
        print(f"\n{Fore.CYAN}Описание:{Style.RESET_ALL}")
        print(description)

        really_symptoms = result['random_symptoms']
        real_symptoms = edit_text(really_symptoms)
        random_symptoms = []
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
        score = evaluate_symptoms(shuffled_values, real_symptoms, difficulty)
        current_score += score
        decision = get_player_decision()
        total_decisions += 1

        if decision == '1':  # Пропустить
            if is_human:
                print(f"{Fore.GREEN}✓ Человек пропущен.{Style.RESET_ALL}")
                current_score += 2 if difficulty == "сложный" else 1
                correct_decisions += 1
            else:
                print(f"{Fore.RED}✗ Вы ошиблись, гость проник в больницу!{Style.RESET_ALL}")
                current_score -= 2 if difficulty == "сложный" else 1

        if decision == '2':  # Убить
            if not is_human:
                print(f"{Fore.GREEN}✓ Гость был убит!{Style.RESET_ALL}")
                current_score += 2 if difficulty == "сложный" else 1
                correct_decisions += 1
            else:
                print(f"{Fore.RED}✗ Вы ошиблись в диагнозе и убили невиновного.{Style.RESET_ALL}")
                current_score -= 2 if difficulty == "сложный" else 1

        if day % 7 == 0:
            accuracy = (correct_decisions / total_decisions) * 100
            print(f"\n{Fore.CYAN}=== Недельный отчет ===")
            print(f"Баллы Игната Минибро: {current_score}")
            print(f"Точность диагнозов: {accuracy:.1f}%")
            print(f"Правильных решений: {correct_decisions} из {total_decisions}{Style.RESET_ALL}")

            if current_score > high_score['score']:
                print(f"\n{Fore.GREEN}🎉 Новый рекорд! 🎉{Style.RESET_ALL}")
                save_high_score(current_score, day)
                high_score = {"score": current_score, "day": day}

        if input(f"\n{Fore.YELLOW}Продолжить? (1 - Да / 2 - Нет): {Style.RESET_ALL}").strip() == '2':
            print(f"\n{Fore.CYAN}=== Итоги игры ===")
            print(f"Баллы Игната Минибро: {current_score}")
            print(f"Точность диагнозов: {(correct_decisions / total_decisions) * 100:.1f}%")
            print(f"Правильных решений: {correct_decisions} из {total_decisions}")
            print(f"Лучший результат: {high_score['score']} очков (день {high_score['day']}){Style.RESET_ALL}")
            break

        day += 1