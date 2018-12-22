# -*- coding: utf-8 -*-
import json
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMessageBox, QAbstractItemView

from models.workers.download_course_worker import DownloadCourseWorker
from models.workers.download_metadata_worker import MetadataWorker
from models.entities.Course import Course
from models.entities.Lecture import Lecture
from widgets.QScrapperTreeItem import QScrapperTreeItem


class MoshScrapperWindow(QMainWindow):

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setWindowState(Qt.WindowMaximized)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.treeWidgetCourses = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidgetCourses.setUniformRowHeights(False)
        self.treeWidgetCourses.setItemsExpandable(True)
        self.treeWidgetCourses.setAllColumnsShowFocus(False)
        self.treeWidgetCourses.setHeaderHidden(False)
        self.treeWidgetCourses.setObjectName("treeWidgetCourses")

        self.treeWidgetCourses.header().setDefaultSectionSize(150)
        self.treeWidgetCourses.header().setMinimumSectionSize(50)
        self.treeWidgetCourses.header().setStretchLastSection(True)

        self.treeWidgetCourses.setColumnWidth(0, 200)
        self.treeWidgetCourses.setColumnWidth(5, 150)

        self.treeWidgetCourses.setSelectionMode(QAbstractItemView.MultiSelection)

        # self.treeWidgetCourses.resizeColumnToContents(2)
        # self.treeWidgetCourses.resizeColumnToContents(3)


        self.verticalLayout.addWidget(self.treeWidgetCourses)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.gridLayoutInfo = QtWidgets.QGridLayout()
        self.gridLayoutInfo.setObjectName("gridLayoutInfo")

        font = QtGui.QFont()
        font.setPointSize(14)

        self.labelSelectedCourses = QtWidgets.QLabel(self.frame)
        self.labelSelectedCourses.setFont(font)
        self.labelSelectedCourses.setObjectName("labelSelectedCourses")
        self.gridLayoutInfo.addWidget(self.labelSelectedCourses)
        self.gridLayoutInfo.addWidget(self.labelSelectedCourses, 0, 0, 1, 1)

        self.labelDownloadPath = QtWidgets.QLabel(self.frame)
        self.labelDownloadPath.setObjectName("labelDownloadPath")
        self.gridLayoutInfo.addWidget(self.labelDownloadPath, 1, 0, 1, 1)

        self.labelSelectedCoursesValue = QtWidgets.QLabel(self.frame)
        self.labelSelectedCoursesValue.setText("")
        self.labelSelectedCoursesValue.setObjectName("labelSelectedCoursesValue")
        self.gridLayoutInfo.addWidget(self.labelSelectedCoursesValue, 0, 1, 1, 1)

        self.labelDownloadPathValue = QtWidgets.QLabel(self.frame)
        self.labelDownloadPathValue.setText("")
        self.labelDownloadPathValue.setObjectName("labelDownloadPathValue")
        self.gridLayoutInfo.addWidget(self.labelDownloadPathValue, 1, 1, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayoutInfo)

        self.pushButtonUpdateMetadata = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButtonUpdateMetadata.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/usr/share/icons/Faenza/status/48/aptdaemon-update-cache.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUpdateMetadata.setIcon(icon)
        self.pushButtonUpdateMetadata.setIconSize(QtCore.QSize(48, 48))
        self.pushButtonUpdateMetadata.setDefault(True)
        self.pushButtonUpdateMetadata.setObjectName("pushButtonUpdateMetadata")
        self.horizontalLayout.addWidget(self.pushButtonUpdateMetadata)
        self.pushButtonDownloadCourses = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButtonDownloadCourses.setFont(font)
        downloadCoursesIcon = QtGui.QIcon()
        downloadCoursesIcon.addPixmap(QtGui.QPixmap("/usr/share/icons/Faenza/status/48/aptdaemon-download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDownloadCourses.setIcon(downloadCoursesIcon)
        self.pushButtonDownloadCourses.setIconSize(QtCore.QSize(48, 48))
        self.pushButtonDownloadCourses.setAutoDefault(False)
        self.pushButtonDownloadCourses.setDefault(True)
        self.pushButtonDownloadCourses.setFlat(False)
        self.pushButtonDownloadCourses.setObjectName("pushButtonDownloadCourses")
        self.horizontalLayout.addWidget(self.pushButtonDownloadCourses)
        self.verticalLayout.addWidget(self.frame)

        self.groupBoxProgress = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxProgress.setObjectName("groupBoxProgress")

        self.horizontalLayoutProgressBar = QtWidgets.QHBoxLayout(self.groupBoxProgress)
        self.horizontalLayoutProgressBar.setObjectName("horizontalLayoutProgressBar")
        self.progressBarOverallProgress = QtWidgets.QProgressBar(self.groupBoxProgress)
        self.progressBarOverallProgress.setProperty("value", 0)
        self.progressBarOverallProgress.setObjectName("progressBarOverallProgress")
        self.horizontalLayoutProgressBar.addWidget(self.progressBarOverallProgress)

        self.verticalLayout.addWidget(self.groupBoxProgress)
        self.setCentralWidget(self.centralwidget)

        self.statusBar().showMessage("Ready")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "CoursesScraper"))
        self.treeWidgetCourses.headerItem().setText(0, _translate("MainWindow", "Title"))
        self.treeWidgetCourses.headerItem().setText(1, _translate("MainWindow", "Duration"))
        self.treeWidgetCourses.headerItem().setText(2, _translate("MainWindow", "Source"))
        self.treeWidgetCourses.headerItem().setText(3, _translate("MainWindow", "Progress"))
        self.treeWidgetCourses.headerItem().setText(4, _translate("MainWindow", "Downloaded"))
        self.treeWidgetCourses.headerItem().setText(5, _translate("MainWindow", "Path"))
        __sortingEnabled = self.treeWidgetCourses.isSortingEnabled()
        self.treeWidgetCourses.setSortingEnabled(False)
        self.treeWidgetCourses.setSortingEnabled(__sortingEnabled)
        self.labelSelectedCourses.setText(_translate("MainWindow", "Selected courses:"))
        self.labelDownloadPath.setText(_translate("MainWindow", "Download path:"))
        self.pushButtonUpdateMetadata.setText(_translate("MainWindow", "Update metadata"))
        self.pushButtonDownloadCourses.setText(_translate("MainWindow", "Download courses (26)"))
        self.groupBoxProgress.setTitle(_translate("MainWindow", "Overall progress:"))

    def addTreeItem(self, entity, parent, checkable=False, ready=False):
        treeItem = QScrapperTreeItem(parent, entity)
        if checkable:
            treeItem.setFlags(treeItem.flags() | Qt.ItemIsUserCheckable)
        if entity.lectures:
            for item in entity.lectures:
                newChild = QScrapperTreeItem(treeItem, item)
                newChild.downloaded = ready
                treeItem.addChild(newChild)
        if type(parent) is QTreeWidgetItem:
            treeItem.downloaded = ready
            parent.addChild(treeItem)
        # else:
        #     parent.addTopLevelItem(newItem)
        return treeItem

    def loadMetadata(self):
        if Path('metadata.json').exists():
            metadata = json.loads(Path('metadata.json').read_text())
            for course in metadata:
                c = Course(_id=course.get('id'), title=course.get('title'))
                for idx, lecture in enumerate(course.get('lectures')):
                    l = Lecture(_id=lecture.get('id'), title=f"{idx}. {lecture.get('title')}", path=lecture.get('path'))
                    c.lectures.append(l)
                self.addTreeItem(c, self.treeWidgetCourses, True)
        else:
            QThreadPool.globalInstance().start(self.metadataWorker)

    def onUpdateMetadata(self):
        self.loadMetadata()

    def onUpdateProgress(self, value):
        self.progressBarOverallProgress.setValue(value)

    def onExceptionRaise(self, message):
        QMessageBox.warning(self, "Exception!", message)
        self.close()
        raise Exception(message)


    def onCompletedTask(self):
        QMessageBox.information(self, 'Info', "Task completed!")
        self.log("Task completed!")

    def onAppendCourse(self, entity):
        self.addTreeItem(entity, self.treeWidgetCourses, True)

    def onCoursesDownload(self):
        for item in self.treeWidgetCourses.selectedItems():
            self.courseWorker = DownloadCourseWorker(courses=item.entity)
            QThreadPool.globalInstance().start(self.courseWorker)

    def onItemSelectionChanged(self):
        totalLecturesCount = 0
        for item in self.treeWidgetCourses.selectedItems():
            if hasattr(item.entity, 'lectures'):
                totalLecturesCount += len(item.entity.lectures)
            else:
                totalLecturesCount += 1
        self.pushButtonDownloadCourses.setText(f"Download ({totalLecturesCount})")

    def log(self, message):
        self.statusBar().showMessage(message)

    def __init__(self):
        super().__init__()
        super(MoshScrapperWindow, self).__init__()
        self.setupUi()

        self.metadataWorker = MetadataWorker()

        self.metadataWorker.downloader.courseReadySignal.connect(self.onAppendCourse)
        self.metadataWorker.downloader.totalProgressSignal.connect(self.onUpdateProgress)
        self.metadataWorker.downloader.errorSignal.connect(self.onExceptionRaise)
        self.metadataWorker.downloader.completedSignal.connect(self.onCompletedTask)
        self.metadataWorker.downloader.logSignal.connect(self.log)

        self.pushButtonUpdateMetadata.clicked.connect(self.onUpdateMetadata)

        self.pushButtonDownloadCourses.clicked.connect(self.onCoursesDownload)

        self.treeWidgetCourses.itemSelectionChanged.connect(self.onItemSelectionChanged)
