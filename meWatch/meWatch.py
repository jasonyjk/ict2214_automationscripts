#  Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import threading
import logging

# Configure logging to capture events and errors for debugging. Logs are stored in a file.
logging.basicConfig(filename='../../Others/mewatch_automation.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Dictionary to hold channel names and their corresponding URLs for easy navigation.
CATEGORIES = {
    "FREE": {
        # Each channel is associated with a direct URL to the full-screen player
        "Channel 5": "https://www.mewatch.sg/channels/channel-5/97098?player-fullscreen",
        "Channel 8": "https://www.mewatch.sg/channels/channel-8/97104?player-fullscreen",
        "Channel U": "https://www.mewatch.sg/channels/channel-u/97129?player-fullscreen",
        "Suria": "https://www.mewatch.sg/channels/suria/97084?player-fullscreen",
        "Vasantham": "https://www.mewatch.sg/channels/vasantham/97096?player-fullscreen",
        "CNA": "https://www.mewatch.sg/channels/cna/97072?player-fullscreen",
        "oktolidays": "https://www.mewatch.sg/channels/oktolidays/186574?player-fullscreen",
        "SPL01": "https://www.mewatch.sg/channels/spl01/98200?player-fullscreen",
        "SPL02": "https://www.mewatch.sg/channels/spl02/98201?player-fullscreen",
        "LIVE 1": "https://www.mewatch.sg/channels/live-1/97073?player-fullscreen",
        "LIVE 2": "https://www.mewatch.sg/channels/live-2/97078?player-fullscreen",
        "LIVE 5": "https://www.mewatch.sg/channels/live-5/98202?player-fullscreen",
        "LIVE 6": "https://www.mewatch.sg/channels/live-6/204746?player-fullscreen",
        "NOW 80s": "https://www.mewatch.sg/channels/now-80s/158965?player-fullscreen",
        "NOW 70s": "https://www.mewatch.sg/channels/now-70s/158964?player-fullscreen",
        "NOW Rock": "https://www.mewatch.sg/channels/now-rock/158963?player-fullscreen",
        "TRACE Urban": "https://www.mewatch.sg/channels/trace-urban/158962?player-fullscreen"
    },
    "PREMIUM": {
        "SPOTV Stadia": "https://www.mewatch.sg/channels/spotv-stadia/158969?player-fullscreen",
        "ROCK Entertainment": "https://www.mewatch.sg/channels/rock-entertainment/227348?player-fullscreen",
        "ROCK Action": "https://www.mewatch.sg/channels/rock-action/227349?player-fullscreen",
        "Global Trekker": "https://www.mewatch.sg/channels/global-trekker/158961?player-fullscreen",
        "Animax": "https://www.mewatch.sg/channels/animax/242030?player-fullscreen",
        "GEM": "https://www.mewatch.sg/channels/gem/242036?player-fullscreen",
        "CinemaWorld": "https://www.mewatch.sg/channels/cinemaworld/382872?player-fullscreen",
        "HBO": "https://www.mewatch.sg/channels/hbo/97137?player-fullscreen",
        "HBO Hits": "https://www.mewatch.sg/channels/hbo-hits/97140?player-fullscreen",
        "HBO Family": "https://www.mewatch.sg/channels/hbo-family/97147?player-fullscreen",
        "HBO Signature": "https://www.mewatch.sg/channels/hbo-signature/97146?player-fullscreen",
        "Cinemax": "https://www.mewatch.sg/channels/cinemax/97155?player-fullscreen"
    }
}

# Global flag to control termination of the video watching loop.
stop_watching = False


def watch_video(driver, url):
    global stop_watching
    try:
        driver.get(url)  # Navigate the web driver to the provided channel URL.
        logging.info(f"Watching video: {url}")  # Log the URL of the video being watched.
        while not stop_watching:
            time.sleep(1)  # This loop runs every second to check if the stop_watching flag has been set.
    except Exception as e:
        # Log any exceptions that occur during the process.
        logging.error(f"An error occurred while watching the video {url}: {e}")


def main():
    global stop_watching

    # Set up Selenium WebDriver with Chrome options to minimize interruptions during video playback.
    chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update the path to your chromedriver.
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Disable notifications that could disrupt the viewing.
    chrome_options.add_argument("--disable-popup-blocking") # Disable pop-ups for smoother navigation.
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        while True:
            print("Select a category:")
            for i, category in enumerate(CATEGORIES.keys(), 1):
                print(f"{i}. {category}")  # Display all available categories to the user.

            category_choice = int(input("Enter choice: "))
            if category_choice not in range(1, len(CATEGORIES) + 1):
                print("Invalid choice")
                continue  # If invalid input, prompt again.

            category = list(CATEGORIES.keys())[category_choice - 1]
            subcategory = CATEGORIES[category]

            print("Select a channel:")
            for i, (channel, url) in enumerate(subcategory.items(), 1):
                print(f"{i}. {channel}")   # Display channels within the selected category.

            channel_choice = int(input("Enter choice: "))
            if channel_choice not in range(1, len(subcategory) + 1):
                print("Invalid choice")
                continue  # If invalid input, prompt again.

            channel = list(subcategory.keys())[channel_choice - 1]
            channel_url = subcategory[channel]

            # Reset the stop_watching flag to ensure the video watching thread runs.
            stop_watching = False

            # Create a new thread for watching the video.
            watch_thread = threading.Thread(target=watch_video, args=(driver, channel_url))
            watch_thread.start()  # Start the video watching thread.

            # Wait for the user to decide to switch channels
            while True:
                user_input = input("Enter 'switch' to change channel or 'exit' to quit: ").strip().lower()
                if user_input == 'switch':
                    stop_watching = True  # Set the flag to stop the current video watching thread.
                    watch_thread.join()  # Ensure the thread completes before continuing.
                    break  # Break out of the loop to select a new channel.
                elif user_input == 'exit':
                    stop_watching = True  # Set the flag to stop the current video watching thread.
                    watch_thread.join()  # Ensure the thread completes before exiting.
                    return
                else:
                    print("Invalid input. Please enter 'switch' or 'exit'.")
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    finally:
        driver.quit()  # Close the WebDriver to free resources.


if __name__ == "__main__":
    main()
