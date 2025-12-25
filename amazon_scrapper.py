from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

def get_amazon_tracks(playlist_url):
    # Setup Chrome
    options = webdriver.ChromeOptions()
    # We leave it in non-headless mode so YOU can log in manually
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(playlist_url)
    
    print("Please log in and navigate to your playlist if not already there.")
    input("Press Enter once the playlist is fully loaded on screen...")

    tracks = []
    
    # Selector strategy: Amazon usually puts track info in 'music-image-row' or similar classes
    # Note: These selectors change often. You might need to 'Inspect' the page.
    rows = driver.find_elements(By.TAG_NAME, "music-image-row")
    
    # ... inside the loop of get_amazon_tracks ...
    rows = driver.find_elements(By.TAG_NAME, "music-image-row")

    for row in rows:
        try:
            # Find the primary link (Song Title)
            title_element = row.find_element(By.CSS_SELECTOR, "music-link[kind='primary'] a")
            title = title_element.text
            
            # Find the secondary link (Artist)
            artist_element = row.find_element(By.CSS_SELECTOR, "music-link[kind='secondary'] a")
            artist = artist_element.text
            
            tracks.append({"title": title, "artist": artist})
            print(f"Captured: {title} by {artist}")
        except Exception as e:
            # Some rows might be headers or ads
            continue
            
    driver.quit()
    
    with open("amazon_playlist.json", "w") as f:
        json.dump(tracks, f, indent=4)
    
    print(f"Saved {len(tracks)} tracks to amazon_playlist.json!")

# Paste your Amazon playlist link here
get_amazon_tracks("https://music.amazon.com/user-playlists/YOUR_ID_HERE")s