import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
# NEW IMPORTS FOR WAITING
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon_playlist(url):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    driver.get(url)
    print("Firefox opened. Please log in and open the desired playlist.")
    input("Press ENTER in this terminal once the playlist page is fully loaded...")

    tracks = []
    seen_track_ids = set()

    def capture_visible_tracks():
        """Helper to find and parse accessibility labels currently on screen."""
        elements = driver.find_elements(By.CSS_SELECTOR, "div.a11y")
        for el in elements:
            try:
                label = el.get_attribute("aria-label")
                if label and "," in label:
                    parts = [p.strip() for p in label.split(",")]
                    title, artist = parts[0], parts[1]
                    track_id = f"{title}-{artist}".lower().strip()
                    if track_id not in seen_track_ids and title != "":
                        tracks.append({"title": title, "artist": artist})
                        seen_track_ids.add(track_id)
                        print(f"✅ Captured: {title} by {artist}")
            except: continue

    # 1. Wait for elements to appear
    print("Waiting for playlist to render...")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.a11y")))

    # 2. Capture and Scroll Loop
    print("Scraping tracks... please wait.")
    for i in range(12): # Increased range slightly
        capture_visible_tracks()
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1.5)

    # 3. Final Save
    with open("amazon_tracks.json", "w") as f:
        json.dump(tracks, f, indent=4)
    
    print(f"\n✅ Success! Captured {len(tracks)} unique tracks.")
    driver.quit()

if __name__ == "__main__":
    url = input("Paste your Amazon Music Playlist URL: ")
    scrape_amazon_playlist(url)