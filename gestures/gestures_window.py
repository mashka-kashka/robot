from random import sample
from time import time, localtime, strftime
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot, QModelIndex
from tensorflow.python.ops.gen_batch_ops import batch
from sklearn.model_selection import train_test_split
from gestures.gestures_table_model import GesturesTableModel
from gestures.train_data_table_model import TrainDataTableModel
from gestures_window_ui import Ui_GesturesWindow
import torch

class GesturesWindow(QMainWindow):
    TRAIN_TAB=2

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.ui = Ui_GesturesWindow()
        self.ui.setupUi(self)

        self.gestures_data_model = GesturesTableModel()
        self.ui.tv_gestures.setModel(self.gestures_data_model)

        self.ui.cb_gestures.setModel(self.gestures_data_model)
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
        sample_index = self.ui.cb_gestures.currentData(Qt.ItemDataRole.UserRole)
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

    @pyqtSlot()
    def on_edit_sample(self):
        sample_index = self.ui.tv_data.currentIndex()
        if not sample_index.isValid():
            return
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Изменение жеста")
        idx = sample_index.siblingAtColumn(self.train_data_model.GESTURE)
        gesture_index = int(self.train_data_model.data(idx, Qt.ItemDataRole.DisplayRole))
        if self.ui.cb_gestures.currentIndex() > 0:
            dlg.setText(f"Заменить жест {self.gestures_data_model.get_unicode(gesture_index) or ''} на {self.ui.cb_gestures.currentText()}?")
        else:
            dlg.setText(f"Заменить жест {self.gestures_data_model.get_unicode(gesture_index) or ''} на неопределённый?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setStyleSheet('font: "Noto Color Emoji";')
        dlg.setIconPixmap(self.train_data_model.draw_palm(sample_index.row(), 100))
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.train_data_model.setData(idx, self.ui.cb_gestures.currentIndex(), Qt.ItemDataRole.EditRole)
            self.train_data_model.dataChanged.emit(idx,idx)

    @pyqtSlot()
    def on_delete_sample(self):
        sample_index = self.ui.tv_data.currentIndex()
        if not sample_index.isValid():
            return
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удаление жеста")
        idx = sample_index.siblingAtColumn(self.train_data_model.GESTURE)
        gesture_index = int(self.train_data_model.data(idx, Qt.ItemDataRole.DisplayRole))
        if self.ui.cb_gestures.currentIndex() > 0:
            dlg.setText(
                f"Вы действительно хотите удалить жест {self.gestures_data_model.get_unicode(gesture_index) or ''}?")
        else:
            dlg.setText(f"Вы действительно хотите удалить неопределённый жест?")
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setStyleSheet('font: "Noto Color Emoji";')
        dlg.setIconPixmap(self.train_data_model.draw_palm(sample_index.row(), 100))
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.train_data_model.removeRow(sample_index.row())

    @pyqtSlot()
    def on_double_clicked_sample(self, index):
        self.on_edit_sample()

    @pyqtSlot(int)
    def on_tab_changed(self, tab):
        if tab == self.TRAIN_TAB:
            self.ui.tb_train.setEnabled(self.train_data_model.rowCount(None) > 0)

    @pyqtSlot()
    def on_train_model(self):
        try:
            _test_size = float(self.ui.le_test_size.text())
            _X = self.train_data_model.X() # Данные
            _y = self.train_data_model.y() # Метки
            _X_train, _X_test, _y_train, _y_test = train_test_split(
                _X, _y, test_size=_test_size, random_state=42, shuffle=True)

            _X_train_tensor = torch.tensor(_X_train.values)
            _y_train_tensor = torch.tensor(_y_train.values).reshape(_y_train.shape[0],1)
            _train_data = torch.hstack((_X_train_tensor, _y_train_tensor))

            _X_test_tensor = torch.tensor(_X_test.values)
            _y_test_tensor = torch.tensor(_y_test.values).reshape(_y_test.shape[0],1)
            _test_data = torch.hstack((_X_test_tensor, _y_test_tensor))

            _batch_size = int(self.ui.le_batch_size.text())
            _train_loader = torch.utils.data.DataLoader(_train_data, batch_size=_batch_size, shuffle=True)
            _test_loader = torch.utils.data.DataLoader(_test_data, batch_size=_batch_size, shuffle=True)

            _epochs = int(self.ui.le_epochs.text())
            _learning_rate = float(self.ui.le_learning_rate.text())
        except Exception as e:
            self.log(f"Ошибка обучения модели: {e}", QColor(200,0,0))


