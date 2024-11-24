import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from renderer import CastleRenderer
from viewing_pane import ViewingPane
import cv2
import numpy as np

HOME=".."
castle_num = 1

available_items = {
    ""
}

class CastleEditorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.castle_renderer = CastleRenderer()
        castle_structure_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_structure.bin"
        castle_items_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_items.bin"
        castle_magic_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_magic.bin"

        # Read the castle data
        with open(castle_structure_filename, "rb") as structure_file:
            self.structure_data = structure_file.read()
        with open(castle_items_filename, "rb") as items_file:
            self.items_data = items_file.read()
        with open(castle_magic_filename, "rb") as magic_file:
            self.magic_data = magic_file.read()

        self.image_frame = ViewingPane(self)
        self.image_frame.coordinatesChanged.connect(self.handleCoords)
        self.image_frame.clicked.connect(self.paneClicked)
        self.labelCoords = QtWidgets.QLabel(self)
        self.gameCoords = QtWidgets.QLabel(self)

        # Selected cell information
        self.selectedCellLabel = QtWidgets.QLabel(self, text = "Selected cell")
        
        self.selectedCellItemLabel = QtWidgets.QLabel(self, text = "Item")
        self.selectedCellItemValue = QtWidgets.QLabel(self)
        self.selectedCellItemLayout = QtWidgets.QVBoxLayout()
        self.selectedCellItemLayout.addWidget(self.selectedCellItemLabel)
        self.selectedCellItemLayout.addWidget(self.selectedCellItemValue)
        
        self.selectedCellStructureLabel = QtWidgets.QLabel(self, text = "Structure")
        self.selectedCellStructureValue = QtWidgets.QLabel(self)
        self.selectedCellStructureLayout = QtWidgets.QVBoxLayout()
        self.selectedCellStructureLayout.addWidget(self.selectedCellStructureLabel)
        self.selectedCellStructureLayout.addWidget(self.selectedCellStructureValue)

        self.selectedCellMagicLabel = QtWidgets.QLabel(self, text = "Magic")
        self.selectedCellMagicValue = QtWidgets.QLabel(self)
        self.selectedCellMagicLayout = QtWidgets.QVBoxLayout()
        self.selectedCellMagicLayout.addWidget(self.selectedCellMagicLabel)
        self.selectedCellMagicLayout.addWidget(self.selectedCellMagicValue)

        self.selectedCellInfoLayout = QtWidgets.QHBoxLayout()
        self.selectedCellInfoLayout.addLayout(self.selectedCellItemLayout)
        self.selectedCellInfoLayout.addLayout(self.selectedCellStructureLayout)
        self.selectedCellInfoLayout.addLayout(self.selectedCellMagicLayout)

        rightMenuLayout = QtWidgets.QWidget()
        rightMenuLayout.setFixedWidth(250)
        self.rightMenu = QtWidgets.QVBoxLayout()
        self.rightMenu.addWidget(self.selectedCellLabel)
        self.rightMenu.addLayout(self.selectedCellInfoLayout)
        self.rightMenu.addStretch()
        self.rightMenu.addWidget(self.gameCoords)
        self.rightMenu.addWidget(self.labelCoords)
        rightMenuLayout.setLayout(self.rightMenu)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.layout.addWidget(rightMenuLayout)
        self.setLayout(self.layout)

        self.display_image()

        self.highlightedCell = None
        self.selectedCell = None

    def display_image(self):
        self.image = self.castle_renderer.render(self.structure_data, self.items_data, self.magic_data)
        qimage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPhoto(QtGui.QPixmap.fromImage(qimage))

    def handleCoords(self, point):
        if not point.isNull():
            self.labelCoords.setText(f'Rendered coords: {point.x()}, {point.y()}')
            game_x = point.x() // 16
            game_y = point.y() // 16
            self.gameCoords.setText(f'Game coords: {game_x}, {game_y}')

            self.highlightedCell = (game_x, game_y)
            self.drawOverlays()
        else:
            self.labelCoords.setText(f'Rendered coords: ')
            self.gameCoords.setText(f'Game coords: ')

    def drawOverlays(self):
        img2 = self.image.copy()

        if self.highlightedCell:
            top_left = np.multiply(self.highlightedCell, 16)
            color = (0, 0, 0)
            thickness = 1
            cv2.rectangle(img2, top_left, np.add(top_left, 16), color, thickness)

        # Show selected
        if self.selectedCell:
            top_left = np.multiply(self.selectedCell, 16)
            color = (0, 255, 0)
            thickness = 1
            cv2.rectangle(img2, top_left, np.add(top_left, 16), color, thickness)
        
        qimage = QtGui.QImage(img2.data, img2.shape[1], img2.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPhoto(QtGui.QPixmap.fromImage(qimage))

    def paneClicked(self, point):
        game_x = point.x() // 16
        game_y = point.y() // 16
        self.selectedCell = (game_x, game_y)
        self.drawOverlays()

        # Write the labels
        index = self.selectedCell[1] * 250 + self.selectedCell[0]
        self.selectedCellItemValue.setText(f"{self.items_data[index]:02x}")
        self.selectedCellStructureValue.setText(f"{self.structure_data[index]:02x}")
        self.selectedCellMagicValue.setText(f"{self.magic_data[index]:02x}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = CastleEditorWindow()
    widget.setWindowTitle("Clyde's Unofficial Castle Editor")
    widget.resize(1320, 900)
    widget.show()

    sys.exit(app.exec_())
