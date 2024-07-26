#  Import necessary libraries
from pywinauto import Application
import time

# Start Teams application
teams_path = r'C:\Users\XXX\AppData\Local\Microsoft\Teams\current\Teams.exe'
app = Application(backend='uia').start(teams_path)

# Connect to the Teams main window based on its title. The specific title can vary, so it might need adjustments.
teams_window = app.window(title="Microsoft Teams, Main Window")

# Print control identifiers
# Uncomment to print out the identifiers for all controls within the Teams window, useful for debugging.
# teams_window.print_control_identifiers()

# Locate and click the button to switch to the new version of Teams if prompted.
yesBtn = teams_window.child_window(title="Did you mean to open the new Teams? Continuing to classic will disconnect any calls you're currently in Yes, go to new Teams", auto_id="goBackButton", control_type="Button")
yesBtn.click_input()

# Connect to a specific chat window by its title.
newWin = Application(backend='uia').connect(title="Chat | ITP Demo 2 | Microsoft Teams", timeout=100)
# Uncomment to print control identifiers for the new window, aiding in finding specific elements.
# newWin.Dialog.print_control_identifiers()

# # MAKE AUDIO CALL
time.sleep(5)  # Pause execution to stabilize the UI before making an audio call.
# Find and click the button to start an audio call within the chat window.
makeAudioCall = newWin.Dialog.child_window(title="Audio call", control_type="Button")
makeAudioCall.click_input()

# INSIDE AUDIO CALL
# Connect to the call window once the call has started.
newWin2 = Application(backend='uia').connect(title="ITP Demo 2 | Microsoft Teams", timeout=100)
# Print identifiers for the call window to help locate the hang-up button or other elements.
newWin2.Dialog.print_control_identifiers()

# LEAVE AUDIO CALL
time.sleep(60)   # set to leave after x seconds
# Locate and click the button to leave the audio call.
leaveAudioCall = newWin2.Dialog.child_window(title="Leave (Ctrl+Shift+H)", auto_id="hangup-button", control_type="Button")
leaveAudioCall.click_input()
