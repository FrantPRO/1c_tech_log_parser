# Парсер логов технологического журнала 1С 8.3
import os
import json

# Дериктория для поиска файлов логов
directory = os.path.normpath(r'\\1cv8\logs')

# Значение отбора данных
selection = "meta"

# Дата отбора логов в формате ГГММДД, где ГГ-год, ММ-месяц, ДД-день
data_s = '190401'

# функция открывает файл и читает по строке с контрлем конца строки
def line_reader(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        complite_line = ''
        for line in f:
            if not line:
                continue
            complite_line += line
            if ':\n' in complite_line:
                complite_line = line.strip('\n')
                continue
            else:
                yield complite_line.strip('\n')
                complite_line = ''


# Метод возвращает словарь с параметрами из файла
# Формат папок логов <ИмяПроцесса>_<ИдентификаторПроцесса>
# Формат фалов логов: имя файла = ГГММДДЧЧ.log, начало файла ММ:СС.тттт-д,<ИмяСобытия>,<Уровень>,<Ключ=Значение>,...
def read_log_file(str_directory, str_file):

    if len(str_file) != 12:
        return 0

    m_result = {}

    # Получаем дату и час из имени файла
    log_date = str_file[4:6] + "." + str_file[2:4] + ".20" + str_file[0:2]
    log_hour = str_file[6:8] + ":"

    dm_result = []

    # Читаем файл по строкам
    for line in line_reader(os.path.join(str_directory, str_file)):

        # Если искомое значение есть в строке
        if selection in line:

            # Получаем основные параметры
            m_params = line.split(',')
            time = log_hour + m_params[0][0:5]
            rphost = str_directory.split('_')[-1] if len(str_directory.split('_')) > 1 else ''

            d_result = {"Time": time, "Event": m_params[1], "Level": m_params[2], "rphost": rphost}

            # Удаляем основные параметры, чтобы не мешали
            del (m_params[0:3])

            # Получаем дополнительные параметры
            o_params = {}
            for element in m_params:
                element = element.strip()
                el = element.split('=')
                if len(el) == 1:
                    o_params[el[0]] = el[0]
                else:
                    o_params[el[0]] = el[1].strip()
            d_result["Params"] = o_params

            dm_result.append(d_result)

            m_result["File_" + log_date] = dm_result

    return m_result


if __name__ == 'main':
    # Список для результата
    result = []

    # Получаем объект-генератор и на каждой итерации получаем кортеж files со списком файлов из очередной папки
    for d, dirs, files in os.walk(directory):

        # Отбираем только файлы логов
        files = filter(lambda x: x.endswith('.log') and data_s in x, files)

        for file in files:
            log_file = read_log_file(d, file)
            if log_file:
                result.append(log_file)

    print(json.dumps(result, ensure_ascii=False))
