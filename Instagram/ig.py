import time
import os
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def save_credentials(username, password):
    with open("credentials.txt", "w") as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    if not os.path.exists("credentials.txt"):
        return None

    with open("credentials.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None


def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password


def read_usernames_from_file(file_path):
    with open(file_path, "r") as file:
        usernames = [line.strip() for line in file]
    return usernames


def remove_username_from_file(username, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != username:
                file.write(line)


def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))


def human_like_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))


def is_element_in_viewport(driver, element):
    element_location = element.location
    element_size = element.size
    viewport_height = driver.execute_script("return window.innerHeight")
    viewport_width = driver.execute_script("return window.innerWidth")

    in_viewport = (0 <= element_location['y'] <= viewport_height and
                   0 <= element_location['x'] <= viewport_width and
                   0 <= (element_location['y'] + element_size['height']) <= viewport_height and
                   0 <= (element_location['x'] + element_size['width']) <= viewport_width)

    print(f"Element in viewport: {in_viewport}")
    return in_viewport


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)

    return driver


def login_to_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    random_delay(3, 7)

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
    )

    human_like_typing(username_input, username)
    human_like_typing(password_input, password)
    password_input.send_keys(Keys.RETURN)
    random_delay(10, 15)

    for _ in range(3):  # Retry up to 3 times
        try:
            save_login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//div[contains(@class, 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37')]"))
            )
            save_login_button.click()
        except TimeoutException:
            print("Save login button not found or not clickable.")

        try:
            dismiss_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Dismiss']"))
            )
            dismiss_button.click()
        except TimeoutException:
            print("Dismiss button not found or not clickable.")

        try:
            notification_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, '_a9-- _ap36 _a9_1') and text()='Not Now']"))
            )
            notification_button.click()
            break
        except TimeoutException:
            print("Notification button not found or not clickable.")
            continue


def like_stories(driver, usernames):
    for follower in usernames:
        story_url = f"https://www.instagram.com/stories/{follower}"
        driver.get(story_url)
        random_delay(3, 7)

        view_story_xpath = "//div[@role='button' and text()='View Story']"
        like_button_xpath = "//div[@role='button' and @tabindex='0' and contains(@class,'x1i10hfl')]//*[name()='svg' and @aria-label='Like']"

        try:
            view_story_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, view_story_xpath))
            )
            print(f"[TRUE] User -> {follower} has a story up.")
            view_story_button.click()

            try:
                like_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, like_button_xpath))
                )
                print("Like button location before any action:", like_button.location)
                print("Like button size before any action:", like_button.size)

                if not is_element_in_viewport(driver, like_button):
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                                          like_button)
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, like_button_xpath))
                    )

                actions = ActionChains(driver)
                actions.move_to_element(like_button).click().perform()
                print("Liked the story successfully!")
                random_delay(2, 5)
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                print("Like button not found or not clickable.")
        except (NoSuchElementException, TimeoutException):
            print(f"[FALSE] User -> {follower} has no story up.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            remove_username_from_file(follower, "followers.txt")

        random_delay(25, 30)


if __name__ == "__main__":
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    followers_file = "followers.txt"
    usernames = read_usernames_from_file(followers_file)

    driver = setup_driver()
    try:
        login_to_instagram(driver, username, password)
        like_stories(driver, usernames)
    finally:
        driver.quit()
