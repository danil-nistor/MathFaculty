import os
import sys

# ================= НАСТРОЙКИ =================
INPUT_FILE = 'edu_hours.txt'      # Имя входного файла
OUTPUT_FILE = 'edu_hours.sql'   # Имя выходного SQL файла
# =============================================

def escape_sql_string(s):
    """Экранирует строку для MySQL/MariaDB"""
    if s is None:
        return "NULL"
    # ВАЖНО: Сначала экранируем обратные слеши, потом кавычки!
    s = s.replace('\\', '\\\\')  # \ → \\
    s = s.replace("'", "''")      # ' → ''
    return "'" + s + "'"

def escape_sql_identifier(name):
    """Экранирует имя колонки/таблицы"""
    clean_name = name.strip().replace(' ', '_').replace('-', '_')
    return f"`{clean_name}`"

def clean_multiline_content(text):
    """Удаляет переносы строк внутри RTF и HTML блоков"""
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        # === ПРОВЕРКА НА RTF ===
        if text[i:i+5] == '{\\rtf':
            rtf_start = i
            brace_depth = 0
            j = i
            while j < length:
                if text[j] == '{':
                    brace_depth += 1
                elif text[j] == '}':
                    brace_depth -= 1
                    if brace_depth == 0:
                        break
                j += 1
            
            rtf_block = text[rtf_start:j+1]
            rtf_clean = rtf_block.replace('\n', ' ').replace('\r', ' ')
            result.append(rtf_clean)
            i = j + 1
            continue
        
        # === ПРОВЕРКА НА HTML (по <!DOCTYPE) ===
        if text[i:i+9].upper() == '<!DOCTYPE':
            html_start = i
            j = i
            
            while j < length:
                if j + 7 <= length:
                    close_tag = text[j:j+7].lower()
                    if close_tag == '</html>' or close_tag == '</body>':
                        j += 7
                        break
                j += 1
            
            if j >= length or (j < length and text[j] == '\n'):
                while j < length and text[j] != '\n':
                    j += 1
            
            html_block = text[html_start:j]
            html_clean = html_block.replace('\n', ' ').replace('\r', ' ')
            result.append(html_clean)
            i = j
            continue
        
        # === ОБЫЧНЫЙ СИМВОЛ ===
        result.append(text[i])
        i += 1
    
    return ''.join(result)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ОШИБКА: Файл {INPUT_FILE} не найден.")
        sys.exit(1)

    print(f"Начинаю обработку файла: {INPUT_FILE}...")
    print("СУБД: MariaDB/MySQL")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Очистка переносов строк в RTF/HTML блоках...")
    content = clean_multiline_content(content)
    
    lines = content.strip().split('\n')
    
    if not lines:
        print("Файл пуст.")
        return

    header_line = lines[0].strip()
    header_fields = header_line.split('|')
    num_columns = len(header_fields)
    
    print(f"Заголовок определен. Количество колонок: {num_columns}")
    
    base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]
    table_name = base_name.replace('-', '_').replace(' ', '_')
    
    sql_lines = []
    sql_lines.append("-- MariaDB/MySQL совместимый SQL")
    sql_lines.append("SET NAMES utf8mb4;")
    sql_lines.append("SET CHARACTER SET utf8mb4;")
    sql_lines.append("")
    
    create_table_sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    create_table_sql += "\n  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    
    col_definitions = []
    for col in header_fields:
        col_name = escape_sql_identifier(col)
        col_definitions.append(f"  {col_name} TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    create_table_sql += "\n" + ",\n".join(col_definitions)
    create_table_sql += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
    
    sql_lines.append(create_table_sql)
    sql_lines.append("")
    sql_lines.append("-- Начало импорта данных")
    
    cols_sql = ", ".join([escape_sql_identifier(col) for col in header_fields])
    
    data_lines = lines[1:]
    total_data_lines = len(data_lines)
    
    successful_rows = 0
    error_rows = 0
    
    for idx, line in enumerate(data_lines):
        line = line.strip()
        if not line:
            continue
        
        fields = line.split('|')
        
        if len(fields) != num_columns:
            error_rows += 1
            print(f"⚠️  ОШИБКА в строке {idx + 2}: Ожидалось {num_columns} полей, найдено {len(fields)}.")
            continue
        
        values_sql = ", ".join([escape_sql_string(val) for val in fields])
        insert_query = f"INSERT INTO `{table_name}` ({cols_sql}) VALUES ({values_sql});"
        sql_lines.append(insert_query)
        
        successful_rows += 1
        
        if (idx + 1) % 100 == 0:
            print(f"Обработано строк: {idx + 1} / {total_data_lines}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(sql_lines))
    
    print("\n" + "="*50)
    print("ГОТОВО!")
    print(f"Файл сохранен: {OUTPUT_FILE}")
    print(f"Имя таблицы: {table_name}")
    print(f"Колонок в таблице: {num_columns}")
    print("-" * 50)
    print(f"Всего строк данных: {total_data_lines}")
    print(f"Успешно конвертировано: {successful_rows}")
    print(f"Ошибок парсинга: {error_rows}")
    print("="*50)
    print("\n💡 Для импорта в MariaDB:")
    print(f"   mysql -u пользователь -p база_данных < {OUTPUT_FILE}")
    print("   или через phpMyAdmin → Импорт")
    print("="*50)

if __name__ == "__main__":
    main()