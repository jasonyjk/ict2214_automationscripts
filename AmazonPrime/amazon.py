#  Import necessary libraries
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function simulates human-like typing, entering one character at a time with a slight random delay.
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))  # Random delay between keystrokes to mimic human typing speed.


# Function to log in to Amazon Prime Video
def login_to_prime(driver, email, password):
    driver.get("https://www.primevideo.com/")
    time.sleep(2)  # Brief pause to ensure the page has loaded.

    try:
        # Click on "Prime Member? Sign in" link
        # Locate and click the sign-in link for Prime members using explicit waits to handle dynamic elements.
        sign_in_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'DVPAWebWidgetsCustomComponents_Button__button')]//span[text()='Prime Member? Sign in']"))
        )
        sign_in_link.click()
        print("Clicked on 'Prime Member? Sign in' link")
    except Exception as e:
        print(f"Error clicking 'Prime Member? Sign in' link: {e}")
        return False

    try:
        # Wait for the email field to be present
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        print("Found 'Email or mobile phone number' field")
    except Exception as e:
        print(f"Error finding 'Email or mobile phone number' field: {e}")
        return False

    time.sleep(random.uniform(1, 2))  # Short wait for the login page to load

    try:
        # Enter the email and click continue
        human_typing(email_field, email)
        driver.find_element(By.ID, "continue").click()
        print("Entered email and clicked 'Continue'")
    except Exception as e:
        print(f"Error entering email or clicking 'Continue': {e}")
        return False

    try:
        # Wait for the password field to be present
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        print("Found 'Password' field")
    except Exception as e:
        print(f"Error finding 'Password' field: {e}")
        return False

    time.sleep(random.uniform(1, 2))  # Short wait for the password field to be present

    try:
        # Enter the password and click sign in
        human_typing(password_field, password)
        driver.find_element(By.ID, "signInSubmit").click()
        print("Entered password and clicked 'Sign in'")
    except Exception as e:
        print(f"Error entering password or clicking 'Sign in': {e}")
        return False

    return True


# Function to get video URLs from the page
def get_video_urls(driver):
    # Extract video URLs from the current page, removing duplicates to avoid reprocessing.
    video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/dp/") or contains(@href, "/detail/")]')
    video_urls = [element.get_attribute('href') for element in video_elements if element.get_attribute('href')]
    video_urls = list(set(video_urls))  # Remove duplicates
    return video_urls


# Function to click the play button, making extensive use of XPath to
# accommodate various possible button states and styles.
def click_play_button(driver):
    try:
        play_button = WebDriverWait(driver, 5).until(
            # EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='play' or @data-automation-id='play' or contains(@class, '_1jWggM CvltKZ fbl-btn _2Pw7le') or @aria-label='Continue watching' or starts-with(@aria-label, 'Play')]"))
            # EC.element_to_be_clickable((By.XPATH, "//a[translate(@data-testid, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='play' or translate(@data-automation-id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='play' or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '_1jWggM CvltKZ fbl-btn _2Pw7le') or translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='continue watching' or starts-with(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'play')]"))
            # contains is necessary in the event the aria-label has extra word front and back
            # This complex XPath handles various formats of the play button found in Prime Video's UI, using multiple conditions to ensure robustness:
            EC.element_to_be_clickable((By.XPATH,
                                        "//a[translate(@data-testid, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='play' or translate(@data-automation-id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='play' or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '_1jWggM CvltKZ fbl-btn _2Pw7le') or contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue watching') or contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'play')]"))
        )
        play_button.click()
        print("Clicked play button")
        return True
    except Exception as e:
        print(f"Could not find or click play button: {e}")
        return False

# Explanation for complex XPath in click_play_button:
# 1. **translate()**: Converts text to lowercase to ensure case-insensitivity, accommodating different HTML markups.
# 2. **Multiple conditions**: Looks for the play button across various attributes (data-testid, data-automation-id,
# class, aria-label), reflecting the button's possible dynamic representations on the webpage.


# Selects a random video from the list of URLs and attempts to play it.
def select_random_video(driver, storefronts):
    storefront = random.choice(storefronts)  # Randomly picks one storefront URL.
    driver.get(storefront)  # Navigates to the chosen storefront.
    time.sleep(5)

    video_urls = get_video_urls(driver)  # Retrieves video URLs from the page.
    if video_urls:
        random_video_url = random.choice(video_urls)  # Selects a random video URL.
        driver.get(random_video_url)  # Navigates to the video page.
        time.sleep(5)
        click_play_button(driver)  # Attempts to start the video.
    else:
        print("No videos found on the page.")


# Main execution function: logs in and navigates through video selections.
def main():
    email = ""   # Placeholder for user email.
    password = ""  # Placeholder for user password.

    # Setup for Selenium WebDriver.
    chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update the path to your chromedriver.
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        login_success = login_to_prime(driver, email, password)  # Attempts to log in.
        if not login_success:
            return

        storefronts = [  # URLs for different video categories on Amazon Prime.
            "https://www.primevideo.com/storefront/ref=atv_hm_hom_c_9zZ8D2_hom",
            "https://www.primevideo.com/storefront/ref=atv_hm_hom_c_9zZ8D2_hom?contentType=movie&contentId=home",
            "https://www.primevideo.com/storefront/ref=atv_hm_hom_c_9zZ8D2_hom?contentType=tv&contentId=home",
            "https://www.primevideo.com/categories/ref=atv_hm_hom_c_9zZ8D2_cat",
            "https://www.primevideo.com/genre/action/ref=atv_hm_fin_c_YyAsEb_1_1?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/documentary/ref=atv_hm_fin_c_YyAsEb_1_3?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/drama/ref=atv_hm_fin_c_YyAsEb_1_4?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/fantasy/ref=atv_hm_fin_c_YyAsEb_1_5?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/horror/ref=atv_hm_fin_c_YyAsEb_1_6?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/kids/ref=atv_hm_fin_c_YyAsEb_1_7?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/suspense/ref=atv_hm_fin_c_YyAsEb_1_8?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/romance/ref=atv_hm_fin_c_YyAsEb_1_9?jic=8%7CEgNhbGw%3D",
            "https://www.primevideo.com/genre/science-fiction/ref=atv_hm_fin_c_YyAsEb_1_10?jic=8%7CEgNhbGw%3D"
        ]

        # Loop to allow user interaction and video selection.
        while True:
            select_random_video(driver, storefronts)
            print("Watching video... Press 'n' to select a new random video, or 'q' to quit.")

            user_input = input().strip().lower()
            if user_input == 'q':
                break
            elif user_input == 'n':
                driver.back()
                time.sleep(2)

    finally:
        driver.quit()  # Ensures the driver is properly closed when done.


if __name__ == "__main__":
    main()
