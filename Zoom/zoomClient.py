from pywinauto.application import Application

# Start the Zoom application and connect to the Zoom Workplace window.
zoomWin = Application(backend='uia').start(r"C:\Users\XXX\AppData\Roaming\Zoom\bin\Zoom.exe").connect(title='Zoom Workplace', timeout=100)
# zoomWin.Dialog.print_control_identifiers()
# Access the "Home" tab in the Zoom application's main window.
homeTab = zoomWin.Dialog.child_window(title="Home 1 of 4", control_type="TabItem").wrapper_object()
homeTab.click_input()
# # Access and click the "Join" button in the Zoom main window to open the join meeting dialog.
joinBtn = zoomWin.Dialog.child_window(title="Join", control_type="Button").wrapper_object()
joinBtn.click_input()
#
# # Connect to the "Join meeting" window that opens after clicking "Join".
joinWin = Application(backend='uia').connect(title="Join meeting", timeout=100)
# joinWin.Dialog.print_control_identifiers()
# # Access the "Meeting ID or personal link name" input field and type in the meeting ID.
idBox = joinWin.Dialog.child_window(title="Meeting ID or personal link name", control_type="Edit").wrapper_object()
idBox.type_keys("XXX XXX XXXX", with_spaces=True)  # replace "" with the meeting id.
# # Access the "Enter your name" input field, clear any existing text, and type in the participant's name.
nameBox = joinWin.Dialog.child_window(title="Enter your name", control_type="Edit").wrapper_object()
nameBox.click_input()
nameBox.type_keys("^a{BACKSPACE}")   # Clears any text by selecting all and pressing BACKSPACE.
nameBox.type_keys("XXX", with_spaces=True)   # replace "" with the participant's name.
# # Access and click the "Join" button on the "Join meeting" dialog.
joinBtn = joinWin.Dialog.child_window(title="Join", control_type="Button").wrapper_object()
joinBtn.click_input()
#
# # Connect to the "Enter meeting passcode" window.
passwdWin = Application(backend='uia').connect(title="Enter meeting passcode", timeout=100)
# # passwdWin.Dialog.print_control_identifiers()
# # Access the "Meeting passcode" input field and type in the meeting passcode.
passwdBox = passwdWin.Dialog.child_window(title="Meeting passcode", control_type="Edit").wrapper_object()
passwdBox.type_keys("XXXX", with_spaces=True)  # replace "" with the meeting passcode.
# # Access and click the "Join meeting" button in the passcode window to finalize joining the meeting.
meetingJoinBtn = passwdWin.Dialog.child_window(title="Join meeting", control_type="Button").wrapper_object()
meetingJoinBtn.click_input()
