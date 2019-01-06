# Парсер логов технологического журнала 1С 8.3
import os

# Дериктория для поиска файлов логов
directory = "/tmp/123"


# Метод возвращает словарь с параметрами из файла
# Формат папок логов <ИмяПроцесса>_<ИдентификаторПроцесса>
# Формат фалов логов: имя файла = ГГММДДЧЧ.log, начало файла ММ:СС.тттт-д,<ИмяСобытия>,<Уровень>,<Ключ=Значение>,...
def read_log(str_directory, str_file):

    m_result = []

    log_date = str_file[4:6] + "." + str_file[2:4] + ".20" + str_file[0:2] + " " + str_file[6:8] + ":"

    with open(os.path.join(str_directory, str_file), 'r') as f:
        for line in f:
            m_params = line.split(',')
            d_result = {"Date": log_date + m_params[0][0:5], "Event": m_params[1], "Level": m_params[2]}
            del (m_params[0:3])
            for element in m_params:
                el = element.split('=')
                if len(el) == 1:
                    d_result[el[0]] = el[0]
                else:
                    d_result[el[0]] = el[1]
            m_result.append(d_result)
    return m_result


# Список для результата
result = []

# Получаем объект-генератор и на каждой итерации получаем кортеж files со списком файлов из очередной папки
for d, dirs, files in os.walk(directory):
    # print(files)

    # Фильтруем файлы
    files = filter(lambda x: x.endswith('.log'), files)

    for file in files:
        # print(d)
        result.append(read_log(d, file))

print(result)
