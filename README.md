# Ethical Web Scraper

## Description
This is an advanced web scraper built with Python, using **Tkinter** for the graphical user interface (GUI) and **BeautifulSoup** for HTML parsing. The application allows users to scrape web pages, extract various data types, and view the results in an organized format.

## Features
- **Scrape Web Pages:** Input a URL to scrape content such as metadata, headings, links, images, forms, and text content.
- **View Scraped Data:** Display results in a scrollable text area with sections for metadata, headings, links, images, and more.
- **Statistics:** View summarized statistics, including counts for headings, links, images, and forms.
- **Save Results:** Automatically saves the scraped data to a JSON file for later use.
- **Multithreading:** Non-blocking scraping to keep the GUI responsive.

## Requirements
- Python 3.7+
- Libraries: 
  - `urllib`
  - `BeautifulSoup` (from `bs4`)
  - `tkinter`
  - `json`
  - `threading`
  - `re`

Install BeautifulSoup using:
```bash
pip install beautifulsoup4
```

## How to Run
1. Clone or download the project.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Run the application:
   ```bash
   python web_scraper_gui.py
   ```
4. Enter the URL in the text box and click **Scrape**.

## Usage
- **Scrape Button:** Start scraping the entered URL.
- **Clear Button:** Clear the results and statistics.
- **Status Bar:** Displays the current status (e.g., scraping, errors, or completion).

## Output
- Scraped data is displayed in the GUI.
- A JSON file containing the scraped data is saved in the project directory.

## JSON Output Format
```json
{
    "meta": {
        "title": "Page Title",
        "meta_description": "Description of the page",
        "meta_keywords": "Keywords for the page"
    },
    "headings": [
        {"level": "h1", "text": "Heading text", "id": "", "classes": []}
    ],
    "links": [
        {"text": "Link text", "url": "https://example.com"}
    ],
    "images": [
        {"src": "https://example.com/image.jpg", "alt": "Image description"}
    ],
    "forms": [
        {"action": "/submit", "method": "post", "fields": []}
    ]
}
```
