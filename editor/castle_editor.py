import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from renderer import CastleRenderer
from viewing_pane import ViewingPane
import cv2
import numpy as np

class CastleEditorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.castle_renderer = CastleRenderer(1)

        self.image_frame = ViewingPane(self)
        self.image_frame.coordinatesChanged.connect(self.handleCoords)
        self.labelCoords = QtWidgets.QLabel(self)
        self.gameCoords = QtWidgets.QLabel(self)
        # self.labelCoords.setAlignment(
        #     QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)

        self.button = QtWidgets.QPushButton("Click me!")

        rightMenuLayout = QtWidgets.QWidget()
        rightMenuLayout.setFixedWidth(250)
        self.rightMenu = QtWidgets.QVBoxLayout()
        self.rightMenu.addWidget(self.button)
        self.rightMenu.addStretch()
        self.rightMenu.addWidget(self.gameCoords)
        self.rightMenu.addWidget(self.labelCoords)
        rightMenuLayout.setLayout(self.rightMenu)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.layout.addWidget(rightMenuLayout)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)
        self.display_image()

    def display_image(self):
        self.image = self.castle_renderer.render()
        qimage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPhoto(QtGui.QPixmap.fromImage(qimage))

    def handleCoords(self, point):
        if not point.isNull():
            self.labelCoords.setText(f'Rendered coords: {point.x()}, {point.y()}')
            game_x = point.x() // 16
            game_y = point.y() // 16
            self.gameCoords.setText(f'Game coords: {game_x}, {game_y}')

            # Show highlight
            highlight = (game_x, game_y)
            
            top_left = np.multiply(highlight, 16)
            # Blue color in BGR
            color = (255, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            img2 = self.image.copy()
            cv2.rectangle(img2, top_left, np.add(top_left, 16), color, thickness)
            qimage = QtGui.QImage(img2.data, img2.shape[1], img2.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.image_frame.setPhoto(QtGui.QPixmap.fromImage(qimage))
        else:
            self.labelCoords.setText(f'Rendered coords: ')
            self.gameCoords.setText(f'Game coords: ')

    def magic(self):
        print("hello")
        self.display_image()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = CastleEditorWindow()
    widget.setWindowTitle("Clyde's Unofficial Castle Editor")
    widget.resize(1320, 900)
    widget.show()

    sys.exit(app.exec_())
