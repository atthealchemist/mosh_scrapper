# -*- coding: utf-8 -*-
import json
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QMessageBox

from models.downloader import Downloader
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

        # self.treeWidgetCourses.resizeColumnToContents(2)
        # self.treeWidgetCourses.resizeColumnToContents(3)


        self.verticalLayout.addWidget(self.treeWidgetCourses)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayoutInfo = QtWidgets.QVBoxLayout()
        self.verticalLayoutInfo.setObjectName("verticalLayoutInfo")

        self.labelSelectedCourses = QtWidgets.QLabel(self.frame)

        font = QtGui.QFont()
        font.setPointSize(14)

        self.labelSelectedCourses.setFont(font)

        self.labelSelectedCourses.setObjectName("labelSelectedCourses")

        self.verticalLayoutInfo.addWidget(self.labelSelectedCourses)

        self.labelDownloadPath = QtWidgets.QLabel(self.frame)
        self.labelDownloadPath.setObjectName("labelDownloadPath")
        self.verticalLayoutInfo.addWidget(self.labelDownloadPath)
        self.horizontalLayout.addLayout(self.verticalLayoutInfo)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/usr/share/icons/Faenza/status/48/aptdaemon-download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDownloadCourses.setIcon(icon1)
        self.pushButtonDownloadCourses.setIconSize(QtCore.QSize(48, 48))
        self.pushButtonDownloadCourses.setAutoDefault(False)
        self.pushButtonDownloadCourses.setDefault(True)
        self.pushButtonDownloadCourses.setFlat(False)
        self.pushButtonDownloadCourses.setObjectName("pushButtonDownloadCourses")
        self.horizontalLayout.addWidget(self.pushButtonDownloadCourses)
        self.verticalLayout.addWidget(self.frame)
        self.groupBoxProgress = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxProgress.setObjectName("groupBoxProgress")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxProgress)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBarOverallProgress = QtWidgets.QProgressBar(self.groupBoxProgress)
        self.progressBarOverallProgress.setProperty("value", 0)
        self.progressBarOverallProgress.setObjectName("progressBarOverallProgress")
        self.horizontalLayout_2.addWidget(self.progressBarOverallProgress)
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
        self.labelSelectedCourses.setText(_translate("MainWindow", "Selected courses: 2 (~300 Mb)"))
        self.labelDownloadPath.setText(_translate("MainWindow", "Download path: ~/Downloads/Courses/"))
        self.pushButtonUpdateMetadata.setText(_translate("MainWindow", "Update metadata"))
        self.pushButtonDownloadCourses.setText(_translate("MainWindow", "Download courses (26)"))
        self.groupBoxProgress.setTitle(_translate("MainWindow", "Overall progress:"))

    def addTreeItem(self, entity, parent, checkable=False):
        treeItem = QScrapperTreeItem(parent, entity)
        if checkable:
            treeItem.setFlags(treeItem.flags() | Qt.ItemIsUserCheckable)
        if entity.lectures:
            for item in entity.lectures:
                newChild = QScrapperTreeItem(treeItem, item)
                newChild.downloaded = False
                treeItem.addChild(newChild)
        if type(parent) is QTreeWidgetItem:
            treeItem.downloaded = False
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
                    l = Lecture(_id=lecture.get('id'), title=f"{idx}. {lecture.get('title')}", source=lecture.get('source'))
                    c.lectures.append(l)
                self.addTreeItem(c, self.treeWidgetCourses, True)
        else:
            self.downloader.download_metadata()

    def onUpdateMetadata(self):
        self.loadMetadata()

    def onUpdateProgress(self, value):
        self.progressBarOverallProgress.setValue(value)

    def onExceptionRaise(self, message):
        QMessageBox.warning(self, "Exception!", message)

    def onCompletedTask(self):
        QMessageBox.information(parent=self, title='Info', text="Task completed!")
        self.log("Task completed!")

    def log(self, message):
        self.statusBar().showMessage(message)

    def __init__(self):
        super().__init__()
        super(MoshScrapperWindow, self).__init__()
        self.setupUi()

        self.downloader = Downloader()

        self.downloader.progressSignal.connect(self.onUpdateProgress)
        self.downloader.errorSignal.connect(self.onExceptionRaise)
        self.downloader.completedSignal.connect(self.onCompletedTask)
        self.downloader.logSignal.connect(self.log)

        self.pushButtonUpdateMetadata.clicked.connect(self.onUpdateMetadata)
