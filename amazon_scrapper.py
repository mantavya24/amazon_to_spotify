import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
# NEW IMPORTS FOR WAITING
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_playlists(urls):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    all_playlists = []

    for idx, url in enumerate(urls):
        print(f"\n--- Processing Playlist {idx+1}/{len(urls)} ---")
        driver.get(url)
        if idx == 0:
            print("Firefox opened. Please log in if necessary and navigate to the playlist.")
        else:
            print(f"Navigated to playlist {idx+1}.")
            
        input("Press ENTER in this terminal once the playlist page is fully loaded...")
        
        # Attempt to capture the playlist name from the H1 tag or the document title
        try:
            playlist_name = driver.find_element(By.CSS_SELECTOR, "h1").text
        except:
            playlist_name = driver.title.replace(" on Amazon Music", "").replace(" on Amazon", "").strip()
            if not playlist_name:
                playlist_name = f"Amazon Playlist {idx+1}"
        print(f"Identified Playlist Name: {playlist_name}")

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
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.a11y")))
        except:
             pass

        # 2. Capture and Scroll Loop
        print("Scraping tracks... please wait.")
        for i in range(12): # Increased range slightly
            capture_visible_tracks()
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1.5)
            
        all_playlists.append({
            "playlist_name": playlist_name,
            "tracks": tracks
        })

    # 3. Final Save
    with open("amazon_tracks.json", "w") as f:
        json.dump(all_playlists, f, indent=4)
    
    total_tracks = sum(len(p["tracks"]) for p in all_playlists)
    print(f"\n✅ Success! Captured {total_tracks} unique tracks across {len(urls)} playlist(s).")
    driver.quit()

if __name__ == "__main__":
    print("Welcome to Amazon Playlist Scraper!")
    print("1. Scrape a single playlist URL")
    print("2. Scrape from playlist_urls.txt (Batch Mode)")
    choice = input("Enter 1 or 2: ").strip()

    urls_to_scrape = []
    
    if choice == '1':
        url = input("Paste your Amazon Music Playlist URL: ").strip()
        if url:
            urls_to_scrape.append(url)
    elif choice == '2':
        try:
            with open("playlist_urls.txt", "r") as f:
                urls_to_scrape = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            if not urls_to_scrape:
                print("playlist_urls.txt is empty! Please add some URLs.")
        except FileNotFoundError:
            print("playlist_urls.txt not found! Creating the file. Please add your URLs and run again.")
            with open("playlist_urls.txt", "w") as f:
                f.write("# Paste your Amazon playlist URLs here, one per line\n")
    else:
        print("Invalid choice.")
        
    if urls_to_scrape:
        scrape_playlists(urls_to_scrape)