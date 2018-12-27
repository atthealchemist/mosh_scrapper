from PyQt5.QtCore import QRunnable

from models.downloader import Downloader


class DownloadLectureWorker(QRunnable):

    def run(self):
        if self.lecture.__class__.__name__ == 'list' or len(self.lecture) > 1:
            for item in self.lecture:
                self.downloader.download_lecture_from_cdn(item, course_title=self.course_title)
        else:
            self.downloader.download_lecture_from_cdn(self.lecture, course_title=self.course_title)
        self.workCompleted = True

    def __init__(self, lecture, course_title='', *args, **kwargs, ):
        QRunnable.__init__(self, *args, **kwargs)
        self.downloader = Downloader()
        self.lecture = lecture
        self.course_title = course_title
        self.workCompleted = False
