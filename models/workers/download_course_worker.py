from PyQt5.QtCore import QRunnable

from models.downloader import Downloader


class DownloadCourseWorker(QRunnable):

    def run(self):
        if type(self.courses) == 'list':
            if len(self.courses) > 1:
                for course in self.courses:
                    self.downloader.download_course(course)
        else:
            self.downloader.download_course(course=self.courses)

    def __init__(self, courses, *args, **kwargs):
        QRunnable.__init__(self, *args, **kwargs)
        self.downloader = Downloader()
        self.courses = courses