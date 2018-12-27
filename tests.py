import unittest
from collections import Counter
from pathlib import Path

from models.entities.Course import Course
from models.entities.Lecture import Lecture
from models.workers.download_course_worker import DownloadCourseWorker
from models.workers.download_lecture_worker import DownloadLectureWorker


class MoshScrapperDownloadingTestCase(unittest.TestCase):

    def setUp(self):
        self.testLecture = Lecture(_id=5634517, title='What is React', path="https://www.filepicker.io/api/file/mgEFvQOWSpKTPdJirMWK")
        self.testAnotherLecture = Lecture(_id=5634521, title='Setting Up the Development Environment', path="https://www.filepicker.io/api/file/mjHnm51CQVu7pFaW6wPD")
        self.testCourse = Course(_id=357787, title='Mastering React', lectures=[self.testLecture])

        self.lectureWorker = DownloadLectureWorker(lecture=self.testLecture, course_title='single')
        self.twoLecturesWorker = DownloadLectureWorker(lecture=[self.testLecture, self.testAnotherLecture], course_title='double')
        self.courseWorker = DownloadCourseWorker(courses=self.testCourse)

        self.lectureTestPath = Path("mosh_courses") / "single" / "What is React.mp4"
        self.twoLecturesTestPath = Path("mosh_courses") / "double"
        self.courseTestPath = Path("mosh_courses") / "Mastering React" / "What is React.mp4"

    @unittest.skip("test_downloading_two_more_lectures passed")
    def test_downloading_two_more_lectures(self):
        self.twoLecturesWorker.run()
        if self.twoLecturesWorker.workCompleted:
            count = Counter(p.suffix for p in self.twoLecturesTestPath.iterdir())
            self.assertEqual(count['.mp4'], 2)

    @unittest.skip("test_downloading_lecture passed")
    def test_downloading_lecture(self):
        self.lectureWorker.run()
        if self.lectureWorker.workCompleted:
            print(f"{self.lectureTestPath}: {self.lectureTestPath.is_file()}")
            self.assertTrue(self.lectureTestPath.is_file(), True)

    @unittest.skip("test_downloading_course passed")
    def test_downloading_course(self):
        self.courseWorker.run()
        if self.courseWorker.workCompleted:
            print(f"{self.lectureTestPath}: {self.lectureTestPath.is_file()}")
            self.assertTrue(self.courseTestPath.is_file(), True)
