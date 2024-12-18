# --- Задача №1 Удвоение чисел и получение первого результата ---
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import ast

def process_number(number): # Функция для обработки числа
    time.sleep(0.2)  # Имитация задержки в 0.2 секунды
    return number * 2  # Умножаем число на 2 и возвращаем результат

def load_numbers_from_file(filename): # Функция для загрузки списков из файла
    with open(filename, 'r') as file:
        content = file.read()  # Читаем содержимое файла
        return ast.literal_eval(content)  # Преобразуем строку в список списков

def process_single_list(sublist): # Функция обработки списка с использованием многопоточности
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_number = {executor.submit(process_number, num): num for num in sublist}
        # Ждем завершения всех задач и собираем обработанные значения
        for future in as_completed(future_to_number):
            results.append(future.result())   
    return results

def process_numbers(number_lists):# Функция для обработки всех списков
    results_dict = {}
    completion_times = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(process_single_list, sublist): i for i, sublist in enumerate(number_lists)}
        # Цикл по завершенным задачам
        for future in as_completed(future_to_index):
            list_index = future_to_index[future]  # Получаем индекс списка
            result = future.result()  # Получаем результат завершенной задачи
            results_dict[list_index] = result  # Сохраняем результаты
            completion_times.append((list_index, sum(result)))  # Сохраняем индекс и сумму
    return results_dict, completion_times  # Возвращаем результаты и время завершения

def calculate_result(completion_times): # Функция для вычисления и вывода суммы самого быстрого списка
    # Находим индекс и сумму списка с минимальным временем обработки
    fastest_index, fastest_sum = min(completion_times, key=lambda x: x[1])
    # Выводим результат
    print(f'Сумма чисел в первом обработанном списке (индекс {fastest_index}): {fastest_sum}')

def task1(): # Основная функция
    filename = 'test_list_numbers.txt'  # Имя файла со списком
    number_lists = load_numbers_from_file(filename)  # Загружаем списки из файла
    results_dict, completion_times = process_numbers(number_lists)  # Обрабатываем числа
    calculate_result(completion_times)  # Вычисляем и выводим сумму для самого быстрого списка

# Тест задачи 1
if __name__ == "__main__":
    task1()  # Вызываем основную функцию

# --- Задача №2  Поиск и суммирование чисел через цепочку файлов ---
import zipfile
import multiprocessing
import re

def read_number_from_zip(zip_path, file_path): # Читает число из указанного файла
    with zipfile.ZipFile(zip_path) as zip_file:
        with zip_file.open(file_path) as file:
            content = file.read().decode('utf-8')  # Чтение содержимого файла
            match = re.search(r'\d+', content)  # Поиск первого числа в тексте
            return int(match.group(0)) if match else 0  # Возвращаем найденное число или 0

def process_file(zip_path_1, zip_path_2, file_path): # Извлекает путь и считывает число
    with zipfile.ZipFile(zip_path_1) as zip_file:
        with zip_file.open(file_path) as file:
            relative_path = file.read().decode('utf-8').strip()  # Чтение пути из файла
            relative_path = relative_path.replace('\\', '/')# Заменяем обратные слэши на прямые
            return read_number_from_zip(zip_path_2, relative_path)  # Получение числа из второго архива

def task2(): # Функция запуска обработки файлов
    path_to_first_zip = 'path_8_8.zip'  # Путь к первому архиву
    path_to_second_zip = 'recursive_challenge_8_8.zip'  # Путь ко второму архиву
    # Получение списка всех текстовых файлов из первого архива
    with zipfile.ZipFile(path_to_first_zip) as zip_file:
        text_files = [f for f in zip_file.namelist() if f.endswith('.txt')]  # Файлы с расширением .txt
    # Использование multiprocessing для параллельной обработки файлов
    num_processes = multiprocessing.cpu_count() -1 # Определяем количество процессов
    with multiprocessing.Pool(processes=num_processes) as pool:
    # pool = multiprocessing.Pool(processes=num_processes) # создаем объект пулла процессов
        results = pool.starmap(process_file, [(path_to_first_zip, path_to_second_zip, file_path) for file_path in text_files]) # Запуск обработки файлов
    # Суммирование всех найденных чисел и вывод результата
    total_sum = sum(results)
    print(f'Сумма всех чисел {total_sum}')  # Выводим общий результат
# Тест задачи 2
if __name__ == "__main__":
    task2()  # Запуск основной функции