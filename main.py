#!/usr/bin/env python3
import sys
from PySide2 import QtCore, QtWidgets, QtGui
import argparse
import signal
from src.webappmanager import initDB, getWebapps, getWebapp, addWebApp
from src.webappBrowser import WebAppBrowser

class AppWidget(QtWidgets.QVBoxLayout):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.button = QtWidgets.QPushButton()
        self.button.size = 100
        self.button.setFixedSize(QtCore.QSize(self.button.size,self.button.size))
        self.button.setObjectName("appButton")
        icon = QtGui.QIcon(app.icon_path)
        if icon.pixmap(256, 256).size().height() < self.button.size:
            self.button.setStyleSheet('QPushButton#appButton { background-image: url("' + app.icon_path + '"); }')
        else:
            self.button.setStyleSheet('QPushButton#appButton {border-image: url("' + app.icon_path + '") 0 0 0 0 stretch stretch; }')
        self.button.clicked.connect(self.launch)
        self.addWidget(self.button, alignment=QtGui.Qt.AlignCenter)
        self.label = QtWidgets.QLabel()
        self.label.setText(app.title)
        self.label.setAlignment(QtGui.Qt.AlignCenter)
        self.addWidget(self.label)

    @QtCore.Slot()
    def launch(self):
        self.browser = WebAppBrowser(self.app)
        self.browser.show()


class AppSelector(QtWidgets.QWidget):
    def __init__(self, apps):
        super().__init__()
        self.setObjectName("appSelector")
        self.apps = apps
        self.layout = QtWidgets.QGridLayout(self)
        self.app_buttons = []
        counter = 0
        for app in self.apps:
            button = AppWidget(app)
            self.layout.addLayout(button,counter//4,counter%4,alignment=QtCore.Qt.AlignTop)
            self.app_buttons.append(button)
            counter += 1


class AddWAPDialog(QtWidgets.QWidget):
    added = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.nameField = QtWidgets.QLineEdit()
        self.titleField = QtWidgets.QLineEdit()
        self.urlField = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("Add Webapp")
        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow("ID:", self.nameField)
        self.layout.addRow("Title:", self.titleField)
        self.layout.addRow("URL:", self.urlField)
        self.layout.addWidget(self.button)
        self.nameField.returnPressed.connect(self.add_wap)
        self.titleField.returnPressed.connect(self.add_wap)
        self.urlField.returnPressed.connect(self.add_wap)
        self.button.clicked.connect(self.add_wap)

    @QtCore.Slot()
    def add_wap(self):
        wap_id = self.nameField.text()
        title = self.titleField.text()
        url = self.urlField.text()
        wap = addWebApp(wap_id, title, url)
        WebAppBrowser(wap)
        self.added.emit()
        self.close()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")

        self.button = QtWidgets.QPushButton("Add WAP!")
        self.appSelector = AppSelector(getWebapps())

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.appSelector)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.add_dialog = AddWAPDialog()
        self.add_dialog.resize(800, 600)
        self.add_dialog.added.connect(self.refresh)
        self.add_dialog.show()

    @QtCore.Slot()
    def refresh(self):
        oldAppSelector = self.appSelector
        self.appSelector = AppSelector(getWebapps())
        oldAppSelector.deleteLater()
        self.layout.replaceWidget(oldAppSelector, self.appSelector)



if __name__ == "__main__":
    QtCore.QCoreApplication.setOrganizationName("RasmusRendal")
    QtCore.QCoreApplication.setApplicationName("Webappifier")
    app = QtWidgets.QApplication([])
    stylesheet_file = open("stylesheet.css", "r")
    stylesheet = stylesheet_file.read()
    stylesheet_file.close()
    app.setStyleSheet(stylesheet)
    initDB()
    parser = argparse.ArgumentParser("Webapp fun")
    parser.add_argument("--app", dest='app', nargs='?', help='Title of webapp to launch')
    args = parser.parse_args()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if args.app != None:
        selectedWebApp = getWebapp(args.app)
        widget = WebAppBrowser(selectedWebApp)
        widget.show()
        sys.exit(app.exec_())
    else:
        widget = MainWindow()
        widget.show()
        sys.exit(app.exec_())
