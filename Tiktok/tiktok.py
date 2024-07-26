#  Import necessary libraries
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


# Simulates human-like typing to emulate more natural interactions with input fields.
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))


# Log into TikTok using username and password, navigating through the login process.
def login_to_tiktok(driver, username, password):
    driver.get("https://www.tiktok.com")
    time.sleep(random.uniform(1, 3))  # Short wait for the page to load

    try:
        # Click on "Log in" button
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='nav-login-button']"))
        )
        login_button.click()

        # Click on "Use phone / email / username"
        use_phone_email_username = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[@data-e2e='channel-item' and .//div[contains(text(),'Use phone / email / username')]]"))
        )
        use_phone_email_username.click()

        # Click on "Log in with email or username"
        login_with_email_username = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log in with email or username')]"))
        )
        login_with_email_username.click()

        # Enter the username and password in their respective fields.
        email_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email or username']"))
        )
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
        )

        human_typing(email_field, username)
        human_typing(password_field, password)

        # Click the login button.
        driver.find_element(By.XPATH, "//button[@data-e2e='login-button']").click()

        # Pause to allow manual CAPTCHA solving
        input("Solve the CAPTCHA manually and press Enter to continue...")

        time.sleep(random.uniform(3, 5))  # Additional wait after CAPTCHA for login completion.
    except Exception as e:
        print(f"Error during login: {e}")
        return False

    return True


# Automates watching TikTok videos by interacting with video elements.
def watch_tiktok_videos(driver):
    try:
        # Scroll the element into view and click on the first video to start playing
        video = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-e2e='explore-item']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", video)   # Scroll the video into view.
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-e2e='explore-item']"))
        )
        video.click()  # Start playing the video.

        time.sleep(3)  # Pause for 3 seconds.

        # Cancel the floating popup using JavaScript to bypass overlays
        floating_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='css-a2a8a8-DivIconCloseContainer e1vz198y4']"))
        )

        # Click to cancel the floating popup using JavaScript to bypass overlays
        driver.execute_script("arguments[0].click();", floating_button)

        time.sleep(3)  # Pause for another 3 seconds.

        # Enable the auto-scroll feature using JavaScript to bypass overlays
        auto_scroll_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='css-weccem-DivAutoScrollButtonContainer etnnns70']"))
        )

        # Click the auto-scroll button using JavaScript to bypass overlays
        driver.execute_script("arguments[0].click();", auto_scroll_button)

        print("First video clicked and auto-scroll enabled. Watching videos...")

        # Keep the browser running
        while True:
            time.sleep(600)  # Sleep for a long time, adjust as necessary

    except Exception as e:
        print(f"Error during video watching setup: {e}")
        driver.refresh()
        time.sleep(random.uniform(5, 10))  # Short wait before retrying


def main():
    username = ""  # Replace with your actual username.
    password = ""  # Replace with your actual password.

    # Setup for Selenium WebDriver.
    chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update the path to your chromedriver.
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")

    driver = uc.Chrome(service=chrome_service, options=chrome_options)

    try:
        login_success = login_to_tiktok(driver, username, password)  # Attempt to log in.
        if login_success:
            watch_tiktok_videos(driver)   # Start watching videos if login is successful.
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            driver.quit()  # Ensure the driver is properly closed.
        except Exception as e:
            print(f"Error closing the driver: {e}")


if __name__ == "__main__":
    main()
