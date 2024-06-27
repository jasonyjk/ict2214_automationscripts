#  Import necessary libraries
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


# Function to simulate human typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))


# Function to automate watching Douyin videos
def watch_douyin_videos(driver):
    try:
        # Navigate to the Douyin discover page
        driver.get("https://www.douyin.com/discover")
        time.sleep(random.uniform(1, 3))  # Short wait for the page to load

        # Close any dialog that might block the video view.
        close_dialog = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='dy-account-close']"))
        )
        close_dialog.click()

        # Scroll the element into view and click on the first video to start playing
        video = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='nFJH7DcV']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", video)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nFJH7DcV']"))
        )
        print(video.click())

        # Handle any popup that might appear after the first video click.
        popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='semi-button semi-button-primary ZzmnQURb']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", video)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='semi-button semi-button-primary ZzmnQURb']"))
        )
        popup.click()

        print("First video clicked. Watching videos...")

        # Keep the browser running to continue watching videos.
        while True:
            time.sleep(600)  # Sleep for a long time, adjust as necessary

    except Exception as e:
        print(f"Error during video watching setup: {e}")
        driver.refresh()
        time.sleep(random.uniform(5, 10))  # Short wait before retrying


def main():
    # Path to the ChromeDriver executable and browser options setup.
    chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update the path to your chromedriver.
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = uc.Chrome(service=chrome_service, options=chrome_options)

    try:
        watch_douyin_videos(driver)  # Call function to watch videos.
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            driver.quit()  # Ensure the driver is properly closed on script termination.
        except Exception as e:
            print(f"Error closing the driver: {e}")


if __name__ == "__main__":
    main()
