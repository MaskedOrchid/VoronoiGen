from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from VoronoiController import DrawModes


class CanvasTools(QWidget):
    def __init__(self, vc):
        super().__init__()
        self.voroController=vc

        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(15)
        tool_layout.setContentsMargins(10, 10, 10, 10)

        add_btn = QPushButton("Add Site")
        add_btn.setFixedHeight(40)
        add_btn.clicked.connect(lambda: self.voroController.setMode(DrawModes.Add))

        remove_btn = QPushButton("Remove Site")
        remove_btn.setFixedHeight(40)
        remove_btn.clicked.connect(lambda: self.voroController.setMode(DrawModes.Remove))

        select_btn = QPushButton("Select Cell")
        select_btn.setFixedHeight(40)
        select_btn.clicked.connect(lambda: self.voroController.setMode(DrawModes.Select))

        tool_layout.addWidget(add_btn)
        tool_layout.addWidget(remove_btn)
        tool_layout.addWidget(select_btn)

        self.setLayout(tool_layout)

