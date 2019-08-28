import os
import sys

import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene

from model.net import net
from moon import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.total_pics = 0
        self.id = 0
        self.pic_folder = ''
        self.pic_list = None

        self.model_selector.addItems(['Faster RCNN', 'CNN', 'DCN'])

        self.btn_choose_pic.clicked.connect(self.choose_pic_forder)
        self.btn_pre.clicked.connect(self.pre_pic)
        self.btn_next.clicked.connect(self.next_pic)
        self.btn_detect.clicked.connect(self.detect)

    def pre_pic(self):
        if self.id == 0:
            self.id = self.total_pics - 1
        else:
            self.id -= 1
        self.refresh()

    def next_pic(self):
        if self.id == self.total_pics - 1:
            self.id = 0
        else:
            self.id += 1
        self.refresh()

    def choose_pic_forder(self):
        folder = QFileDialog.getExistingDirectory()
        if folder != '':
            self.pic_folder = folder
            self.total_pics = len(list(x for x in os.listdir(self.pic_folder) if
                                       (x.endswith('.jpg') or x.endswith('.jpeg') or x.endswith('.png'))))
            self.refresh()

    def detect(self):
        model = net()
        result = model.predict(self.pic_list[self.id])
        # we suppose the result is according to the origin picture

        img = cv2.imread(os.path.join(self.pic_folder, self.pic_list[self.id]), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        obj, score, box = result
        xmin, ymin, xmax, ymax = box
        cv2.putText(img, obj + ' ' + str(score), (xmin, ymin+10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0, 255), 1)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0, 255), 1)

        self.refresh(img)

    def refresh(self, img = None):
        self.pic_list = os.listdir(self.pic_folder)
        if img is None:
            img = cv2.imread(os.path.join(self.pic_folder, self.pic_list[self.id]), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        y, x = img.shape[0], img.shape[1]
        frame = QImage(img, x, y, QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.graphicsView.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec())
