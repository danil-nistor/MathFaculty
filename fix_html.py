import re

def process_html_tabs_in_file(file_path):
    # Читаем файл целиком
    try:
        with open(file_path, 'r', encoding='windows-1251') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return

    # Регулярное выражение:
    # (?:...) - группа без захвата (для выбора начала)
    # <!DOCTYPE|<html - ищем одно из двух
    # .*? - любой контент (нежадный поиск, до первого закрывающего тега)
    # </html> - конец блока
    # flags=re.DOTALL - чтобы точка . захватывала и переносы строк (\n)
    # flags=re.IGNORECASE - чтобы <HTML> тоже сработал
    pattern = r'((?:<!DOCTYPE|<html).*?</html>)'

    def replace_tabs(match):
        html_block = match.group(0)
        # Заменяем табуляцию на 4 пробела. 
        # Если нужно на 1 пробел, замените '    ' на ' '
        return html_block.replace('\t', '    ')

    # Выполняем замену только внутри найденных блоков
    new_content = re.sub(pattern, replace_tabs, content, flags=re.DOTALL | re.IGNORECASE)

    # Записываем результат обратно в файл (или в новый файл)
    output_path = file_path # Можно изменить на 'output.txt'
    
    with open(output_path, 'w', encoding='windows-1251') as f:
        f.write(new_content)

    print(f"Готово! Файл '{output_path}' обработан.")

# --- Использование ---
# Укажите имя вашего файла здесь
filename = 'Планы (2).txt' 

# Запуск функции
process_html_tabs_in_file(filename)