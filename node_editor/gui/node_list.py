from PySide2 import QtWidgets, QtCore, QtGui
from node_editor.gui.node import NodeListGeneral


class NodeList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(NodeList, self).__init__(parent)

        for node in NodeListGeneral().get_nodes():
            self.addItem(node)

        self.setDragEnabled(True)  # enable dragging

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        pos = event.pos()

        # actions
        print_help = QtWidgets.QAction("Print help")
        menu.addAction(print_help)

        action = menu.exec_(self.mapToGlobal(pos))
        item_name = self.selectedItems()[0].text()

        if action == print_help:
            print(f"help will be printed to the {item_name} node")
        else:
            print(f"{item_name} action")

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        name = item.text()

        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()

        mime_data.setText(name)
        drag.setMimeData(mime_data)
        drag.exec_()

        super(NodeList, self).mousePressEvent(event)
