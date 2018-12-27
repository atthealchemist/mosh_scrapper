import json
import random
import time
from multiprocessing import Manager
from pathlib import Path

import requests
from PyQt5.QtCore import pyqtSignal, QObject

from models.course_encoder import CourseEncoder
from models.parser import Parser
from models.utils import Utils
from templates import wistia_json_url_template, download_lecture_from_course_template


class Downloader(QObject):
    completedSignal = pyqtSignal()
    totalProgressSignal = pyqtSignal(int)
    errorSignal = pyqtSignal(str)
    logSignal = pyqtSignal(str)
    courseReadySignal = pyqtSignal(object)

    def log(self, message):
        self.logSignal.emit(message)
        print(message)

    def download_course(self, course):
        self.log(f"Downloading {course.title}...")
        for idx, lecture in enumerate(course.lectures):
            path = Path("mosh_courses") / course.title / f"{lecture.title}.mp4"
            if path.exists():
                print(f"{lecture.title}.mp4 is already downloaded, skipping...")
                continue
            if lecture.path != "":
                if "filepicker" in lecture.path:
                    self.log(
                        f"[{idx+1} of {len(course.lectures)}] Downloading lecture \"{lecture.title}\" from course \"{course.title}\"")
                    self.download_lecture_from_cdn(lecture, course.title)
                else:
                    self.log(
                        f"[{idx+1} of {len(course.lectures)}] Downloading lecture \"{lecture.title}\" from course \"{course.title}\"")
                    self.download_lecture_from_wistia(lecture, course.title)

    def download_lecture_from_cdn(selfs, lecture, course_title):
        filename = f"{lecture.title}.mp4"
        course_dir = Path("mosh_courses").resolve() / course_title
        file = requests.get(lecture.path)
        file_size = int(file.headers['Content-Length'])
        print(download_lecture_from_course_template.substitute(lecture=filename, course=course_title,
                                                               directory=course_dir, fileSize=file_size))
        Utils.write_file(course_dir, filename, file.content)
        file.close()

    def download_lecture_from_wistia(self, lecture, course_title):
        response = requests.get(wistia_json_url_template.substitute(wistia_id=lecture.source))
        json_response = json.loads(Utils.get_json_from_callback(response.text))
        response.close()

        media = json_response["media"]

        ready_mp4_url = media["assets"][0]["url"]
        filename = f"{lecture.title}.mp4"

        course_dir = Path("mosh_courses").resolve() / course_title

        file = requests.get(ready_mp4_url)
        print(download_lecture_from_course_template.substitute(lecture=filename, course=course_title,
                                                               directory=course_dir))

        Utils.write_file(course_dir, filename, file.content)
        file.close()

    def download_metadata(self):
        self.log("First of all, I'll download all required metadata...")

        try:
            # Download courses metadata
            for idx, cid in enumerate(self.parser.parse_courses_ids()):
                course = next(self.parser.parse_course(cid))
                self.log(
                    f'[{idx+1} of {self.parser.get_courses_count()}] Fetching metadata for {course.id} - {course.title} ({len(course.lectures)} lectures) finished!')
                self.courses.append(course.dict())
                self.courseReadySignal.emit(course)
                self.totalProgressSignal.emit(round(idx + 1 / self.parser.get_courses_count() * 100))

            self.completedSignal.emit()
        except Exception as ex:
            self.errorSignal.emit(f'''[!] An exception was raised. Details:\n{ex}\n
            But i still have your downloaded data and saved it for you :)''')
        finally:
            Path('metadata.json').write_text(json.dumps(self.courses, indent=4, cls=CourseEncoder))
            self.log("Saving loaded metadata to './metadata.json'")

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
