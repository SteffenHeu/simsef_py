import subprocess
import sys
import time
import argparse
import os
import shutil
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# instrument specific imports
from src.AcquisitionControl import AcquisitionControl
from src.AcquisitionParameters import AcquisitionParameters

def main():
    app = QApplication(sys.argv)

    # Create a QWidget object (a window)
    window = QWidget()
    window.setGeometry(100, 100, 300, 200)  # Set the position and size of the window
    window.setWindowTitle('SIMSEF pewpew')  # Set the window title

    # Create a QTextEdit object (a text area)
    global text_area
    text_area = QTextEdit()
    text_area.setPlaceholderText('Please select a file')

    # Create two QPushButton objects (buttons)
    button1 = QPushButton('Select command file')
    button2 = QPushButton('Run acquisition')

    # Define a function to handle the button1 click event
    def open_file_dialog():
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text file (*.txt)")
        file_path = file_dialog.getOpenFileName(window, 'Select command file')[0]
        if file_path:
            text_area.setText(file_path)

    # Connect the button1 click event to the open_file_dialog function
    button1.clicked.connect(open_file_dialog)

    # Connect the button2 click event to the run_function function
    button2.clicked.connect(run_function)

    # Create a QVBoxLayout object to arrange the widgets vertically
    layout = QVBoxLayout()
    layout.addWidget(text_area)
    layout.addWidget(button1)

    # Create a QHBoxLayout object to arrange the buttons horizontally
    button_layout = QHBoxLayout()
    button_layout.addWidget(button1)
    button_layout.addWidget(button2)
    layout.addLayout(button_layout)

    # Set the dark mode stylesheet
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    # Apply the stylesheet to the widgets
    style_sheet = """
    QTextEdit {
        background-color: #252525;
        color: white;
        border: 1px solid #444444;
    }

    QPushButton {
        background-color: #333333;
        color: white;
        border: 1px solid #444444;
    }

    QPushButton:hover {
        background-color: #444444;
    }
    """
    window.setStyleSheet(style_sheet)

    window.setLayout(layout)

    window.show()  # Show the window

    sys.exit(app.exec_())

def run_function():

    # Your code here
    # text_area.append('Button 2 was clicked!')
    # create Parameters
    control = AcquisitionControl()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--commandfile', help='the path to command file', type=str, required=True)
    # argtable = parser.parse_args()
    commandFilePath = text_area.toPlainText()

    with open(commandFilePath) as f:
        lines = f.readlines()

        measured = 0
        starttime = datetime.now()
        for line in lines:
            line = line.strip()
            args = line.split(" ")
            parameters = AcquisitionParameters(args)
            control.runAcquisition(parameters)

            control.controller.waitUntilAcqFinished()

            measured = measured + 1
            elapsedTime = datetime.now() - starttime
            text_area.append('Acquired MS/MS in spot ' + parameters.spot + ' ' + str(measured) + '/' + str(len(lines)))

            remaining = (elapsedTime / measured) * (len(lines) - measured)
            text_area.append('Time elapsed: ' + str(elapsedTime) + ' Remaining: ' + str(remaining))


if __name__ == "__main__":
    main()
