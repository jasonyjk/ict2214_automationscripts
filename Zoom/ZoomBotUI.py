import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu, QPushButton, QLineEdit, QCheckBox, QDateTimeEdit, QHeaderView
from MainWinUI import Ui_MainWindow
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
from pandas import DataFrame
from StorageSystem import DataBase
from threading import Thread
from time import sleep, time
from datetime import datetime
from urllib.request import urlopen
from pywinauto.application import Application
from pywinauto import timings


class ZoomBotUI(QMainWindow):

    meetingData = []
    curMeetingCount = 0
    closeBtns = []
    cols = ['Text', 'Text', 'Text', 'DateTime', 'CheckBox', 'CheckBox']
    sql = DataBase()
    flag = None

    def __init__(self):
        super(ZoomBotUI, self).__init__()

        # Setting up the UI
        self.ui = Ui_MainWindow()   # import UI (Ui_MainWindow() is a class) from MainWinUI.py
        self.ui.setupUi(self)       # bring the UI to the screen (refer to line 15 in MainWinUI.py)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.restoreData()
        self.startThread()  #

        # Adding Functions to Buttons
        self.ui.closeBtn.clicked.connect(self.hide)  # inbuilt function of PyQt5 also to make sure the timer doesn't close
        self.ui.minBtn.clicked.connect(self.showMinimized)  # inbuilt function of PyQt5
        self.ui.closeBtn.setToolTip("Close")        # label
        self.ui.minBtn.setToolTip("Minimize")
        self.ui.addBtn.clicked.connect(self.addMeeting)
        self.ui.saveBtn.clicked.connect(self.saveTable)  # DO NOT PUT () otherwise program will crash for hide and below

        # self.ui.appIcon.setIcon(QIcon("./ZoomAuto.png"))

        # Changing Headers of the Table
        stylesheet = "::section{background-color:rgb(204,204,204);border-radius:14px}"
        self.ui.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        self.ui.tableWidget.verticalHeader().setStyleSheet(stylesheet)

        # Setting up Tray Menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("C:/Users/JasonYeo/Desktop/development for zoom/automation.png"))
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.closeEvent)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Display the UI on Screen
        self.show()                 # bring UI to the front (visible)

    def closeEvent(self, event):
        self.saveTable()    # autosave the table if we accidentally quit the program
        self.flag = False   #
        self.tray_icon.hide()
        self.close()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos()+event.globalPos()-self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def addMeeting(self):   # creates widget to fill up the cell(columns)
        name = QLineEdit(self)
        Id = QLineEdit(self)
        passwd = QLineEdit(self)
        datetime = QDateTimeEdit(self)
        audio = QCheckBox(self)
        video = QCheckBox(self)
        close = QPushButton(self)

        datetime.setDisplayFormat('dd-MMM , hh:mm')
        datetime.setDateTime(QDateTime().currentDateTime())

        close.setIcon(QIcon('./close-button.png'))
        close.setFlat(True)

        self.ui.tableWidget.insertRow(self.curMeetingCount)  # contains number of rows or meeting
        close.setObjectName(str(self.curMeetingCount))       # corresponds to close = QPushButton(self), give each delete button in the respective row an id, equivalent to the row id
        close.released.connect(lambda: self.deleteMeeting(close.objectName()))
        self.closeBtns.append(close)
        self.elements = [name, Id, passwd, datetime, audio, video, close]
        col = 0
        for element in self.elements:
            self.ui.tableWidget.setCellWidget(self.curMeetingCount, col, element)
            col += 1

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.elements.remove(close)
        row = []
        for element, name in zip(self.elements, self.cols):
            element.setObjectName(name)
            row.append(element)
        self.meetingData.append(row)
        self.curMeetingCount += 1

    def deleteMeeting(self, button_id):
        self.ui.tableWidget.removeRow(int(button_id))
        self.curMeetingCount -= 1
        self.closeBtns.remove(self.closeBtns[int(button_id)])
        for i in range(self.curMeetingCount):       # Adjust button ids according to row id
            self.closeBtns[i].setObjectName(str(i))
        self.meetingData.remove(self.meetingData[int(button_id)])  # remove data from that specific row from the meeting id

    def saveTable(self):
        if self.checkData():
            data = []   # contains pure data
            rows = []
            for x in range(len(self.meetingData)):
                for i in range(6):
                    if self.meetingData[x][i].objectName() == "Text":
                        data.append(self.meetingData[x][i].text())
                    elif self.meetingData[x][i].objectName() == "DateTime":
                        data.append(self.meetingData[x][i].text())
                    elif self.meetingData[x][i].objectName() == "CheckBox":
                        data.append(self.meetingData[x][i].checkState())
                rows.append(data)
                data = []
            meeting = DataFrame(rows, columns=('Name', 'ID', 'Password', 'DateTime', 'Audio', 'Video'))
            print(meeting)
            print("\n")
            print(meeting["DateTime"])
            print("\n")
            print(meeting.set_index("DateTime"))
            self.sql.enterData(meeting)
            self.startThread()
        else:
            return

    def checkData(self):
        checked = True
        for x in range(len(self.meetingData)):

            length = len(self.meetingData[x][1].text().replace(" ", ""))
            if 9 > length or length > 11:
                self.meetingData[x][1].setStyleSheet("color: red;")
                checked = False
            else:
                self.meetingData[x][1].setStyleSheet("color: black;")

            curTime = datetime.now()
            meetingTime = str(curTime.year) + '-' + self.meetingData[x][3].text() + ':00'
            meetingTime = datetime.strptime(meetingTime, '%Y-%d-%b , %H:%M:%S')
            if meetingTime < curTime:
                self.meetingData[x][3].setStyleSheet("color: red;")
                checked = False
            else:
                self.meetingData[x][3].setStyleSheet("color: black;")

        return checked

    def restoreData(self):
        data = self.sql.readData()
        for x in range(len(data)):
            self.addMeeting()
            for y in range(len(data.columns)):
                if self.meetingData[x][y].objectName() == "Text":
                    self.meetingData[x][y].setText(data.loc[x][y])
                if self.meetingData[x][y].objectName() == "DateTime":
                    dateTime = QDateTime().fromString(data.loc[x][y], 'dd-MMM , hh:mm')     # need to convert datetime format from db, text/string into datetime
                    self.meetingData[x][y].setDateTime(dateTime)
                if self.meetingData[x][y].objectName() == "CheckBox":
                    self.meetingData[x][y].setCheckState(int(data.loc[x][y]))   # box is check (2) else (0), convert text/string format into integer

    def startThread(self):
        meetingList = self.sql.readData()
        self.flag = False
        self.timerThread = Thread(target=self.timer, args=(meetingList,))
        sleep(1)
        self.timerThread.start()

    def timer(self, meetings):
        self.flag = True        #
        while self.flag:        # timer infinitely keep checking the current time and time of the meeting so that it can start the schedule meeting
            curTime = str(datetime.now().strftime('%d-%b , %H:%M:%S'))
            self.ui.displayTime.setText(f"Time : {curTime}")
            for meetingTime in meetings['DateTime']:
                if curTime == (meetingTime + ':00'):
                    if not self.checkNetwork():
                        self.startMeeting(meetingTime, meetings)
                        self.deleteMeeting(list(meetings['DateTime']).index(meetingTime))
                        self.saveTable()
            sleep(1)

    def checkNetwork(self):
        not_connected = True
        timeout = time() + 30
        while not_connected and timeout > time():
            try:
                urlopen('http://google.com')
                not_connected = False
            except:
                not_connected = True
            sleep(1)
        return not_connected

    def startMeeting(self, time, meeting):
        meetingDetails = meeting.set_index('DateTime')
        name = meetingDetails['Name'][time]
        Id = meetingDetails['ID'][time]
        passwd = meetingDetails['Password'][time]
        no_audio = meetingDetails['Audio'][time]
        no_video = meetingDetails['Video'][time]

        # HERE
        # notification.notify("ZoomAuto", "Meeting has started", "ZoomAuto", './ZoomAuto.ico')
        try:
            zoomWin = Application(backend='uia').start(r"C:\Users\JasonYeo\AppData\Roaming\Zoom\bin\Zoom.exe").connect(title='Zoom Workplace', timeout=100)
            #zoomWin.Dialog.print_control_identifiers()
        except timings.TimeoutError:
            try:
                zoomWin = Application(backend='uia').start(r"C:\Users\JasonYeo\AppData\Roaming\Zoom\bin\Zoom.exe").connect(title='Zoom Workplace', timeout=100)
                # notification.notify("ZoomAuto", "Bad Internet Connection", "ZoomAuto", './ZoomAuto.ico')
            except timings.TimeoutError:
                # notification.notify("ZoomAuto", "Zoom Not Installed, Meeting Failed", "ZoomAuto", './ZoomAuto.ico')
                print("")

        homeTab = zoomWin.Dialog.child_window(title="Home 1 of 4", control_type="TabItem").wrapper_object()
        homeTab.click_input()

        joinBtn = zoomWin.Dialog.child_window(title="Join", control_type="Button").wrapper_object()
        joinBtn.click_input()

        joinWin = Application(backend='uia').connect(title="Join meeting", timeout=100)
        idBox = joinWin.Dialog.child_window(title="Meeting ID or personal link name", control_type="Edit").wrapper_object()
        idBox.type_keys(Id, with_spaces=True)

        nameBox = joinWin.Dialog.child_window(title="Enter your name", control_type="Edit").wrapper_object()
        nameBox.click_input()
        nameBox.type_keys("^a{BACKSPACE}")
        nameBox.type_keys(name, with_spaces=True)
        # HERE

        audio = joinWin.Dialog.child_window(title="Don't connect to audio", control_type="CheckBox").wrapper_object()
        video = joinWin.Dialog.child_window(title="Turn off my video", control_type="CheckBox").wrapper_object()
        audio_ts = audio.get_toggle_state()
        video_ts = video.get_toggle_state()

        if no_audio == 0 and audio_ts == 1:
            audio.toggle()
        if no_audio == 2 and audio_ts == 0:
            audio.toggle()

        if no_video == 0 and video_ts == 1:
            video.toggle()
        if no_video == 2 and video_ts == 0:
            video.toggle()

        #
        joinBtn = joinWin.Dialog.child_window(title="Join", control_type="Button").wrapper_object()
        joinBtn.click_input()

        try:
            passwdWin = Application(backend='uia').connect(title="Enter meeting passcode", timeout=100)
            passwdBox = passwdWin.Dialog.child_window(title="Meeting passcode", control_type="Edit").wrapper_object()
            passwdBox.type_keys(passwd, with_spaces=True)

            meetingJoinBtn = passwdWin.Dialog.child_window(title="Join meeting", control_type="Button").wrapper_object()
            meetingJoinBtn.click_input()
            # notification.notify("ZoomAuto", "Meeting Joined", "ZoomAuto", './ZoomAuto.ico')

        except:
            try:
                Application(backend='uia').connect(title="Enter meeting passcode, That passcode was incorrect. Please try again.")
                # notification.notify("ZoomAuto", "Invalid Meeting ID", "ZoomAuto", './ZoomAuto.ico')
                # MIGHT NEED TO CHECK THE ID HERE
            except:
                # notification.notify("ZoomAuto", "Bad Internet Connection", "ZoomAuto", './ZoomAuto.ico')
                print()

        #  AREA TO IMPROVISE (FOR FURTHER)
        internal = Application(backend='uia').connect(title="Zoom Meeting", timeout=30)
        # internal.Dialog.print_control_identifiers()
        shareScreen = internal.Dialog.child_window(title="Share, Alt+S", control_type="Button").wrapper_object()
        shareScreen.click_input()

        internal2 = Application(backend='uia').connect(title="Select a window or an application that you want to share", timeout=30)
        # internal2.Dialog.print_control_identifiers()

        entireScreen = internal2.Dialog.child_window(title="Screen, share your entire screen", control_type="ListItem").wrapper_object()
        entireScreen.click_input()

        shareSound = internal2.Dialog.child_window(title="Share sound Select this option if you want others to hear sounds coming from your computer as well as see your shared screen", control_type="CheckBox").wrapper_object()
        shareSound.click_input()

        optimizeVideo = internal2.Dialog.child_window(title="Optimize for video clip Optimize screen sharing for viewing video clip.", control_type="CheckBox").wrapper_object()
        optimizeVideo.click_input()

        shareBtn = internal2.Dialog.child_window(title="Share Screen", control_type="Button")
        shareBtn.click_input()


if __name__ == "__main__":
    app = QApplication(sys.argv)    # creates application framework and interact with the OS
    mainWin = ZoomBotUI()           # calling the class above
    sys.exit(app.exec_())
