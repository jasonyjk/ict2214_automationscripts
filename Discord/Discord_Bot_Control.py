import subprocess
import time

# Function to run bots in Discord.
def run_bot(script_name):
    return subprocess.Popen(['python', script_name])

if __name__ == "__main__":
    # Run both bot scripts
    auto_msg_bot1 = run_bot('MessageBot1.py')
    auto_msg_bot2 = run_bot('MessageBot2.py')

    try:
        # Keep the master script running to monitor the bots
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # If the user interrupts (Ctrl+C), terminate both bot processes
        auto_msg_bot1.terminate()
        auto_msg_bot2.terminate()
        print("Bots terminated.")