from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets
import os
from src.webappmanager import updateIcon

class WebAppBrowser(QtWidgets.QWidget):
    def __init__(self, webapp):
        super().__init__()
        self.webapp = webapp
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.load(QtCore.QUrl(self.webapp.url))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.view)
        self.layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self.setWindowTitle(self.webapp.title)
        self.view.iconChanged.connect(self.iconChangedListener)

    @QtCore.Slot()
    def iconChangedListener(self, icon):
        pixmap = icon.pixmap(256, 256)
        path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation) + "/icons/"
        if not os.path.exists(path):
            os.makedirs(path)
        icon_path = path + self.webapp.id + ".png"
        pixmap.save(icon_path)
        updateIcon(self.webapp.id, icon_path)
        self.view.iconChanged.disconnect(self.iconChangedListener)
