from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSize
from niaaml_gui.progress_bar import ProgressBar
from niaaml_gui.windows.threads import OptimizeThread, RunThread
import copy

class ProcessWindow(QMainWindow):
    def __init__(self, parent, data):
        super(ProcessWindow, self).__init__(parent)
        self.setMinimumSize(QSize(640, 480))

        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.__progressBar = ProgressBar()
        layout.addWidget(self.__progressBar)

        self.__textArea = QPlainTextEdit(parent=self)
        self.__textArea.setReadOnly(True)
        layout.addWidget(self.__textArea)

        confirmBar = QHBoxLayout(self)
        confirmBar.addStretch()

        self.__btn = QPushButton(self)
        self.__btn.setText('Cancel')
        font = self.__btn.font()
        font.setPointSize(12)
        self.__btn.setFont(font)
        self.__btn.clicked.connect(self.cancelClose)
        confirmBar.addWidget(self.__btn)

        layout.addItem(confirmBar)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.__data = copy.deepcopy(data)

        if self.__data.isOptimization:
            optimizer = OptimizeThread(self.__data)
            optimizer.optimized.connect(self.onOptimizationComplete)
            self.__runningThread = optimizer
            optimizer.start()
            self.__textArea.appendPlainText('Pipeline optimization running...\n')
        else:
            runner = RunThread(self.__data)
            runner.ran.connect(self.onRunComplete)
            self.__runningThread = runner
            runner.start()
            self.__textArea.appendPlainText('Pipeline running...\n')
    
    def cancelClose(self):
        self.close()
        try:
            self.__runningThread.terminate()
        except:
            return
    
    def onOptimizationComplete(self, data):
        self.__progressBar.setMaximum(100)
        self.__progressBar.setValue(100)
        self.__textArea.appendPlainText(data + '\n')
        self.__textArea.appendPlainText('Pipeline optimization complete.')
        self.__textArea.appendPlainText('Results exported to: ' + self.__data.outputFolder)
        self.__btn.setText('Close')

    def onRunComplete(self, data):
        self.__progressBar.setMaximum(100)
        self.__progressBar.setValue(100)
        self.__textArea.appendPlainText('Predictions: ' + data + '\n')
        self.__textArea.appendPlainText('Pipeline run complete.')
        self.__btn.setText('Close')
