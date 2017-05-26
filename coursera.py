import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook


def fetch_content(url):
    time.sleep(1)
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


def get_course_info(course_url):
    print(course_url)
    course_html = fetch_content(course_url)
    course_html_tree = BeautifulSoup(course_html, 'html.parser')
    return {'course_name': get_html_text(course_html_tree, 'h1', {'class': 'title display-3-text'}),
            'course_language': get_html_text(course_html_tree, 'div', {'class': 'rc-Language'}),
            'course_startdate': course_html_tree.find('div', {'class': 'startdate rc-StartDateString caption-text'}).find('span').text,
            'course_period': get_html_count_elements(course_html_tree, 'div', {'class': 'week'}),
            'course_rating': get_html_text(course_html_tree, 'div', {'class': 'ratings-text bt3-visible-xs'})
            }


def xls_set_head(worksheet, head_names):
    for row in worksheet.iter_rows(min_row = 1, max_col=len(head_names)+1, max_row = 1):
        for name, cell in zip(head_names, row):
            cell.value = name
            print(cell.value)


def output_courses_info_to_xlsx(filepath, courses_info):
    wb = Workbook()
    worksheet = wb.create_sheet('Coursera')
    head_names = courses_info[0].keys()
    xls_set_head(worksheet, head_names)
    for row, course_info in zip(worksheet.iter_rows(min_row = 2, max_col=len(head_names)+1, max_row = len(courses_info)+1), courses_info):
        for name, cell in zip(head_names, row):
            cell.value = course_info[name]
    wb.save(filepath)


if __name__ == '__main__':
    coursera_xml_feed = 'https://www.coursera.org/sitemap~www~courses.xml'
    some_xml = fetch_content(coursera_xml_feed)
    url_courses_list = get_courses_list(some_xml)
    c_info = get_course_info(url_courses_list[0])
    print(c_info)
    output_courses_info_to_xlsx('qq.xlsx', [c_info])
