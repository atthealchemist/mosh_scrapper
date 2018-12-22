from PyQt5.QtCore import QRunnable

from models.downloader import Downloader


class MetadataWorker(QRunnable):

    def run(self):
        self.downloader.download_metadata()

    def __init__(self, *args, **kwargs):
        QRunnable.__init__(self, *args, **kwargs)
        self.downloader = Downloader()