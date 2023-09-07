import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Read the CSV file with URLs
csv_url = "https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URT" \
          "xTJrIRkD7PnGTM/export?format=csv"
df = pd.read_csv(csv_url)

# Initialize Selenium WebDriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
chrome_options.add_argument("--no-sandbox")  # Add this option for Linux environments
chrome_driver_path = ChromeDriverManager().install()  # Use WebDriver Manager to get ChromeDriver path

# Function to check if a URL returns a 404 error
def is_url_valid(url):
    try:
        driver = webdriver.Chrome(options=chrome_options)  # Create WebDriver instance
        driver.get(url)
        return not "404 - Not Found" in driver.title
    except Exception as e:
        print(f"Error checking {url}: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()  # Close the WebDriver after checking

# Function to scrape data from a single URL
def scrape_product_info(url):
    try:
        driver = webdriver.Chrome(options=chrome_options)  # Create WebDriver instance
        driver.get(url)
        time.sleep(2)  # Wait for page to load (you may need to adjust this)
        
        # Check if the URL is valid (not 404 error)
        if "404 - Not Found" in driver.title:
            print(f"{url} not available (404 Error)")
            return None
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract the product details
        product_title_element = soup.find("span", {"id": "productTitle"})
        product_image_element = soup.find("img", {"id": "landingImage"})
        product_price_element = soup.find("span", {"class": ["a-price-whole","a-price-symbol"]})
        product_details_element = soup.find("div", {"id": "productDescription"})
        
        # Initialize variables to store data
        product_title = "Not Found"
        product_image_url = "Not Found"
        product_price = "Not Found"
        product_details = "Not Found"
        
        # Check if the elements exist before calling get_text()
        if product_title_element:
            product_title = product_title_element.get_text().strip()
        
        if product_image_element:
            product_image_url = product_image_element["src"]
        
        if product_price_element:
            product_price = product_price_element.get_text().strip()
        
        if product_details_element:
            product_details = product_details_element.get_text().strip()
        
        # Check if all relevant data fields are "Not Found"
        if (
            product_title == "Not Found" and
            product_image_url == "Not Found" and
            product_price == "Not Found" and
            product_details == "Not Found"
        ):
            print(f"No data found for {url}, skipping...")
            return None
        
        product_info = {
            "Product Title": product_title,
            "Product Image URL": product_image_url,
            "Price of the Product": product_price,
            "Product Details": product_details,
        }
        
        return product_info
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()  # Close the WebDriver after each URL

# Initialize a list to store the scraped data
scraped_data = []

# Track the number of URLs processed
urls_processed = 0

# Track the start time for processing 100 URLs
start_time = time.time()

# Loop through the first 100 URLs and scrape data
for index, row in df.head(100).iterrows():
    country = row['country']
    asin = row['Asin']
    url = f"https://www.amazon.{country}/dp/{asin}"
    
    # Check if the URL is valid (not 404 error)
    if is_url_valid(url):
        product_info = scrape_product_info(url)
        if product_info:
            scraped_data.append(product_info)
    
    # Increment the count of processed URLs
    urls_processed += 1
    
    # Check if 100 URLs have been processed
    if urls_processed % 100 == 0:
        # Calculate the time taken for processing 100 URLs
        elapsed_time = time.time() - start_time
        print(f"Time taken for processing 100 URLs: {elapsed_time:.2f} seconds")
        start_time = time.time()  # Reset the start time

# Save the scraped data as a JSON file
with open("scraped_data.json", "w") as json_file:
    json.dump(scraped_data, json_file, indent=4)

print("Scraping completed for the first 100 URLs.")
