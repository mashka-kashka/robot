from time import time, localtime, strftime
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot

from gestures.gestures_table_model import GesturesTableModel
from gestures.train_data_table_model import TrainDataTableModel
from gestures_window_ui import Ui_GesturesWindow


class GesturesWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.ui = Ui_GesturesWindow()
        self.ui.setupUi(self)

        self.table_model = GesturesTableModel()
        self.ui.tv_gestures.setModel(self.table_model)

        self.ui.cb_gestures.setModel(self.table_model)
        self.ui.cb_gestures.setModelColumn(GesturesTableModel.UNICODE_COLUMN)

        self.train_data_model = TrainDataTableModel()
        self.ui.tv_data.setModel(self.train_data_model)
        self.train_data_model.dataChanged.connect(self.on_data_changed)
        self.train_data_model.modelReset.connect(self.on_data_changed)

        self.scene = QGraphicsScene()
        self.ui.gv_palm.setScene(self.scene)
        self.scenePixmapItem = None

        self.logger = self.ui.teLog

        #self.scene = QGraphicsScene()
        #self.ui.gv_camera.setScene(self.scene)
        #self.scenePixmapItem = None

    def is_palm_visible(self):
        return not self.ui.gv_palm.visibleRegion().isEmpty()

    @pyqtSlot(object)
    def show_palm(self, image):
        _pixmap = QPixmap.fromImage(image)

        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(_pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scenePixmapItem.setZValue(0)
        else:
            self.scenePixmapItem.setPixmap(_pixmap)

        self.ui.gv_palm.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.gv_palm.show()

    def log(self, message, color):
        fmt = QTextFormat()
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.setTextColor(color)
        self.logger.append(strftime("%H:%M:%S : ", localtime()))
        self.logger.insertPlainText(message)

    @pyqtSlot()
    def on_add_sample(self):
        sample_index = self.ui.cb_gestures.currentIndex()
        self.train_data_model.add(sample_index, self.app.hand_results)

    @pyqtSlot()
    def on_new_data(self):
        if self.train_data_model.is_modified():
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Сохранить изменённые данные перед созданием новых?")
            dlg.setText("Данные изменены!")
            dlg.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()

            if button == QMessageBox.StandardButton.Yes:
                self.log("TODO: Сохранение изменённых данных", QColor(255,0,0))

        self.train_data_model.create()

    @pyqtSlot()
    def on_open_data(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Открыть файл данных для обучения модели",
            ".",
            "Текст CSV (*.csv);; Все файлы (*.*)",
        )
        if fname[0]:
            self.train_data_model.open(fname[0])

    @pyqtSlot()
    def on_save_data(self):
        filename = self.train_data_model.get_file_name()
        if filename:
            self.train_data_model.save(filename)
        else:
            self.on_save_data_as()

    @pyqtSlot()
    def on_save_data_as(self):
        fname = QFileDialog.getSaveFileName(
            self,
            "Открыть файл данных для обучения модели",
            ".",
            "Текст CSV (*.csv);; Все файлы (*.*)",
        )
        if fname[0]:
            self.train_data_model.save(fname[0])

    @pyqtSlot()
    def on_data_changed(self):
        self.ui.tb_save_data.setEnabled(self.train_data_model.is_modified())
        self.ui.tb_save_data_as.setEnabled(self.train_data_model.is_modified())
