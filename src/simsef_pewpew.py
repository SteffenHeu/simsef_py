import subprocess
import sys
import time
import argparse
import os
import shutil
from datetime import datetime
import sys
from threading import Thread
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

# instrument specific imports
from src.AcquisitionControl import AcquisitionControl
from src.AcquisitionParameters import AcquisitionParameters


class Main(QtGui.QGuiApplication):

    def log(self, msg: str):
        print(msg)
        if self.text_area:
            self.text_area.append(msg)

    def startRunThread(self):
        self.log("Creating run thread...")
        self.thread = RunThread(self.commandFilePath)
        self.thread.getTrigger().connect(lambda s: self.log(s))
        self.thread.start()

    # Define a function to handle the button1 click event
    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text file (*.txt)")
        file_path = file_dialog.getOpenFileName(window, 'Select command file')[0]
        if file_path:
            self.commandFilePath = file_path
            self.log("Command file selected:")
            self.log(self.commandFilePath)

    def __init__(self, parent=None):
        app = QApplication(sys.argv)

        parser = argparse.ArgumentParser()
        parser.add_argument('--commandfile', help='the path to command file', type=str, required=False)
        argtable = parser.parse_args()

        # Create a QWidget object (a window)
        global window
        window = QWidget()
        window.setGeometry(100, 100, 300, 200)  # Set the position and size of the window
        window.setWindowTitle('SIMSEF pewpew')  # Set the window title

        # Create a QTextEdit object (a text area)
        self.commandFilePath = None
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText('Please select a file')

        if (argtable.commandfile):
            self.commandFilePath = argtable.commandfile
            self.log("Command file path already set via arg: " + self.commandFilePath)

        if (self.commandFilePath):
            self.log(self.commandFilePath)

        # Create two QPushButton objects (buttons)
        button1 = QPushButton('Select command file')
        button2 = QPushButton('Run acquisition')

        # Connect the button1 click event to the open_file_dialog function
        button1.clicked.connect(lambda: self.open_file_dialog())

        # Connect the button2 click event to the run_function function
        button2.clicked.connect(lambda: self.startRunThread())

        if (self.commandFilePath != None):
            self.log("Starting auto execute.")
            self.startRunThread()

        # Create a QVBoxLayout object to arrange the widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(button1)

        # Create a QHBoxLayout object to arrange the buttons horizontally
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        layout.addLayout(button_layout)

        # Set the dark mode stylesheet
        dark_palette = self.getDarkPalette()
        app.setPalette(dark_palette)

        style_sheet = self.getStyleSheet()
        window.setStyleSheet(style_sheet)
        window.setLayout(layout)
        window.show()  # Show the window

        sys.exit(app.exec_())

    def getStyleSheet(self):
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
        return style_sheet

    def getDarkPalette(self):
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
        return dark_palette


class RunThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self, commandFilePath):
        super().__init__()
        self.commandFilePath = commandFilePath

    def run(self):
        control = AcquisitionControl()

        if self.commandFilePath is None:
            self.trigger.emit("Cannot start acquisition, command file path not set.")
            return

        with open(self.commandFilePath) as f:
            lines = f.readlines()

            measured = 0
            starttime = datetime.now()
            for line in lines:
                line = line.strip()
                args = line.split(" ")
                parameters = AcquisitionParameters(args)

                try:
                    control.runAcquisition(parameters)

                    control.controller.waitUntilAcqFinished()

                    measured = measured + 1
                    elapsedTime = datetime.now() - starttime
                    self.trigger.emit(
                        'Acquired MS/MS in spot ' + parameters.spot + ' ' + str(measured) + '/' + str(len(lines)))

                    remaining = (elapsedTime / measured) * (len(lines) - measured)
                    self.trigger.emit('Time elapsed: ' + str(elapsedTime) + ' Remaining: ' + str(remaining))
                except Exception:
                    self.trigger.emit("Unknown error when measuring line " + line)

    def getTrigger(self):
        return self.trigger


if __name__ == "__main__":
    Main()
