import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QListWidgetItem,
                             QLineEdit, QPushButton, QCheckBox)


class ChecklistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checklist")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.create_ui()

    def create_ui(self):
        # Input area for new items
        self.input_layout = QHBoxLayout()
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Enter new item...")
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)

        self.input_layout.addWidget(self.item_input)
        self.input_layout.addWidget(self.add_button)

        # Checklist
        self.checklist = QListWidget()
        self.checklist.itemChanged.connect(self.item_checked)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_item)
        self.clear_completed_button = QPushButton("Clear Completed")
        self.clear_completed_button.clicked.connect(self.clear_completed)

        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.clear_completed_button)

        # Add all widgets to main layout
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.checklist)
        self.layout.addLayout(self.button_layout)

    def add_item(self):
        text = self.item_input.text().strip()
        if text:
            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            checkbox = QCheckBox(text)
            checkbox.stateChanged.connect(lambda state, item=item: self.update_item_state(item, state))

            layout.addWidget(checkbox)
            widget.setLayout(layout)

            item.setSizeHint(widget.sizeHint())
            self.checklist.addItem(item)
            self.checklist.setItemWidget(item, widget)

            self.item_input.clear()

    def delete_item(self):
        selected_items = self.checklist.selectedItems()
        for item in selected_items:
            self.checklist.takeItem(self.checklist.row(item))

    def clear_completed(self):
        for i in range(self.checklist.count() - 1, -1, -1):
            item = self.checklist.item(i)
            widget = self.checklist.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox.isChecked():
                self.checklist.takeItem(i)

    def item_checked(self, item):
        # This is triggered when the item itself changes (not the checkbox)
        pass

    def update_item_state(self, item, state):
        # This handles the checkbox state changes
        widget = self.checklist.itemWidget(item)
        checkbox = widget.findChild(QCheckBox)

        # You could add additional logic here for when items are checked/unchecked
        if state == 2:  # 2 means checked
            font = checkbox.font()
            font.setStrikeOut(True)
            checkbox.setFont(font)
            checkbox.setStyleSheet("color: gray")
        else:
            font = checkbox.font()
            font.setStrikeOut(False)
            checkbox.setFont(font)
            checkbox.setStyleSheet("color: black")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChecklistApp()
    window.show()
    sys.exit(app.exec_())