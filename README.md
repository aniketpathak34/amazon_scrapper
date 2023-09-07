---

# Amazon Product Scraper

This Python script allows you to scrape product information from Amazon URLs provided in a CSV file. It uses Selenium and Beautiful Soup to extract details such as product title, image URL, price, and product description from each URL.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Output](#output)
- [Performance](#performance)
- [Contributing](#contributing)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your machine.
- Required Python libraries installed. You can install them using `pip`:

```bash
pip install pandas selenium beautifulsoup4 webdriver-manager
```

- Chrome web browser installed. You can also use other browsers supported by Selenium.

## Getting Started

To get started, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/amazon-product-scraper.git
```

2. Change to the project directory:

```bash
cd amazon-product-scraper
```

3. Install the required Python libraries (if you haven't already):

```bash
pip install pandas selenium beautifulsoup4 webdriver-manager
```

4. Download and install ChromeDriver. The script uses WebDriver Manager to automatically download ChromeDriver. If you want to use a specific version or have Chrome installed in a custom location, you can modify the `chrome_driver_path` variable in the script accordingly.

## Usage

1. Prepare your CSV file with a list of Amazon URLs to scrape. The CSV file should have the following columns: `id`, `Asin`, `country`. For example:

```csv
id,Asin,country
1,B01234567,com
2,B09876543,co.uk
3,B98765432,de
...
```

2. Update the `csv_url` variable in the script to point to your CSV file.

3. Run the script:

```bash
python amazon_scraper.py
```

The script will start scraping product information from the URLs in the CSV file. Progress and errors will be displayed in the console.

## Output

The scraped product information will be saved as a JSON file named `scraped_data.json` in the project directory. Each product's details will be stored in a dictionary format, including:

- Product Title
- Product Image URL
- Price of the Product
- Product Details

## Performance

The script tracks the time taken to process each batch of 100 URLs. After processing each batch, it reports the time taken to the console. You can monitor the progress and performance of the scraping process.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create a GitHub issue or submit a pull request.


---
