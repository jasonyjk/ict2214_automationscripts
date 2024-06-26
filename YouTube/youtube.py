"""
Estimating Total Time:
Fixed watch time: 10 seconds (e.g. input).
Random delay between videos: 5 to 10 seconds.
Page loading and ad handling: Let's conservatively estimate this might total around 5 seconds per video.
"""

#  Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import random
import time


# Dictionary mapping YouTube categories to their respective URLs for easy access.
CATEGORIES = {
    "Trending": "https://www.youtube.com/feed/trending",
    "Music": "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ",
    "Movies": "https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D",
    "Gaming": "https://www.youtube.com/gaming",
    "News": "https://www.youtube.com/channel/UCYfdidRxbB8Qhf0Nx7ioOYw",
    "Sports": "https://www.youtube.com/channel/UCEgdi0XIXXZ-qJOFPf4JSKw",
    "Fashion & Beauty": "https://www.youtube.com/channel/UCrpQ4p1Ql_hG8rKXIKM1MOQ",
    "Podcasts": "https://www.youtube.com/podcasts"
}


def get_video_urls(driver, category_url):
    driver.get(category_url)
    time.sleep(5)  # Wait for the page to fully load before proceeding.

    video_urls = []

    # Locate subcategory elements by specific XPATH and store their URLs if they exist.
    subcategory_elements = driver.find_elements(By.XPATH, '//a[@id="endpoint" and contains(@href, "/browse/")]')
    subcategory_urls = [element.get_attribute('href') for element in subcategory_elements if element.get_attribute('href')]

    # If subcategories exist, navigate each and scrape video URLs.
    if subcategory_urls:
        for subcategory_url in subcategory_urls:
            driver.get(subcategory_url)
            time.sleep(5)  # Allow subcategory page to load.
            video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/watch?v=")]')
            video_urls.extend([element.get_attribute('href') for element in video_elements if element.get_attribute('href')])
    else:
        # If no subcategories, scrape video URLs directly from the main category page.
        video_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/watch?v=")]')
        video_urls = [element.get_attribute('href') for element in video_elements if element.get_attribute('href')]

    video_urls = list(set(video_urls))  # Remove duplicates to ensure each video is only processed once.
    return video_urls


def skip_ads(driver):
    try:
        # Try to find the "Skip Ad" button and click it if present.
        skip_button = driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button")
        if skip_button:
            skip_button.click()
            print("Skipped ad")
    except:
        # Skip this block if no skippable ad is found.
        pass

    try:
        # Try to find the close button for overlay ads and click it if present.
        close_button = driver.find_element(By.CLASS_NAME, "ytp-ad-overlay-close-button")
        if close_button:
            close_button.click()
            print("Closed overlay ad")
    except:
        # Skip this block if no overlay ad is found.
        pass


def watch_youtube_video(driver, url, duration):
    try:
        driver.get(url)
        print(f"Watching video: {url}")
        start_time = time.time()
        end_time = start_time + duration

        # Continuously check for ads and attempt to skip them during the video playback duration.
        while time.time() < end_time:
            skip_ads(driver)
            time.sleep(0.5)  # Check for ads every half second.
    except Exception as e:
        print(f"An error occurred while watching the video {url}: {e}")


def main():
    print("Select a YouTube category:")
    for i, category in enumerate(CATEGORIES.keys(), 1):
        print(f"{i}. {category}")

    category_choice = int(input("Enter choice (1-8): "))
    if category_choice not in range(1, 9):
        print("Invalid choice")
        return

    category = list(CATEGORIES.keys())[category_choice - 1]
    category_url = CATEGORIES[category]

    duration_per_video = int(input("Enter duration to watch each video (in seconds): "))

    # Set up the Selenium WebDriver with Chrome options to minimize unwanted pop-ups.
    chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'  # Update the path to your chromedriver.
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        watched_videos = set()
        video_urls = get_video_urls(driver, category_url)

        while True:
            # Refresh the list of video URLs if it's empty and try to retrieve new ones.
            if not video_urls:
                video_urls = get_video_urls(driver, category_url)
                if not video_urls:
                    print("No videos found. Retrying...")
                    time.sleep(10)
                    continue

            video_url = random.choice(video_urls)
            video_urls.remove(video_url)

            # Watch a video if it hasn't been watched before.
            if video_url not in watched_videos:
                watch_youtube_video(driver, video_url, duration_per_video)
                watched_videos.add(video_url)
                # Add a short delay between videos to mimic real user behavior.
                time.sleep(random.uniform(5, 10))
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        driver.quit()  # Ensure the WebDriver is closed properly.


if __name__ == "__main__":
    main()
