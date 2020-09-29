from lxml import etree
from datetime import datetime, timedelta

people = etree.Element('people')
et = etree.ElementTree(people)
et.write('people_test.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')

et = etree.ElementTree(file='people_test.xml')
root = et.getroot()


def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


start_write = datetime.now()
start_time = datetime.strptime('21-12-2011 10:54:47', '%d-%m-%Y %H:%M:%S')
end_time = datetime.strptime('21-12-2011 19:43:02', '%d-%m-%Y %H:%M:%S')
start_write1 = datetime.now()
for day_index in range(20):  # 2000
    start_write = datetime.now()
    for person_index in range(10):  # 1000
        person = etree.SubElement(people, 'person')
        person.set('full_name', f'person{person_index}')
        etree.SubElement(person, 'start').text = (start_time + timedelta(days=(1 * day_index))).strftime(
            '%d-%m-%Y %H:%M:%S')
        etree.SubElement(person, 'end').text = (end_time + timedelta(days=(1 * day_index))).strftime(
            '%d-%m-%Y %H:%M:%S')
        root.append(person)
    et.write('people_test.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')
    print(datetime.now() - start_write)

print(datetime.now() - start_write1)

print(datetime.now() - start_write)
