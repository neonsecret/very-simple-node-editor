from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QLineEdit, QGraphicsProxyWidget, QGraphicsScene

from pytorchgui.gui.port import Port


def create_input():
    node = Node()
    node.title = "IN"
    node.type_text = "input"
    node.add_port(name="output", is_output=True)
    node.conn_type = "input"
    node.build()
    return node


def create_output():
    node = Node()
    node.title = "OUT"
    node.conn_type = "output"
    node.type_text = "output"
    node.add_port(name="input", is_output=False)
    node.build()
    return node


def create_sum():
    node = Node()
    node.title = "SUM"
    node.conn_type = "data"
    node.type_text = "built-in"
    node.add_port(name="input A", is_output=False)
    node.add_port(name="input B", is_output=False)
    node.add_port(name="output", is_output=True)
    node.build()
    return node


def create_divide():
    node = Node()
    node.title = "DIVIDE"
    node.conn_type = "data"
    node.type_text = "built-in"
    node.add_port(name="input A", is_output=False)
    node.add_port(name="input B", is_output=False)
    node.add_port(name="output", is_output=True)
    node.build()
    return node


def create_multiply():
    node = Node()
    node.title = "MULT"
    node.conn_type = "data"
    node.type_text = "built-in"
    node.add_port(name="input A", is_output=False)
    node.add_port(name="input B", is_output=False)
    node.add_port(name="output", is_output=True)
    node.build()
    return node


def create_substract():
    node = Node()
    node.title = "MINUS"
    node.conn_type = "data"
    node.type_text = "built-in"
    node.add_port(name="input A", is_output=False)
    node.add_port(name="input B", is_output=False)
    node.add_port(name="output", is_output=True)
    node.build()
    return node


def create_neon_node():
    node = Node()
    node.title = "Image 2x2"
    node.type_text = "custom_tweaked"
    node.conn_type = "image"
    node.add_port(name="input 1", is_output=False)
    node.add_port(name="input 2", is_output=False)
    node.add_port(name="output 1", is_output=True)
    node.add_port(name="output 2", is_output=True)
    node.build()
    return node


def create_constant_node():
    node = Node()
    node.title = "Constant"
    node.type_text = "built-in"
    node.conn_type = "constant"
    node.add_port(name="output 1", is_output=True)
    node.value = 5
    node.build()
    return node


class NodeListGeneral:
    def __init__(self):
        self.nodes = {
            "Input": create_input,
            "Output": create_output,
            "Sum": create_sum,
            "Multiply": create_multiply,
            "Minus": create_substract,
            "Divide": create_divide,
            "Neon": create_neon_node,
            "Constant": create_constant_node
        }

    def get_nodes(self):
        return self.nodes


class Node(QtWidgets.QGraphicsPathItem):
    def __init__(self):
        super(Node, self).__init__()

        self.setFlag(QtWidgets.QGraphicsPathItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsPathItem.ItemIsSelectable)

        self._title_text = "Title"
        self._type_text = "base"

        self._width = 30  # The Width of the node
        self._height = 50  # the height of the node
        self._ports = []  # A list of ports
        self.value = None

        self.node_color = QtGui.QColor(62, 62, 62, 255)

        self.conn_type = "data"

        self.conn_type_colors = {
            "input": QtGui.QColor(155, 162, 91),
            "data": QtGui.QColor(62, 62, 70),
            "image": QtGui.QColor(8, 149, 115),
            "output": QtGui.QColor(155, 162, 91),
            "constant": QtGui.QColor(252, 98, 3)
        }

        self.title_path = QtGui.QPainterPath()  # The path for the title
        self.type_path = QtGui.QPainterPath()  # The path for the type
        self.misc_path = QtGui.QPainterPath()  # a bunch of other stuff
        self.input_fild = None

        self.horizontal_margin = 30  # horizontal margin
        self.vertical_margin = 15  # vertical margin

    @property
    def title(self):
        return self._title_text

    @title.setter
    def title(self, title):
        self._title_text = title

    @property
    def type_text(self):
        return self._type_text

    @type_text.setter
    def type_text(self, type_text):
        self._type_text = type_text

    def paint(self, painter, option=None, widget=None):
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(241, 175, 0), 2))
            painter.setBrush(self.node_color)
        else:
            painter.setPen(self.node_color.lighter())
            painter.setBrush(self.node_color)

        painter.drawPath(self.path())
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.white)

        painter.drawPath(self.title_path)
        painter.drawPath(self.type_path)
        painter.drawPath(self.misc_path)

        if self.title == "Constant":
            self.value = input("Enter constant value")

    def add_port(self, name, is_output=False, flags=0, ptr=None):
        port = Port(self, self.scene())
        port.set_is_output(is_output)
        port.set_name(name)
        port.set_node(node=self)
        port.set_port_flags(flags)
        port.set_ptr(ptr)

        self._ports.append(port)

    def build(self):
        """ Build the node
        """

        self.title_path = QtGui.QPainterPath()  # reset
        self.type_path = QtGui.QPainterPath()  # The path for the type
        self.misc_path = QtGui.QPainterPath()  # a bunch of other stuff

        total_width = 0
        total_height = 0
        path = QtGui.QPainterPath()  # The main path

        # The fonts what will be used
        title_font = QtGui.QFont("DejaVuSans", pointSize=16)
        title_type_font = QtGui.QFont("DejaVuSans", pointSize=8)
        port_font = QtGui.QFont("DejaVuSans")

        # Get the dimentions of the title and type
        title_dim = {
            "w": QtGui.QFontMetrics(title_font).width(self._title_text),
            "h": QtGui.QFontMetrics(title_font).height(),
        }

        title_type_dim = {
            "w": QtGui.QFontMetrics(title_type_font).width("(" + self._type_text + ")"),
            "h": QtGui.QFontMetrics(title_type_font).height(),
        }

        # Get the max width
        for dim in [title_dim["w"], title_type_dim["w"]]:
            if dim > total_width:
                total_width = dim

        # Add both the title and type height together for the total height
        for dim in [title_dim["h"], title_type_dim["h"]]:
            total_height += dim

        # Add the heigth for each of the ports
        for port in self._ports:
            port_dim = {
                "w": QtGui.QFontMetrics(port_font).width(port.name()),
                "h": QtGui.QFontMetrics(port_font).height(),
            }

            if port_dim["w"] > total_width:
                total_width = port_dim["w"]

            total_height += port_dim["h"]

        # Add the margin to the total_width
        total_width += self.horizontal_margin
        total_height += self.vertical_margin

        # Draw the background rectangle
        path.addRoundedRect(
            -total_width / 2, -total_height / 2, total_width, total_height, 5, 5
        )

        # Draw the title
        self.title_path.addText(
            -title_dim["w"] / 2,
            (-total_height / 2) + title_dim["h"],
            title_font,
            self._title_text,
        )

        # Draw the type
        self.type_path.addText(
            -title_type_dim["w"] / 2,
            (-total_height / 2) + title_dim["h"] + title_type_dim["h"],
            title_type_font,
            "(" + self._type_text + ")",
        )

        y = (-total_height / 2) + title_dim["h"] + title_type_dim["h"] + port_dim["h"]

        for port in self._ports:
            if port.is_output():
                port.setPos(total_width / 2 - 10, y)
            else:
                port.setPos(-total_width / 2 + 10, y)
            y += port_dim["h"]

        self.setPath(path)

        self._width = total_width
        self._height = total_height

    def select_connections(self, value):
        for port in self._ports:
            if port.connection is not None:
                for i, conn in enumerate(port.connection):
                    if conn:
                        port.connection[i]._do_highlight = value
                        port.connection[i].update_path()

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

            # confirm to open in the editor replacing what is existing

    def delete(self):
        """Delete the connection.
        Remove any found connections ports by calling :any:`Port.remove_connection`.  After connections
        have been removed set the stored :any:`Port` to None. Lastly call :any:`QGraphicsScene.removeItem`
        on the scene to remove this widget.
        """

        to_delete = []

        for port in self._ports:
            if port.connection is not None:
                for i, conn in enumerate(port.connection):
                    if conn:
                        to_delete.append(port.connection[i])

        for connection in to_delete:
            connection.delete()

        self.scene().removeItem(self)
