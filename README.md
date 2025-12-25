---
### 📄 `README.md`


```
# Amazon Music to Spotify Porter 🎵

A robust data migration tool built to transfer playlists from Amazon Music to Spotify. This project demonstrates advanced web scraping techniques, API integration, and secure OAuth 2.0 implementation.

## 🚀 The Challenge
Unlike Spotify, Amazon Music does not currently offer an open public Web API for personal playlist access. This "walled garden" approach usually prevents automated migration. 

**The Solution:** I developed a custom Selenium-based engine that utilizes **ARIA-label parsing** (Accessibility tree) to accurately extract track metadata even when standard DOM elements are obscured or nested within complex Web Components.

## ✨ Key Features
- **Intelligent Scraping:** Uses Selenium (Firefox/GeckoDriver) with a robust "Wait-and-Scroll" mechanism to handle lazy-loading virtual lists.
- **Accessibility-Based Extraction:** Pivots to `aria-label` attributes to ensure 100% metadata retrieval accuracy.
- **Fuzzy Matching:** Implements Levenshtein distance algorithms via `TheFuzz` to resolve discrepancies in song naming (e.g., matching "Song Title [Explicit]" to "Song Title").
- **OAuth 2.0 Integration:** Securely handles Spotify's Authorization Code Flow with proper redirect URI management.
- **Security First:** Utilizes `.env` management to prevent API credential leakage.

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **Automation:** Selenium (GeckoDriver/Firefox)
- **API Wrapper:** Spotipy
- **Algorithms:** Fuzzy String Matching (TheFuzz)
- **Environment Management:** Python-Dotenv

## 📁 Project Structure
```text
amazon-to-spotify/
├── .env                # Private API Keys (Hidden)
├── .gitignore          # Prevents leaking secrets to GitHub
├── README.md           # Documentation
├── requirements.txt    # Project Dependencies
├── amazon_scraper.py   # Phase 1: Data Extraction Logic
└── spotify_engine.py   # Phase 2: API Search & Playlist Injection

```

## 📋 Setup & Installation

1. **Clone the Repo**
```bash
git clone [https://github.com/YOUR_USERNAME/amazon-to-spotify.git](https://github.com/YOUR_USERNAME/amazon-to-spotify.git)
cd amazon-to-spotify

```


2. **Install Requirements**
```bash
pip install -r requirements.txt

```


3. **Configure Environment Variables**
Create a `.env` file and add your Spotify Developer credentials:
```env
SPOTIPY_CLIENT_ID='your_spotify_client_id'
SPOTIPY_CLIENT_SECRET='your_spotify_client_secret'
SPOTIPY_REDIRECT_URI='[http://127.0.0.1:8080](http://127.0.0.1:8080)'

```



## 🎮 Usage

### Step 1: Extract from Amazon

Run the scraper. Login when the browser opens and navigate to your playlist.

```bash
python amazon_scraper.py

```

*Outputs: `amazon_tracks.json*`

### Step 2: Sync to Spotify

Run the engine to find the matches and generate your new playlist.

```bash
python spotify_engine.py

```

## 📉 Lessons Learned

* **Handling Race Conditions:** Implemented `WebDriverWait` to manage asynchronous rendering in modern web apps.
* **Cross-Platform Discrepancies:** Developed fuzzy logic to bridge the gap between different streaming service metadata standards.
* **Security Best Practices:** Managed sensitive credentials using the loopback IP (`127.0.0.1`) for OAuth security.

---

**Maintained by Mantavya**

```
---
