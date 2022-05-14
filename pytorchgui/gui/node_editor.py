from PySide2 import QtWidgets, QtCore

from pytorchgui.gui.connection import Connection
from pytorchgui.gui.node import Node
from pytorchgui.gui.port import Port


class NodeEditor(QtCore.QObject):
    def __init__(self, parent):
        super(NodeEditor, self).__init__(parent)
        self.port = None
        self.scene = None
        self._last_selected = None
        self.connection = []

    def install(self, scene):
        self.scene = scene
        self.scene.installEventFilter(self)

    def item_at(self, position):
        items = self.scene.items(
            QtCore.QRectF(position - QtCore.QPointF(1, 1), QtCore.QSizeF(3, 3))
        )

        if items:
            return items[0]
        return None

    def eventFilter(self, watched, event):
        if type(event) == QtWidgets.QWidgetItem:
            return False

        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:

            if event.button() == QtCore.Qt.LeftButton:
                item = self.item_at(event.scenePos())
                if isinstance(item, Port):
                    self.connection.append(Connection(None))
                    self.scene.addItem(self.connection[-1])
                    # self.connection.start_port = item
                    self.port = item
                    self.connection[-1].start_pos = item.scenePos()
                    self.connection[-1].end_pos = event.scenePos()
                    self.connection[-1].update_path()
                    return True

                elif isinstance(item, Connection):
                    self.connection.append(Connection(None))
                    self.connection[-1].start_pos = item.start_pos
                    self.scene.addItem(self.connection[-1])
                    # self.connection.start_port = item.start_port
                    self.port = item.start_port
                    self.connection[-1].end_pos = event.scenePos()
                    self.connection[-1].update_start_and_end_pos()  # to fix the offset
                    return True

                elif isinstance(item, Node):
                    if self._last_selected:
                        # If we clear the scene, we loose the last selection
                        try:
                            self._last_selected.select_connections(False)
                        except RuntimeError as e:
                            print(e)
                            # pass

                    item.select_connections(True)
                    self._last_selected = item

                else:
                    try:
                        if self._last_selected:
                            self._last_selected.select_connections(False)
                    except RuntimeError as e:
                        print(e)
                        # pass

                    self._last_selected = None

            elif event.button() == QtCore.Qt.RightButton:

                pass

        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Delete:

                for item in self.scene.selectedItems():
                    for port in item._ports:
                        if port.connection is not None:
                            for conn in port.connection:
                                conn.delete()
                    if isinstance(item, (Connection, Node)):
                        # print(f"item {item}")
                        item.delete()

                return True

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            for i, conn in enumerate(self.connection):
                if conn:
                    self.connection[i].end_pos = event.scenePos()
                    self.connection[i].update_path()
                    return True

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            for i, conn in enumerate(self.connection):
                if conn and event.button() == QtCore.Qt.LeftButton:
                    item = self.item_at(event.scenePos())

                    # connecting a port
                    if isinstance(item, Port):
                        if self.port.can_connect_to(item):
                            print("connecting")

                            if item.connection is not None:
                                print("connection exists!")
                                item.clear_connection()

                            self.connection[i].start_port = self.port

                            self.connection[i].end_port = item

                            self.connection[i].update_start_and_end_pos()
                            self.connection[i] = None

                        else:
                            print("Deleting connection")
                            self.connection[i].delete()
                            self.connection[i] = None

                    if self.connection[i]:
                        self.connection[i].delete()
                    self.connection[i] = None
                    self.port = None
                    return True

        return super(NodeEditor, self).eventFilter(watched, event)
