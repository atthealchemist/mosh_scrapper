import json
import random
import time
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from pathlib import Path

import requests
from PyQt5.QtCore import pyqtSignal, QObject

from models.parser import Parser
from models.utils import Utils
from templates import wistia_json_url_template, download_lecture_from_course_template


class Downloader(QObject):

    completedSignal = pyqtSignal()
    progressSignal = pyqtSignal(int)
    errorSignal = pyqtSignal(str)
    logSignal = pyqtSignal(str)

    def log(self, message):
        self.logSignal.emit(message)
        print(message)

    def download_course(self, course):

        for idx, lecture in enumerate(course.lectures):
            if lecture.source != "":
                self.download_lecture(lecture, idx, course.title)

    def download_lecture(self, lecture, idx, course_title):
        response = requests.get(wistia_json_url_template.substitute(wistia_id=lecture.source))
        json_response = json.loads(Utils.get_json_from_callback(response.text))
        response.close()

        media = json_response["media"]

        ready_mp4_url = media["assets"][0]["url"]
        filename = f"{idx}. {lecture.title}.mp4"

        course_dir = Path("mosh_courses").resolve() / course_title

        file = requests.get(ready_mp4_url)
        print(download_lecture_from_course_template.substitute(lecture=filename, course=course_title, directory=course_dir))

        Utils.write_file(course_dir, filename, file.content)
        file.close()

    def download_metadata(self):
        self.log("First of all, I'll download all required metadata...")
        _courses = self.parser.parse_courses_list()
        course_count = len(_courses) if _courses else self.parser.get_courses_count()

        try:
            # Download courses metadata
            if _courses and len(_courses) > 0:
                for idx, course in enumerate(_courses):
                    # Course put
                    self.log(f'[{idx+1} of {len(_courses)}] Processing {course.id} - {course.title}')
                    self.course_queue.put(course)
                    self.log(f'put course {course.title} ({len(self.parser.parse_lectures_list(course.id))} lectures)')
                    for lecture in self.parser.parse_lectures_list(course.id):
                        # Lecture put
                        self.lect_queue.put(lecture)
                        self.log(f'put lecture {lecture.title}')
                        # Lecture get
                        while self.lect_queue.qsize() > 0:
                            idx = self.parser.get_lectures_count() - self.lect_queue.qsize()
                            lecture = self.lect_queue.get()
                            self.log(f'\t[{idx} of {self.parser.get_lectures_count()}] Course #{course.id} - {course.title} added lecture: {lecture.title} ')
                            course.lectures.append(lecture.dict())
                    # Course get
                    while self.course_queue.qsize() > 0:
                        course = self.course_queue.get()
                        idx = course_count - self.course_queue.qsize()
                        self.courses.append(course.dict())
                        self.progressSignal.emit(round(idx+1/course_count*100))
        except Exception as ex:
            self.errorSignal.emit(f'''[!] An exception was raised. Details:\n{ex}\n
            But i still have your downloaded data and saved it for you :)''')
        finally:
            Path('metadata.json').write_text(json.dumps(self.courses, indent=4))
            self.log("Saving loaded metadata to './metadata.json'")
            self.completedSignal.emit()


    def lectures_worker(self, course, queue):
        for lecture in self.parser.parse_lectures_list(course.get("id")):
            queue.put(lecture)
        while not queue.empty():
            lecture = queue.get()
            course.lectures.append(lecture.dict())
        time.sleep(random.randint(1, 5))
        return course

    def __init__(self):
        super(Downloader, self).__init__()
        self.courses = []
        self.parser = Parser()
        self.manager = Manager()
        self.course_queue = self.manager.Queue()
        self.lect_queue = self.manager.Queue()
