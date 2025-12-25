import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

def scrape_amazon_playlist(url):
    # 1. Setup Firefox
    options = webdriver.FirefoxOptions()
    # options.add_argument("--private") # Optional: Open in private mode
    
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()), 
        options=options
    )
    
    driver.get(url)
    print("Firefox opened. Please log in and open the desired playlist.")
    input("Press ENTER in this terminal once the playlist page is fully loaded...")

    tracks = []
    seen_track_ids = set()

    # 2. Scrolling Logic (Refined for Firefox)
    print("Scraping tracks... please wait.")
    
    # We use a loop to scroll down and capture data in chunks
    for i in range(10): # Increase this number for very long playlists
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1.5) # Give Firefox a moment to render the new elements
        
        rows = driver.find_elements(By.TAG_NAME, "music-image-row")
        
        for row in rows:
            a11y_elements = driver.find_elements(By.CSS_SELECTOR, "div.a11y")

            for el in a11y_elements:
                try:
                    label = el.get_attribute("aria-label")
                    
                    # We expect a format like: "Song Name, Artist, Album"
                    if label and "," in label:
                        parts = [p.strip() for p in label.split(",")]
                        
                        # Usually: [0] is Title, [1] is Artist
                        title = parts[0]
                        artist = parts[1]
                        
                        track_id = f"{title}-{artist}".lower().strip()
                        if track_id not in seen_track_ids:
                            tracks.append({
                                "title": title, 
                                "artist": artist,
                                "full_label": label # Keeping the full string just in case
                            })
                            seen_track_ids.add(track_id)
                            print(f"✅ Captured: {title} by {artist}")
                except Exception as e:
                    continue
    # 3. Save to JSON
    with open("amazon_tracks.json", "w") as f:
        json.dump(tracks, f, indent=4)
    
    print(f"\n✅ Success! Captured {len(tracks)} unique tracks.")
    driver.quit()

if __name__ == "__main__":
    # Test with a public or your own playlist URL
    url = input("Paste your Amazon Music Playlist URL: ")
    scrape_amazon_playlist(url)