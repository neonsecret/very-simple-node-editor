# from PySide2.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene

from PySide2 import QtWidgets, QtGui

from node_editor.gui.view import View
from node_editor.gui.node_editor import NodeEditor

from node_editor.gui.node import NodeListGeneral


class NodeScene(QtWidgets.QGraphicsScene):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos())
        if item.setAcceptDrops:
            # pass on event to item at the coordinates
            try:
                item.dropEvent(e)
            except RuntimeError:
                pass  # This will supress a Runtime Error generated when dropping into a widget with no ProxyWidget

    def dragMoveEvent(self, e):
        e.acceptProposedAction()


class NodeWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(NodeWidget, self).__init__(parent)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.node_editor = NodeEditor(self)
        self.scene = NodeScene()
        self.scene.setSceneRect(0, 0, 9999, 9999)
        self.view = View(self)
        self.view.setScene(self.scene)
        self.node_editor.install(self.scene)

        main_layout.addWidget(self.view)

        self.view.request_node.connect(self.create_node)

        self.nodes = NodeListGeneral().get_nodes()

    def create_node(self, name):
        print("creating node:", name)

        node = self.nodes[name]()

        self.scene.addItem(node)

        pos = self.view.mapFromGlobal(QtGui.QCursor.pos())
        node.setPos(self.view.mapToScene(pos))
