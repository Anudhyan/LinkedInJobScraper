import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Path to ChromeDriver (from environment variable)
CHROME_DIR = os.getenv("CHROME_DRIVER_PATH", "chromedriver")  # default to 'chromedriver' if not set

def get_ready_driver(user_agent):
    """Set up and return a configured WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(executable_path=CHROME_DIR)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Disable detection of WebDriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    driver.implicitly_wait(10)
    return driver

def convert_relative_date(date_str):
    """Convert relative date string to YYYY-MM-DD format."""
    today = datetime.now()
    try:
        if "week" in date_str:
            weeks_ago = int(re.search(r'\d+', date_str).group())
            post_date = today - relativedelta(weeks=weeks_ago)
        elif "month" in date_str:
            months_ago = int(re.search(r'\d+', date_str).group())
            post_date = today - relativedelta(months=months_ago)
        elif "day" in date_str:
            days_ago = int(re.search(r'\d+', date_str).group())
            post_date = today - timedelta(days=days_ago)
        elif "hour" in date_str:
            hours_ago = int(re.search(r'\d+', date_str).group())
            post_date = today - timedelta(hours=hours_ago)
        elif "minute" in date_str:
            minutes_ago = int(re.search(r'\d+', date_str).group())
            post_date = today - timedelta(minutes=minutes_ago)
        else:
            post_date = today
    except Exception:
        post_date = today

    return post_date.strftime("%Y-%m-%d")

def extract_job_listings(driver):
    """Extract job listings from LinkedIn search results."""
    # Wait until jobs section loads
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/section[2]/ul')))
    print("Jobs section loaded.")

    jobs_section = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/ul')
    job_elements = jobs_section.find_elements(By.XPATH, './/li')
    print(f"Found {len(job_elements)} job elements.")

    job_list = []

    for job_element in job_elements:
        try:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", job_element)
            time.sleep(1)
            driver.execute_script("arguments[0].style.border='3px solid red'", job_element)
            time.sleep(1)

            job_title = job_element.find_element(By.CLASS_NAME, 'sr-only').text
            company_name = job_element.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle').text
            location = job_element.find_element(By.CSS_SELECTOR, 'span.job-search-card__location').text
            job_link = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            date_posted = job_element.find_element(By.CSS_SELECTOR, 'time.job-search-card__listdate').text
            date_posted = convert_relative_date(date_posted)

            job_details = {
                "Job Title": job_title,
                "Company Name": company_name,
                "Location": location,
                "Job Link": job_link,
                "Date Posted": date_posted
            }

            job_list.append(job_details)
            print(f"Extracted job: {job_details}")

        except Exception as e:
            print(f"Error extracting job details: {e}")
            continue

    return job_list

def sort_and_save_jobs(job_list, output_file):
    """Sort job listings by date posted in descending order and save to CSV."""
    sorted_job_list = sorted(job_list, key=lambda x: pd.to_datetime(x['Date Posted']), reverse=True)
    df = pd.DataFrame(sorted_job_list)
    df.to_csv(output_file, index=False)
    print(f"Job details saved to '{output_file}'.")

def main():
    """Main function to start the job scraping process."""
    driver = None
    try:
        user_agent = UserAgent(browsers=['edge', 'chrome', 'firefox']).random
        print(f"Using User Agent: {user_agent}")

        driver = get_ready_driver(user_agent)

        base_url = "https://www.linkedin.com/jobs/search"
        job_title = "Software"
        location = "Kolkata"
        search_url = f"{base_url}?keywords={job_title}&location={location}"
        print(f"Navigating to URL: {search_url}")

        driver.get(search_url)

        job_list = extract_job_listings(driver)
        print(f"Extracted {len(job_list)} jobs.")

        sort_and_save_jobs(job_list, 'linkedin_jobs_sorted.csv')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
