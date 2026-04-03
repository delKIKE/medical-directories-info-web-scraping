# 🏥 Honduras Medical Directory Scraper

A web scraping project that collects doctor information from three major hospital directories in Honduras and saves the data into structured CSV files for further analysis.

---

## 📋 Project Overview

This project scrapes the public medical directories of the following hospitals:

- **Hospital y Clínicas Viera** (4 pages)
- **La Policlínica**
- **Honduras Medical Center (HMC)**

For each doctor, the following information is extracted:

- Full name
- Medical specialty
- Sub-specialty
- Location / floor
- Phone number
- Office hours / schedule

---

## 🛠️ Tools & Libraries

| Tool | Purpose |
|---|---|
| `requests` | Fetching HTML from standard websites |
| `BeautifulSoup` | Parsing and extracting data from HTML |
| `Selenium` | Rendering JavaScript-heavy pages (HMC) |
| `csv` | Saving extracted data to CSV files |
| `feedparser` | Initial response inspection |

---

## ⚙️ How It Works

### Hospital Viera & La Policlínica
These sites are standard server-rendered websites, meaning their HTML content is fully available when fetched with a simple `requests.get()` call. BeautifulSoup is used to navigate the HTML structure, locate doctor entries, and extract the relevant fields.

### Honduras Medical Center (HMC)
HMC presented a more complex challenge. The site is built as a **Single Page Application (SPA)** using JavaScript — meaning a regular HTTP request only returns an empty HTML shell with no doctor data. This required a two-step approach split across two files:

**Step 1 — `selenium_hmc.py` (run locally)**
A standalone Python script that:
1. Launches a real Chrome browser using Selenium
2. Navigates to `hmc.com.hn/directory` and waits 5 seconds for JavaScript to fully render the content
3. Saves the fully rendered HTML to a local file (`hmc_page.html`)

This script only needs to be run once to capture the page. The saved HTML file is then used as the input for the notebook.

**Step 2 — `medical_directories.ipynb` (the notebook)**
Reads the saved `hmc_page.html` file and uses BeautifulSoup to parse it and extract all doctor entries.

---

## 🧩 Challenges & How They Were Solved

### 1. SPA Rendering (HMC)
**Problem:** Standard `requests` and `feedparser` calls returned an empty `<div id="app"></div>` with no content.  
**Solution:** Switched to Selenium with headless Chrome to render the JavaScript before scraping. This required understanding the difference between server-rendered and client-rendered websites.

### 2. NoneType Errors
**Problem:** Some doctor entries were missing certain fields (e.g., no `<h4>` or `<p>` tag), causing `AttributeError: 'NoneType' object has no attribute 'get_text'`.  
**Solution:** Added `if element is not None` checks before calling `.get_text()`, making the scraper resilient to inconsistent HTML structures across entries.

### 3. Unwanted Text ("En Atención")
**Problem:** Some entries included a status label "En Atención" that was being captured as part of the doctor's data.  
**Solution:** Added a conditional filter to skip any field containing that phrase before writing to CSV.

### 4. CSV Formatting
**Problem:** Initial attempts used `writerows` instead of `writerow`, which caused each character to be written as a separate row.  
**Solution:** Restructured the loop to collect all fields into variables first, then write them as a single row using `writerow([name, specialty, floor, phone, schedule])`.

### 5. ResultSet vs Single Element
**Problem:** Calling `.find()` on a list returned by `find_all()` caused `AttributeError: ResultSet object has no attribute "find"`.  
**Solution:** Learned the distinction between iterating over a ResultSet and operating on a single Tag element — fixed by calling `.find()` on the loop variable (`div`) instead of the list (`entry_text`).

---

## 📁 Output

Each hospital's data is saved as a separate CSV file:

```
medical_directory.csv       ← HMC doctors
viera_directory.csv         ← Hospital Viera doctors
policlinica_directory.csv   ← La Policlínica doctors
```

---

## 🚀 How to Run

1. Clone the repository
2. Install dependencies:
```bash
pip install requests beautifulsoup4 selenium feedparser
```
3. For HMC, make sure Chrome is installed (Selenium Manager will handle the driver automatically)
4. Run the notebook `medical_directories.ipynb`

---

## 💡 Potential Extensions

- Merge all three CSVs into a unified Honduras medical database
- Analyze specialty distribution across hospitals
- Visualize doctor availability by day and time
- Build a searchable web interface on top of the data

---

## 👤 Author

Adan Ordonez
Drexel Data Science Master's Student  
Honduras, 2026
