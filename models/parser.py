import json
from pathlib import Path

import requests
from lxml import html

from models.entities.Course import Course
from models.entities.Lecture import Lecture
from models.utils import Utils
from templates import course_url, course_lecture


class Parser:

    def get_lectures_count(self):
        return self.lections_list_len

    def get_courses_count(self):
        return self.courses_list_len

    def parse_wistia_id(self, course_id, lecture_id):
        with self.session.get(course_lecture.substitute(course_id=course_id, lecture_id=lecture_id),
                              cookies=self.cookies, verify=False) as lecture:
            soup = html.fromstring(html=lecture.content)
            wistia_id = ''
            for _id in soup.find_class("attachment-wistia-player"):
                wistia_id = _id.attrib['data-wistia-id']
            return wistia_id

    def parse_lectures_list(self, course_id):
        with self.session.get(course_url.substitute(course_id=course_id), cookies=self.cookies, verify=False) as course:
            soup = html.fromstring(html=course.content)

            urls = [_url.attrib['href'] for _url in soup.find_class('item')]
            lids = [Utils.get_id_from_url(_url) for _url in urls]
            titles = [Utils.flush(_title.text) for _title in soup.find_class('lecture-name')]
            wids = [self.parse_wistia_id(course_id, _lid) for _lid in lids]
            durations = [_dur.attrib['aria-valuemax'] for _dur in soup.find_class('w-player-wrapper')]

            lectures = [Lecture(_id=_id, title=_title, source=_wid, duration=_dur, path=_url) for
                        _id, _title, _wid, _dur, _url in zip(lids, titles, wids, durations, urls)]

            self.lections_list_len = len(lectures)
            return lectures

    def parse_courses_list(self):
        with self.session.get("https://codewithmosh.com/courses/", cookies=self.cookies, verify=False) as courses_list:
            soup = html.fromstring(html=courses_list.content)

            titles = [Utils.flush(_title.text_content()) for _title in soup.find_class("course-listing-title")]
            ids = [_id.attrib['data-course-id'] for _id in soup.find_class("course-listing")]

            courses = [Course(_id=_id, title=Utils.flush(_title)) for _id, _title in zip(ids, titles)]
            self.courses_list_len = len(courses)
            return courses

    def __init__(self):
        self.session = requests.Session()
        self.cookies = Utils.load_cookies()
        self.lections_list_len = 0
        self.courses_list_len = 0
