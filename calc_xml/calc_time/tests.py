import os
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils.dateparse import parse_duration
from lxml import etree
from .calc_time import fast_iter, calc


# функция проверки соответствия полученного и правильного результатов
def eq(context, calc_data, **kwargs):
    res = True
    count_context_elem = 0
    for event, elem in context:
        count_context_elem += 1
        for sub_element in elem.getchildren():
            if sub_element.tag == 'date':
                date = sub_element.text
            else:
                sum_delta = sub_element.text
        if date in calc_data:
            if calc_data[date] != parse_duration(sum_delta):
                res = False
        else:
            res = False
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    if count_context_elem < len(calc_data):
        res = False

    return res


class CalcTests(TestCase):

    def setUp(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.context_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/people_test.xml'),
                                           events=('end',), tag='person')
        fullname_str = 'person2'
        self.fullname_xpath = etree.XPath(f"/people/person[@full_name='{fullname_str}']")

    def tearDown(self):
        del self.basedir
        del self.context_xml
        del self.fullname_xpath

    # проверка обработки по имени и интервалу дат
    def test_interval_fullname(self):
        calc_for_days = fast_iter(self.context_xml, calc,
                                  start=datetime.strptime('27-12-2011 0:00:00', '%d-%m-%Y %H:%M:%S'),
                                  end=datetime.strptime('29-12-2011 23:59:59', '%d-%m-%Y %H:%M:%S'),
                                  xp=self.fullname_xpath)
        test_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/result_interval_fullname.xml'),
                                   events=('end',), tag='day')
        self.assertEqual(eq(test_xml, calc_for_days), True)

    # проверка обработки по интервалу дат
    def test_interval(self):
        calc_for_days = fast_iter(self.context_xml, calc,
                                  start=datetime.strptime('27-12-2011 0:00:00', '%d-%m-%Y %H:%M:%S'),
                                  end=datetime.strptime('28-12-2011 23:59:59', '%d-%m-%Y %H:%M:%S'))
        test_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/result_interval.xml'),
                                   events=('end',), tag='day')
        self.assertEqual(eq(test_xml, calc_for_days), True)

    # проверка обработки по имени
    def test_fullname(self):
        calc_for_days = fast_iter(self.context_xml, calc, xp=self.fullname_xpath)
        test_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/result_fullname.xml'),
                                   events=('end',), tag='day')
        self.assertEqual(eq(test_xml, calc_for_days), True)

    # проверка обработки без имени и дат
    def test_result(self):
        calc_for_days = fast_iter(self.context_xml, calc)
        test_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/result.xml'),
                                   events=('end',), tag='day')
        self.assertEqual(eq(test_xml, calc_for_days), True)

    # проверка обнаружения ошибки
    def test_wrong_result(self):
        calc_for_days = fast_iter(self.context_xml, calc)
        test_xml = etree.iterparse(os.path.join(self.basedir, 'for_tests/result_wrong.xml'),
                                   events=('end',), tag='day')
        self.assertEqual(eq(test_xml, calc_for_days), False)
