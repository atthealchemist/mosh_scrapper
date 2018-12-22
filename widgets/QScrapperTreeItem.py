from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTreeWidgetItem, QLabel, QCheckBox, QProgressBar


class QScrapperTreeItem(QTreeWidgetItem):

    @property
    def title(self):
        return self.text(0)

    @title.setter
    def title(self, text):
        self.setText(0, text)

    @property
    def duration(self):
        return self.itemDurationLabel.text()

    @duration.setter
    def duration(self, value):
        self.itemDurationLabel.setText(value)
    
    @property
    def path(self):
        return self.itemPathLabel.text()

    @path.setter
    def path(self, value):
        self.itemPathLabel.setText(value)

    @property
    def downloaded(self):
        return self.itemDownloadedCheckBox.isChecked()

    @downloaded.setter
    def downloaded(self, checked):
        self.itemDownloadedCheckBox.setChecked(checked)

    @property
    def progress(self):
        return self.itemProgressBar.value()

    @progress.setter
    def progress(self, value):
        self.itemProgressBar.setValue(value)

    def __init__(self, parent, entity):
        super(QScrapperTreeItem, self).__init__(parent)
        self.entity = entity

        # column 0 - Course/Lecture Title
        self.setText(0, entity.title)

        # column 1 - Duration
        self.itemDurationLabel = QLabel()
        self.itemDurationLabel.setText(f"{entity.duration} mins")
        # self.itemDurationLabel.setAlignment(Qt.AlignCenter)
        self.treeWidget().setItemWidget(self, 1, self.itemDurationLabel)

        # column 2 - Source
        self.itemSourceLabel = QLabel()
        self.itemSourceLabel.setOpenExternalLinks(True)
        self.itemSourceLabel.setText(f'<a href="{entity.source}">{entity.source}</a>')
        self.itemSourceLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # self.itemSourceLabel.setAlignment(Qt.AlignCenter)
        self.treeWidget().setItemWidget(self, 2, self.itemSourceLabel)


        # column 3 - Progress
        self.itemProgressBar = QProgressBar()
        self.itemProgressBar.setValue(0)
        self.treeWidget().setItemWidget(self, 3, self.itemProgressBar)


        # column 4 - Downloaded
        self.itemDownloadedCheckBox = QCheckBox()
        self.itemDownloadedCheckBox.setCheckable(False)
        self.itemDownloadedCheckBox.setContentsMargins(10, 0, 10, 0)
        self.treeWidget().setItemWidget(self, 4, self.itemDownloadedCheckBox)

        # column 5 - Path
        self.itemPathLabel = QLabel()
        self.itemPathLabel.setOpenExternalLinks(True)
        self.itemPathLabel.setText(f'<a href="{entity.path}">{entity.path}</a>')
        self.itemPathLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # self.itemPathLabel.setAlignment(Qt.AlignCenter)
        self.treeWidget().setItemWidget(self, 5, self.itemPathLabel)

        if self.downloaded:
            self.itemProgressBar.setVisible(False)

