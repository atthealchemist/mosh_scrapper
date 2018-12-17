import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PyQt5.QtWidgets import QApplication

from views.mosh_scrapper_window import MoshScrapperWindow


def main():
    app = QApplication(sys.argv)
    window = MoshScrapperWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
