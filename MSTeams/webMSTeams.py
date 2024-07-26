#  Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# NEED pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to log in to Microsoft Teams
def login_to_teams(driver, email, password):
    driver.get("https://teams.live.com/v2/?ref=msa-guest-login")

    # Wait for the login page to load and enter email
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "loginfmt"))).send_keys(email)
    driver.find_element(By.ID, "idSIButton9").click()

    # Wait for the password page to load and enter password
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "passwd"))).send_keys(password)
    driver.find_element(By.ID, "idSIButton9").click()

    # Wait for the stay signed in page and click Yes
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "acceptButton"))).click()

    # Handle optional prompt that may appear after logging in.
    try:
        # Wait for the continue button to be present
        continue_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tid='continue-button-fre']"))
        )
        continue_button.click()
    except Exception as e:
        print("Error clicking the Continue button:", e)


# Function to automatically accept incoming calls.
def accept_call(driver):
    while True:
        try:
            # Check for incoming call dialog
            # Continuously check for the presence of the call acceptance button.
            call_dialog = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Accept with audio']")))
            time.sleep(5)  # Delay to handle any UI delays or updates.
            call_dialog.click()
            print("Call accepted")
            return  # Exit the loop once the call is accepted.
        except Exception as e:
            print("No incoming call detected, retrying...")
        time.sleep(5)  # Wait before checking again.


# Main function to orchestrate the automation process.
def main():
    # Credentials for login.
    email = ""
    password = ""

    # Configure Chrome options to optimize for automation.
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Disable browser notifications.
    chrome_options.add_argument("--start-maximized")  # Start Chrome maximized.
    chrome_options.add_argument(
        "--use-fake-ui-for-media-stream")  # Automatically grant permissions for microphone and camera

    # Initialize the WebDriver with auto-managed Chrome driver.
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        login_to_teams(driver, email, password)

        # Main loop to handle incoming calls continuously.
        while True:
            accept_call(driver)
            # Keep the browser open and maintain the call session
            while "teams.microsoft.com" in driver.current_url:
                time.sleep(10)  # Check every 10 seconds if the call is still active
            print("Call ended, waiting for new calls...")
    finally:
        driver.quit()  # Ensure the driver is properly closed.


if __name__ == "__main__":
    main()
