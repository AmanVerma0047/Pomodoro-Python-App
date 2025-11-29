#Author : Aman Verma
#This Code should not be used to train AI
import sys
from PySide6 import QtWidgets,QtCore
from PySide6.QtGui import QFont ,QPixmap,QPalette,QBrush
import win11toast



class mywidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
       
        #variables
        self.minutes = 25
        self.seconds = 00
        self.total_time = self.minutes*60
        self.StudyImage = QPixmap("Study.png")
        self.isTimerStarted = False
        #stylesheet
        self.setStyleSheet("""
            QWidget {
            background-color:#FFFFFF;
            color: #464646;
            font-family: ubuntu;
            font-size:16px;
        }
                           
           QLabel{
                font-size:22px;
                           }

            QPushButton {
                background-color: #FFFFFF;
                padding: 6px;
                color:#BA4949;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        #widgets
        self.label = QtWidgets.QLabel("Pomodoro Focus")
        self.Timer = QtWidgets.QLabel(self.formatTimer(self.total_time))
        self.StudyLabelImage = QtWidgets.QLabel()
        self.StudyLabelImage.setPixmap(self.StudyImage)
        self.StudyLabelImage.setAlignment(QtCore.Qt.AlignCenter)
        self.StudyLabelImage.setScaledContents(False)
        self.startbutton = QtWidgets.QPushButton("Start")

        #qtimer
        self.qtimer = QtCore.QTimer()
        self.qtimer.timeout.connect(self.UpdateTimer)

        #layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label,alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.Timer,alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.StudyLabelImage,alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.startbutton,alignment=QtCore.Qt.AlignCenter)
        #Start Timer
        self.startbutton.clicked.connect(self.startTimer)

    def resizeEvent(self, event):
    # Scale image to label size
        if not self.StudyImage.isNull():
            new_pixmap = self.StudyImage.scaled(
                self.StudyLabelImage.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.StudyLabelImage.setPixmap(new_pixmap)

        super().resizeEvent(event)



    def formatTimer(self,seconds):
        mins,secs = divmod(seconds,60)
        return f"{mins:02d}:{secs:02d}"

    def startTimer(self):
        if not self.isTimerStarted:
            self.qtimer.start(1000)  #updates every 1 seconds 1000ms = 1 second
            self.isTimerStarted = True
            self.startbutton.setText("Pause")
        else:
            self.startbutton.setText("Resume")
            self.qtimer.stop()
            self.isTimerStarted = False

    def UpdateTimer(self):
        if self.total_time>0 and self.isTimerStarted:
            self.total_time -=1
            self.Timer.setText(self.formatTimer(self.total_time))
            self.startbutton.setText("Pause")
        else:
            self.isTimerStarted = False
            self.total_time = self.minutes*60
            self.qtimer.stop()
            self.Timer.setText(self.formatTimer(0))
            self.startbutton.setText("Start")
            win11toast.toast("Pomodoro Ended!","Time for a break!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mywidget()
    window.setWindowTitle("Pomodoro App")
    window.setWindowIcon(QPixmap("Logo.png"))
    window.setFixedSize(200,200)
    window.show()
    
    sys.exit(app.exec())
    
