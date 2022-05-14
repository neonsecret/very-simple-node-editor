import sys
import logging

from PySide2 import QtWidgets, QtCore, QtGui

from pytorchgui.gui.node_widget import NodeWidget
from pytorchgui.gui.palette import palette
from pytorchgui.gui.node_list import NodeList

logging.basicConfig(level=logging.DEBUG)


class NodeEditor(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.settings = None

        icon = QtGui.QIcon("resources\\app.ico")
        self.setWindowIcon(icon)

        self.setWindowTitle("Logic Node Editor")
        settings = QtCore.QSettings("node-editor", "NodeEditor")

        # Layouts
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()

        self.node_list = NodeList()
        self.splitter = QtWidgets.QSplitter()

        self.setCentralWidget(main_widget)
        main_widget.setLayout(main_layout)

        self.node_widget = NodeWidget(self)
        button = QtWidgets.QPushButton('Process')
        button.setStyleSheet(
            "QPushButton:pressed { background-color: rgb(25,25,25) }"
            "QPushButton { background-color: black;  "
            "border-style: outset;"
            "border-width: 1px;"
            "border-radius: 5px;"
            "border-color: beige;"
            "min-width: 5em;"
            "padding: 6px; }"
        )
        self.button = button
        self.button.clicked.connect(self.process_graph)

        main_layout.addWidget(self.splitter)
        main_layout.addWidget(self.button)

        self.splitter.addWidget(self.node_list)
        self.splitter.addWidget(self.node_widget)

        try:
            self.restoreGeometry(settings.value("geometry"))
            s = settings.value("splitterSize")
            self.splitter.restoreState(s)

        except AttributeError as e:
            logging.warning(
                "Unable to load settings. First time opening the tool?\n" + str(e)
            )

    def closeEvent(self, event):
        self.settings = QtCore.QSettings("node-editor", "NodeEditor")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterSize", self.splitter.saveState())
        QtWidgets.QWidget.closeEvent(self, event)

    def process_graph(self):
        items = self.node_widget.scene.items()
        print("processing graph")
        for _item in items:
            if str(type(_item)) == str(type(_item)) == "<class 'pytorchgui.gui.port.Port'>":
                pass
            elif str(type(_item)) == str(type(_item)) == "<class 'pytorchgui.gui.node.Node'>":
                pass
            else:
                print(f"connection between nodes {_item._start_port.m_node._title_text} "
                      f"and {_item._end_port.m_node._title_text}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("resources\\app.ico"))
    app.setPalette(palette)
    launcher = NodeEditor()
    launcher.show()
    app.exec_()
    sys.exit()
