# Парсер логов технологического журнала 1С 8.3
import os
import json

# Дериктория для поиска файлов логов
directory = "/tmp/123"

# Значение отбора данных
selection = "meta"


# Метод возвращает словарь с параметрами из файла
# Формат папок логов <ИмяПроцесса>_<ИдентификаторПроцесса>
# Формат фалов логов: имя файла = ГГММДДЧЧ.log, начало файла ММ:СС.тттт-д,<ИмяСобытия>,<Уровень>,<Ключ=Значение>,...
def read_log_file(str_directory, str_file):

    m_result = {}

    # Получаем дату и час из имени файла
    log_date = str_file[4:6] + "." + str_file[2:4] + ".20" + str_file[0:2]
    log_hour = str_file[6:8] + ":"

    with open(os.path.join(str_directory, str_file), 'r') as f:

        dm_result = []

        # Читаем файл по строкам
        for line in f:
            # print(line)

            # Если искомое значение есть в строке
            if selection in line:

                # Получаем основные параметры
                m_params = line.split(',')
                d_result = {"Time": log_hour + m_params[0][0:5], "Event": m_params[1], "Level": m_params[2]}
                del (m_params[0:3])

                # Получаем остальные параметры
                o_params = {}
                for element in m_params:
                    el = element.split('=')
                    if len(el) == 1:
                        o_params[el[0]] = el[0]
                    else:
                        o_params[el[0]] = el[1].strip()
                d_result["Params"] = o_params

                dm_result.append(d_result)

                m_result["File_" + log_date] = dm_result

    return m_result


# Список для результата
result = []

# Получаем объект-генератор и на каждой итерации получаем кортеж files со списком файлов из очередной папки
for d, dirs, files in os.walk(directory):
    # print(files)

    # Отбираем только файлы логов
    files = filter(lambda x: x.endswith('.log'), files)

    for file in files:
        # print(d)
        result.append(read_log_file(d, file))

print(json.dumps(result))

