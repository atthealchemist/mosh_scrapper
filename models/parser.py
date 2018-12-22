import json
import re
from pathlib import Path

import requests
from lxml import html

from models.entities.Course import Course
from models.entities.Lecture import Lecture
from models.utils import Utils
from templates import course_url, course_lecture


class Parser:

    def get_lectures_count(self):
        return self.lectures_list_len

    def get_courses_count(self):
        return self.courses_list_len

    def parse_wistia_id(self, course_id, lecture_id):
        with self.session.get(course_lecture.substitute(course_id=course_id, lecture_id=lecture_id),
                              cookies=self.cookies, verify=False) as lecture:
            lxml = html.fromstring(html=lecture.content)
            wistia_ids = lxml.find_class('attachment-wistia-player')
            wistia_id = ''
            for _id in wistia_ids:
                wistia_id = _id.attrib['data-wistia-id']
            return wistia_id

    def parse_lectures_list(self, course_id):
        with self.session.get(course_url.substitute(course_id=course_id), cookies=self.cookies, verify=False) as course:
            lxml = html.fromstring(html=course.content)

            urls = [_url.attrib['href'] for _url in lxml.find_class('item')]
            lids = [Utils.get_id_from_url(_url) for _url in urls]
            titles = [Utils.flush(_title.text) for _title in lxml.find_class('lecture-name')]
            wids = [self.parse_wistia_id(course_id, _lid) for _lid in lids]
            durations = [_dur.attrib['aria-valuemax'] for _dur in lxml.find_class('w-player-wrapper')]

            lectures = [Lecture(_id=_id, title=_title, source=_wid, duration=_dur, path=_url) for
                        _id, _title, _wid, _dur, _url in zip(lids, titles, wids, durations, urls)]

            if self.lectures_list_len < 1:
                self.lectures_list_len = len(lectures)
            return lectures

    def parse_course(self, course_id):
        with self.session.get(f"https://codewithmosh.com/courses/enrolled/{course_id}", cookies=self.cookies,
                              verify=False) as course:
            soup = html.fromstring(html=course.content)
            title = soup.xpath("//h2")[0].text_content()
            lectures_ids = [_id.attrib['data-lecture-id'] for _id in soup.xpath("//*[@data-lecture-id]")]
            lectures = [next(self.parse_lecture_from_course(course_id, _lecture_id)) for _lecture_id in lectures_ids]
            course = Course(_id=course_id, title=title, lectures=lectures)
            yield course

    def parse_lecture_from_course(self, course_id, lecture_id):
        with self.session.get(f"https://codewithmosh.com/courses/{course_id}/lectures/{lecture_id}",
                              cookies=self.cookies, verify=False) as lecture:
            soup = html.fromstring(html=lecture.text)
            title = Utils.flush(soup.xpath("//h2")[1].text_content())
            url = soup.xpath("//*[contains(@class,'download')]")
            if len(url) < 1:
                yield Lecture(_id=lecture_id, title=title)
            yield Lecture(_id=lecture_id, title=title, path=url[0].attrib['href'] if 'href' in url[0].attrib else '')

    def parse_courses_ids(self):
        with self.session.get("https://codewithmosh.com/courses/", cookies=self.cookies, verify=False) as courses_list:
            soup = html.fromstring(html=courses_list.content)
            ids = [_id.attrib['data-course-id'] for _id in soup.find_class("course-listing")]
            if self.courses_list_len < 1:
                self.courses_list_len = len(ids)
            return ids[1:]

    def __init__(self):
        self.session = requests.Session()
        self.cookies = Utils.load_cookies()
        self.lectures_list_len = 0
        self.courses_list_len = 0
