import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from renderer import CastleRenderer
from viewing_pane import ViewingPane
import cv2
import numpy as np

HOME=".."
castle_num = 3

# Define structures as 0-199, minus certain ranges of animation sprites
available_structure = range(200)
ranges_to_remove = [(33, 42), (44, 47), (49,52), (97,107), (114,119), (121,123), (124,129), (137,143), (158,163), (178,183), (185,185), (198,199)]
available_structure = [
    num for num in available_structure 
    if not any(start <= num <= end for start, end in ranges_to_remove)
]

# Define items as 0-192, minus certain ranges of animation sprites
available_items = range(193)
ranges_to_remove = [(8,14), (19,25), (28,34), (38,44), (47,53), (55,58), (60,63), (65,76), (78,80), (82,84), (86,88), (90,92), (94,97), (106,109), (111,114), (116,119), (121,130), (132,133), (135,136), (138,139), (141,142), (145,160), (162,165), (167,168), (170,173), (175,176), (178,181), (183,184), (186,189), (191,192)]
available_items = [
    num for num in available_items 
    if not any(start <= num <= end for start, end in ranges_to_remove)
]

RIGHT_MENU_SIZE = 500

class ItemButton(QtWidgets.QLabel):
    clicked = QtCore.Signal(int)

    def setId(self, id):
        self.id = id
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.id)

class CastleEditorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.castle_renderer = CastleRenderer()
        castle_structure_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_structure.bin"
        castle_items_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_items.bin"
        castle_magic_filename = f"{HOME}/extracted/volume4_castles/castle{castle_num}_magic.bin"

        # Read the castle data
        with open(castle_structure_filename, "rb") as structure_file:
            self.structure_data = bytearray(structure_file.read())
        with open(castle_items_filename, "rb") as items_file:
            self.items_data = bytearray(items_file.read())
        with open(castle_magic_filename, "rb") as magic_file:
            self.magic_data = bytearray(magic_file.read())

        self.image_frame = ViewingPane(self)
        self.image_frame.coordinatesChanged.connect(self.handleCoords)
        self.image_frame.clicked.connect(self.paneClicked)
        self.labelCoords = QtWidgets.QLabel(self)
        self.gameCoords = QtWidgets.QLabel(self)

        self.numberOfGemsValue = QtWidgets.QLabel()

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

        self.structure_sprites = {}
        for i in range(200):
            self.structure_sprites[i] = cv2.imread(f"{HOME}/extracted/images/structure/{i:03}.png")

        self.item_sprites = {}
        for i in range(200):
            self.item_sprites[i] = cv2.imread(f"{HOME}/extracted/images/items/{i:03}.png")
        
        self.structureLayout = QtWidgets.QGridLayout()
        GRID_SPACING = 5
        self.structureLayout.setSpacing(GRID_SPACING)
        for idx, structure in enumerate(available_structure):
            label = ItemButton()
            label.setId(structure)
            sprite = self.structure_sprites[structure]
            tileSize = 32
            qimage = QtGui.QImage(sprite.data, sprite.shape[1], sprite.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped().scaled(tileSize, tileSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(QtGui.QPixmap.fromImage(qimage))
            num_cols = (RIGHT_MENU_SIZE - 20) // (tileSize + 5)
            label.clicked.connect(self.structure_selected)
            self.structureLayout.addWidget(label, idx // num_cols, idx % num_cols)
        
        self.itemsLayout = QtWidgets.QGridLayout()
        self.itemsLayout.setSpacing(GRID_SPACING)
        for idx, item in enumerate(available_items):
            label = ItemButton()
            label.setId(item)
            sprite = self.item_sprites[item]
            tileSize = 32
            qimage = QtGui.QImage(sprite.data, sprite.shape[1], sprite.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped().scaled(tileSize, tileSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(QtGui.QPixmap.fromImage(qimage))
            num_cols = (RIGHT_MENU_SIZE - 20) // (tileSize + 5)
            label.clicked.connect(self.item_selected)
            self.itemsLayout.addWidget(label, idx // num_cols, idx % num_cols)

        rightMenuLayout = QtWidgets.QWidget()
        rightMenuLayout.setFixedWidth(RIGHT_MENU_SIZE)
        self.rightMenu = QtWidgets.QVBoxLayout()
        self.rightMenu.addWidget(self.numberOfGemsValue)
        self.rightMenu.addWidget(self.selectedCellLabel)
        self.rightMenu.addLayout(self.selectedCellInfoLayout)
        self.rightMenu.addWidget(QtWidgets.QLabel(text = "Structure:"))
        self.rightMenu.addLayout(self.structureLayout)
        self.rightMenu.addWidget(QtWidgets.QLabel(text = "Items:"))
        self.rightMenu.addLayout(self.itemsLayout)
        self.rightMenu.addStretch()
        self.rightMenu.addWidget(self.gameCoords)
        self.rightMenu.addWidget(self.labelCoords)
        rightMenuLayout.setLayout(self.rightMenu)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.layout.addWidget(rightMenuLayout)
        self.setLayout(self.layout)

        self.highlightedCell = None
        self.selectedCell = None

        self.display_image()
        self.image_frame.zoom(5)

    def display_image(self):
        self.image = self.castle_renderer.render(self.structure_data, self.items_data, self.magic_data)
        qimage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPhoto(QtGui.QPixmap.fromImage(qimage))
        self.drawOverlays()

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

    def update_castle_stats(self):
        num_gems = sum(1 for v in self.items_data if v == 0x3B)
        self.numberOfGemsValue.setText(f"{num_gems}")

    def structure_selected(self, id):
        index = self.selectedCell[1] * 250 + self.selectedCell[0]
        self.structure_data[index] = id
        self.display_image()
        self.update_castle_stats()
    
    def item_selected(self, id):
        index = self.selectedCell[1] * 250 + self.selectedCell[0]
        self.items_data[index] = id
        self.display_image()
        self.update_castle_stats()

    def magic_selected(self, id):
        index = self.selectedCell[1] * 250 + self.selectedCell[0]
        self.magic_data[index] = id
        self.display_image()
        self.update_castle_stats()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = CastleEditorWindow()
    widget.setWindowTitle("Clyde's Unofficial Castle Editor")
    widget.resize(1600, 900)
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec_())
