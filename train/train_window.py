from random import sample
from time import time, localtime, strftime
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap, QIcon, QPainter, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot, QModelIndex, QPoint
from tensorflow.python.ops.gen_batch_ops import batch
from sklearn.model_selection import train_test_split

from train.gestures_dataset import GesturesDataset
from train.gestures_model import GesturesNet
from train.gestures_table_model import GesturesTableModel
from train.train_data_table_model import TrainDataTableModel
from train_window_ui import Ui_TrainWindow

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data

class TrainWindow(QMainWindow):
    TRAIN_TAB=2

    label_font = QFont("Times", 20)
    emoji_font = QFont("Noto Color Emoji", 64)

    def __init__(self, app):
        super().__init__()

        self.app = app

        # Интерфейс
        self.ui = Ui_TrainWindow()
        self.ui.setupUi(self)

        self.palm_pixmap = None
        self.palm_scene = QGraphicsScene()
        self.ui.gv_palm.setScene(self.palm_scene)
        self.classification_scene = QGraphicsScene()
        self.ui.gv_classification.setScene(self.classification_scene)

        self.logger = self.ui.teLog

        # Модель списка жестов
        self.gestures_data_model = GesturesTableModel()
        self.ui.tv_gestures.setModel(self.gestures_data_model)
        self.ui.cb_gestures.setModel(self.gestures_data_model)
        self.ui.cb_gestures.setModelColumn(GesturesTableModel.UNICODE_COLUMN)

        # Модель таблицы данных для обучения
        self.train_data_model = TrainDataTableModel()
        self.ui.tv_data.setModel(self.train_data_model)
        self.train_data_model.dataChanged.connect(self.on_data_changed)
        self.train_data_model.modelReset.connect(self.on_data_changed)

        # Нейронная сеть для распознавания жестов
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.gestures_model = None

    def is_palm_visible(self):
        return not self.ui.gv_palm.visibleRegion().isEmpty()

    @pyqtSlot(object)
    def show_palm(self, image, results):
        # Активна вкладка "Распознавание"
        if self.gestures_model and self.ui.tabClassification.isVisible():
            try:
                sample = self.train_data_model.get_sample(results)
                if sample:
                    input = torch.tensor(sample).double().to(self.device)
                    self.gestures_model.eval()
                    prediction = self.gestures_model(input)
                    #prediction = F.softmax(prediction)
                    score = max(prediction)
                    ids = self.train_data_model.get_gestures_ids()
                    gesture = ids[prediction.argmax()]
                    gesture = self.gestures_data_model.get_unicode_by_id(gesture)

                    painter = QPainter(image)
                    painter.setPen(QColor(255, 255, 255))
                    painter.setFont(self.label_font)
                    painter.drawText(QPoint(5, 25), f"Уверенность: {score:.4f}")
                    #if score > 0.7:
                    painter.setFont(self.emoji_font)
                    painter.drawText(QPoint(5, 100), f"{gesture}")
            except Exception as e:
                print(e)

        _pixmap = QPixmap.fromImage(image)

        if self.palm_pixmap is None:
            self.palm_pixmap = QGraphicsPixmapItem(_pixmap)
            self.palm_pixmap.setZValue(0)
        else:
            self.palm_pixmap.setPixmap(_pixmap)

        # Активнка вкладка "Распознавание"
        if self.ui.tabClassification.isVisible():
            if len(self.classification_scene.items()) == 0:
                self.classification_scene.addItem(self.palm_pixmap)
            self.ui.gv_classification.fitInView(self.classification_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.gv_classification.show()

        # Активна вкладка "Данные"
        elif self.ui.tabData.isVisible():
            # if results.multi_handedness:
            #     handedness_dict = MessageToDict(self.hand_results.multi_handedness[0])
            #     classification = handedness_dict['classification'][0]
            #     painter = QPainter(image)
            #     painter.setPen(QColor(255, 255, 255))
            #     painter.setFont(self.label_font)
            #     painter.drawText(QPoint(5, 25), f"Уверенность: {classification['score']}")
            #     hand = classification['label']
            #     if hand == "Left":
            #         hand = "Правая"  # Зеркальное искажение
            #     else:
            #         hand = "Левая"
            #     painter.drawText(QPoint(5, 55), hand)
            #     painter.drawText(QPoint(5, 85), f"X: {min_x:.2f} {max_x:.2f}")
            #     painter.drawText(QPoint(5, 115), f"Y: {min_y:.2f} {max_y:.2f}")
            #     painter.drawText(QPoint(5, 145), f"Z: {min_z:.2f} {max_z:.2f}")
            #
            #     # painter.setFont(self.emoji_font)
            #     # painter.drawText(QPoint(5, 140), "👍")
            #
            #     painter.end()
            if len(self.palm_scene.items()) == 0:
                self.palm_scene.addItem(self.palm_pixmap)
            self.ui.gv_palm.fitInView(self.palm_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
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
            self.ui.tb_train_model.setEnabled(self.train_data_model.rowCount(None) > 0)

    @pyqtSlot()
    def on_train_model(self):
        try:
            labels = self.train_data_model.get_gestures_ids()
            if not self.gestures_model or not all(x == y for x, y in zip(labels, self.gestures_model.labels)):
                self.gestures_model = GesturesNet(labels).to(self.device)

            # Разделение полного набора данных на обучающий и тестовых наборы
            test_size = float(self.ui.le_test_size.text())
            X = self.train_data_model.X() # Данные
            y = self.train_data_model.y() # Метки
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, shuffle=True)

            # Наборы обучающих и тестовых данных
            train_data = GesturesDataset(X_train, y_train)
            test_data = GesturesDataset(X_test, y_test)

            # Загрузчики наборов данных
            batch_size = int(self.ui.le_batch_size.text())
            train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True, )
            val_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=True)

            # Оптимизатор
            learning_rate = float(self.ui.le_learning_rate.text())
            optimizer = optim.Adam(self.gestures_model.parameters(), lr=learning_rate)

            # Обучение
            loss_fn = torch.nn.CrossEntropyLoss()
            epochs = int(self.ui.le_epochs.text())
            for epoch in range(1, epochs + 1):
                training_loss = 0.0
                valid_loss = 0.0
                self.gestures_model.train()
                for batch in train_loader:
                    optimizer.zero_grad()
                    inputs, targets = batch
                    inputs = inputs.to(self.device)
                    targets = targets.to(self.device)
                    output = self.gestures_model(inputs)
                    loss = loss_fn(output, targets)
                    loss.backward()
                    optimizer.step()
                    training_loss += loss.data.item() * inputs.size(0)
                training_loss /= len(train_loader.dataset)

                self.gestures_model.eval()
                num_correct = 0
                num_examples = 0
                for batch in val_loader:
                    inputs, targets = batch
                    inputs = inputs.to(self.device)
                    output = self.gestures_model(inputs)
                    targets = targets.to(self.device)
                    loss = loss_fn(output, targets)
                    valid_loss += loss.data.item() * inputs.size(0)
                    correct = torch.eq(torch.max(F.softmax(output, dim=1), dim=1)[1], targets)
                    num_correct += torch.sum(correct).item()
                    num_examples += correct.shape[0]
                valid_loss /= len(val_loader.dataset)

                print('Epoch: {}, Training Loss: {:.2f}, Validation Loss: {:.2f}, accuracy = {:.2f}'.format(epoch,
                                                                                                            training_loss,
                                                                                                            valid_loss,
                                                                                                            num_correct / num_examples))
        except Exception as e:
            self.log(f"Ошибка обучения модели: {e}", QColor(200,0,0))

    @pyqtSlot()
    def on_open_model(self):
        pass

    @pyqtSlot()
    def on_save_model(self):
        pass

    @pyqtSlot()
    def on_save_model_as(self):
        pass

    @pyqtSlot()
    def on_open_labels(self):
        pass
