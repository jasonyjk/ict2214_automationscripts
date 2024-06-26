import subprocess
import os
session_file = 'INSERT SESSION FILE HERE'

# READ ME FIRST #
# THIS CONTROL SCRIPT ASSUMES YOU HAVE TWO WORKING TELEGRAM ACCOUNTS FOR USE.
# IF YOU ONLY HAVE ONE, YOU CAN RUN THE BOT SCRIPT MANUALLY INSTEAD.

# Function to run the automated messaging scripts.
def run_script(script_name):
    print("Reached RunScript function.")
    print("You may need to log in from here using your telephone number and an OTP. If you are running this script again after completion or termination of the previous instance of this script, please log in on the following new line.")
    return subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

# Function to send all output of scripts when script ends running.
def monitor_script(process):
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        if process.poll() is not None:
            break
    # Capture any remaining output after the process ends
    for remaining_output in process.stdout.readlines():
        print(remaining_output.strip())
    stderr = process.communicate()[1]
    return process.returncode, stderr

def main():

    # Removes session file from local folder. This ensures that every time the script is run, it's a new fresh instance
    # of itself. Telegram uses this session file to log you in automatically every time to the API, so to ensure that
    # it doesn't do that, delete this session file.
    if os.path.exists(session_file):
        os.remove(session_file)
        print(f"Deleted session file: {session_file}")

    # Run the first script
    print("Starting the first script...")
    process1 = run_script('automated_msg_1.py')
    #print("Script has completed running.")
    returncode, stderr = monitor_script(process1)
    
    # Check if the first script terminated due to FloodWaitError
    if returncode == 1:
        print("FloodWaitError detected. Switching to Script 2")
        
        # Run the second script
        print("Starting Second Script")
        process2 = run_script('automated_msg_2.py')
        returncode, stderr = monitor_script(process2)

        if returncode == 0:
            print("Script 2 completed successfully.")
        else:
            print(f"sScript 2 failed with return code {returncode}.")
            print(f"stderr: {stderr}")
    else:
        print(f"Script 1 failed with return code {returncode}.")
        print(f"FloodWaitError hit. Please wait for the number of seconds as mentioned above.")

if __name__ == "__main__":
    main()