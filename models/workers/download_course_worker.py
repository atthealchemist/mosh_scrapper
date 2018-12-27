from PyQt5.QtCore import QRunnable

from models.downloader import Downloader


class DownloadCourseWorker(QRunnable):

    def run(self):
        if self.courses.__class__.__name__ == 'Lecture':
            self.downloader.download_lecture_from_cdn(self.courses, 'single')
            return
        if self.courses.__class__.__name__ == 'list':
            if len(self.courses) > 1:
                for course in self.courses:
                    self.downloader.download_course(course)
        else:
            self.downloader.download_course(course=self.courses)
        self.workCompleted = True

    def __init__(self, courses, *args, **kwargs):
        QRunnable.__init__(self, *args, **kwargs)
        self.downloader = Downloader()
        self.courses = courses
        self.workCompleted = False