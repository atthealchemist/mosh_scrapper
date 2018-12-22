from PyQt5.QtCore import QRunnable

from models.downloader import Downloader


class DownloadLectureWorker(QRunnable):

    def run(self):
        self.downloader.download_lecture_from_wistia(self.lecture, course_title=self.course_title)

    def __init__(self, lecture, course_title='', *args, **kwargs, ):
        QRunnable.__init__(self, *args, **kwargs)
        self.downloader = Downloader()
        self.lecture = lecture
        self.course_title=course_title