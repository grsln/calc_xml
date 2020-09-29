import os
from datetime import datetime, timedelta
from django.test import TestCase
from lxml import etree
from .calc_time import fast_iter, calc
import re

regex = re.compile(r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')


def parse_time(time_str):
    parts = regex.match(time_str)
    assert parts is not None, "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(
        time_str)
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)


def eq(context, calc_data, **kwargs):
    res = True
    for event, elem in context:
        for sub_element in elem.getchildren():
            if sub_element.tag == 'date':
                date = sub_element.text
            else:
                sum_delta = sub_element.text
        if calc_data[date] != parse_time(sum_delta):
            print(date)
            print(calc_data[date])
            print(sum_delta)
            res = False
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

    return res


class CalcTests(TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.context_xml = etree.iterparse(os.path.join(basedir, 'for_tests/people_test.xml'),
                                           events=('end',), tag='person')
        self.out = 'for_tests/test_interval_fullname.xml'
        fullname_str = 'person2'
        self.fullname_xpath = etree.XPath(f"/people/person[@full_name='{fullname_str}']")
        self.test_xml = etree.iterparse(os.path.join(basedir, 'for_tests/result_interval_fullname.xml'),
                                        events=('end',), tag='day')

    def tearDown(self):
        del self.context_xml
        del self.fullname_xpath

    def test_interval_fullname(self):
        calc_for_days = fast_iter(self.context_xml, calc,
                                  start=datetime.strptime('27-12-2011 0:00:00', '%d-%m-%Y %H:%M:%S'),
                                  end=datetime.strptime('29-12-2011 23:59:59', '%d-%m-%Y %H:%M:%S'),
                                  xp=self.fullname_xpath)

        self.assertEqual(eq(self.test_xml, calc_for_days), True)

    # calc_for_days = fast_iter(context_xml, calc, xp=fullname_xpath)

    # calc_for_days = fast_iter(context_xml, calc,
    #               start=datetime.strptime('27-12-2011 0:00:00', '%d-%m-%Y %H:%M:%S'),
    #               end=datetime.strptime('29-12-2011 23:59:59', '%d-%m-%Y %H:%M:%S'))

    # calc_for_days = fast_iter(context_xml, calc)
