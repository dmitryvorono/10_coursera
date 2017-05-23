import requests
from lxml import etree
from bs4 import BeautifulSoup
import time

def fetch_content(url):
    time.sleep(1)
    request = requests.get(url)
    if request.status_code == requests.codes.ok:
        return request.content

def get_courses_list(coursera_xml):
    coursera_tree_xml = etree.XML(coursera_xml)
    nodes = coursera_tree_xml.xpath('//*')
    return [e.text for e in coursera_tree_xml.iter('*') if e.text.startswith('http')]


def get_course_info(course_url):
    print(course_url)
    course_html = fetch_content(course_url)
    course_html_tree = BeautifulSoup(course_html, 'html.parser')
    #print(course_html_tree.prettify())
    course_name = course_html_tree.find('h1', {'class': 'title display-3-text'})
    print(course_name.text)
    course_language = course_html_tree.find('div', {'class': 'rc-Language'})
    print(course_language.text)
    course_startdate = course_html_tree.find('div', {'class': 'startdate rc-StartDateString caption-text'}).find('span')
    print(course_startdate.text)
    course_period = course_html_tree.find_all('div', {'class': 'week'})
    print(len(course_period))
    course_rating = course_html_tree.find('div', {'class': 'ratings-text bt3-visible-xs'})
    if not course_rating is None:
        print(course_rating.text)


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    coursera_xml_feed = 'https://www.coursera.org/sitemap~www~courses.xml'
    some_xml = fetch_content(coursera_xml_feed)
    url_courses_list = get_courses_list(some_xml)
    #print(url_courses_list)
    get_course_info(url_courses_list[0])
