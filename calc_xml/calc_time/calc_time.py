import os
from datetime import datetime
from django.conf import settings
from lxml import etree


# функция перебора всех узлов, подсчета и суммирования разницы delta
def fast_iter(context, func, **kwargs):
    res = {}
    for event, elem in context:
        calc_date = func(elem, **kwargs)
        if calc_date:
            calc_date_str = calc_date['date'].strftime('%d-%m-%Y')
            if calc_date_str in res:
                res[calc_date_str] += calc_date['delta']
            else:
                res[calc_date_str] = calc_date['delta']
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    return res


# функция для извлечения из узла person данных start и end
def get_start_end_elem(el):
    for sub_element in el.getchildren():
        if sub_element.tag == 'start':
            str_start_time = sub_element.text
        else:
            str_end_time = sub_element.text
    start_time = datetime.strptime(str_start_time, '%d-%m-%Y %H:%M:%S')
    end_time = datetime.strptime(str_end_time, '%d-%m-%Y %H:%M:%S')
    return {'start': start_time, 'end': end_time}


# проверка соответствия имени
def check_fullname(el, xp):
    fullname_xp = xp(el)
    if fullname_xp:
        if fullname_xp[0].get('full_name') == el.get('full_name'):
            return True
    return False


# вычисление времени пребывания за одно посещение
def calc(el, start=None, end=None, xp=None):
    start_end = get_start_end_elem(el)
    if start and end:
        if (start_end['start'] >= start) and (start_end['end'] <= end):
            if xp:
                if not check_fullname(el, xp):
                    return None
        else:
            return None
    else:
        if xp:
            if not check_fullname(el, xp):
                return None
    delta_time = start_end['end'] - start_end['start']
    return {'date': start_end['start'].date(), 'delta': delta_time}


# запись вычисленного результата в xml файл
def save_xml(result_file, calc_data):
    print(result_file)
    data = etree.Element('data')
    root = etree.ElementTree(data)
    for day_data in calc_data:
        day = etree.SubElement(data, 'day')
        date = etree.SubElement(day, 'date')
        date.text = day_data
        duration = etree.SubElement(day, 'duration')
        duration.text = str(calc_data[day_data])
        root.write(result_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')


# функция для вызова из страницы приложения
def calc_file(filename, start=None, end=None, fullname=None):
    base_dir_str = str(settings.BASE_DIR)
    file_full_path = base_dir_str + filename
    result_filename = 'result_' + os.path.basename(filename)
    result_dir = base_dir_str + os.path.dirname(filename)
    result_full_path = os.path.join(result_dir, result_filename)
    download_link = os.path.join(os.path.dirname(filename), result_filename)
    context_xml = etree.iterparse(file_full_path, events=('end',), tag='person')

    fullname_xpath = None
    if fullname:
        fullname_str = fullname
        fullname_xpath = etree.XPath(f"/people/person[@full_name='{fullname_str}']")
    start_datetime = None
    end_datetime = None
    if start and end:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        start_datetime = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0, 0)
        end_datetime = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59, 999999)

    calc_for_days = fast_iter(context_xml, calc,
                              start=start_datetime,
                              end=end_datetime,
                              xp=fullname_xpath)
    save_xml(result_full_path, calc_for_days)
    return download_link
