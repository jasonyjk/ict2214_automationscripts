import subprocess
import time

def run_bot(script_name):
    return subprocess.Popen(['python', script_name])

if __name__ == "__main__":
    # Run both bot scripts
    sender_bot_process = run_bot('Discord/MessageBot1.py')
    receiver_bot_process = run_bot('Discord/MessageBot2.py')

    try:
        # Keep the master script running to monitor the bots
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # If the user interrupts (Ctrl+C), terminate both bot processes
        sender_bot_process.terminate()
        receiver_bot_process.terminate()
        print("Bots terminated.")