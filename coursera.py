import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
import argparse
import random


def fetch_content(url):
    time.sleep(1)
    print('fetch: {0}'.format(url))
    request = requests.get(url)
    if request.status_code == requests.codes.ok:
        return request.content


def get_courses_list(coursera_xml):
    coursera_tree_xml = etree.XML(coursera_xml)
    return [e.text for e in coursera_tree_xml.iter('*') if e.text.startswith('http')]


def get_html_text(html_tree, tag, attrs):
    target_element = html_tree.find(tag, attrs)
    if target_element is not None:
        return target_element.text


def get_html_count_elements(html_tree, tag, attrs):
    target_elements = html_tree.find_all(tag, attrs)
    return len(target_elements)


def get_random_courses_info(url_courses_list, count_courses):
    shuffled_courses_list = make_shuffled_list(url_courses_list)
    return [get_course_info(url) for url in shuffled_courses_list[:count_courses]]


def make_shuffled_list(seq):
    shuffled_seq = seq[:]
    random.shuffle(shuffled_seq)
    return shuffled_seq


def get_course_info(course_url):
    course_html = fetch_content(course_url)
    course_html_tree = BeautifulSoup(course_html, 'html.parser')
    return {'Name': get_html_text(course_html_tree, 'h1', {'class': 'title display-3-text'}),
            'Language': get_html_text(course_html_tree, 'div', {'class': 'rc-Language'}),
            'Start date': course_html_tree.find('div', {'class': 'startdate rc-StartDateString caption-text'}).find('span').text,
            'Period': get_html_count_elements(course_html_tree, 'div', {'class': 'week'}),
            'Rating': get_html_text(course_html_tree, 'div', {'class': 'ratings-text bt3-visible-xs'})
            }


def xls_set_head(worksheet, head_names):
    for row in worksheet.iter_rows(min_row=1, max_col=len(head_names) + 1, max_row=1):
        for name, cell in zip(head_names, row):
            cell.value = name


def output_courses_info_to_xlsx(filepath, courses_info):
    wb = Workbook()
    worksheet = wb.active
    worksheet.title = 'Coursera'
    head_names = courses_info[0].keys()
    xls_set_head(worksheet, head_names)
    for row, course_info in zip(worksheet.iter_rows(min_row=2, max_col=len(head_names)+1, max_row=len(courses_info)+1), courses_info):
        for name, cell in zip(head_names, row):
            cell.value = course_info[name]
    wb.save(filepath)


if __name__ == '__main__':
    default_count_courses = 20
    default_output_filename = 'coursera_courses.xlsx'
    parser = argparse.ArgumentParser(description='export Cousera courses to excel')
    parser.add_argument('-c', '--count', help='count courses to export in excel', type=int, default=default_count_courses)
    parser.add_argument('-o', '--output', help='output filename', type=str, default=default_output_filename)
    args = parser.parse_args()
    coursera_xml_feed = 'https://www.coursera.org/sitemap~www~courses.xml'
    coursera_xml_content = fetch_content(coursera_xml_feed)
    url_courses_list = get_courses_list(coursera_xml_content)
    output_courses_info_to_xlsx(args.output, get_random_courses_info(url_courses_list, args.count))
