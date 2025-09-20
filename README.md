# LinkedIn Job Scraper

A Python-based LinkedIn Job Scraper using Selenium to extract job listings for a given keyword and location.  
The scraper collects the following details for each job:

- **Job Title**  
- **Company Name**  
- **Location**  
- **Job Link**  
- **Date Posted**  

The extracted data is saved into a CSV file (`linkedin_jobs_sorted.csv`) sorted by the most recent postings.

---

## Features

- Automated job search on LinkedIn based on keyword and location  
- Handles relative date strings like "1 week ago" or "3 days ago"  
- Sorts extracted jobs by date and saves them into a CSV file  
- Uses random user agents to reduce detection risk  

---

## Prerequisites

- Python 3.8 or higher  
- Chrome Browser  
- ChromeDriver matching your Chrome version  

---

## Installation

1. Clone the repository:pip install -r requirements.txt


```bash
git clone https://github.com/Anudhyan/LinkedInJobScraper.git
cd LinkedInJobScraper
```
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Update the ChromeDriver path in scraper.py

```bash
CHROME_DIR = r"C:\path\to\chromedriver.exe"
```

Usage

Run the scraper:
```bash
python scraper.py
```

## Disclaimer

This project is intended for educational and personal learning purposes only.
Do not use this script to violate LinkedIn's Terms of Service or any applicable laws.

LinkedIn may block accounts or IP addresses that perform automated scraping

The author of this repository is not responsible for any misuse of this code

Always respect websites’ terms, privacy policies, and robot exclusion standards (robots.txt)

By using this code, you agree to use it responsibly and ethically.
