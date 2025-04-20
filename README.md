# Lakai Product Scraper

## Overview
This repository contains a Python-based web scraper designed to fetch product data from the Lakai website. The scraper collects information about shoes and apparel, including product names, prices, colors, descriptions, image URLs, and downloads product images from the website. The collected data is saved into a CSV file for further usage.

## Features
- **Scrape Product Data**: Extracts product details such as:
  - Product Name
  - Price
  - Color
  - Description
  - Image URLs
  - Product Page URL
- **Image Download**: Automatically downloads product images and organizes them into category-specific folders.
- **CSV Export**: Saves all the scraped product details into a CSV file for easy data analysis and use.
- **Category Support**: Currently supports scraping data from:
  - Shoes
  - Apparel

## How It Works
1. The scraper fetches product listings from the Lakai website.
2. It navigates to individual product pages using the links provided on the category pages.
3. Extracts relevant product details using BeautifulSoup and stores them in a structured format.
4. Downloads images after saving the product data into a CSV file.

## Requirements
- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`

Install the required libraries using:
```bash
pip install requests beautifulsoup4
```

## Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/reypkn/scrape_lakai.git
   cd scrape_lakai
   ```
2. Run the scraper:
   ```bash
   python scrape_lakai_products.py
   ```
3. Output:
   - A `products.csv` file containing all scraped product data.
   - Images downloaded into the `product_images` directory, organized by category.

## File Structure
- `scrape_lakai_products.py`: Main script for scraping product data and downloading images.
- `product_images/`: Directory where all downloaded images are stored.
- `products.csv`: CSV file containing the scraped product data.

## Configuration
The script is currently configured to scrape the following categories:
- Shoes: `https://www.lakai.com/collections/shoes`
- Apparel: `https://www.lakai.com/collections/apparel`

To add or modify categories, update the `BASE_URLS` dictionary in the script:
```python
BASE_URLS = {
    "shoes": "https://www.lakai.com/collections/shoes",
    "apparel": "https://www.lakai.com/collections/apparel"
}
```

## Future Enhancements
- Implement a scheduler to automate scraping at regular intervals.
- Improve error handling and logging.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements or suggestions.

## License
This project is licensed under NONE.

## Disclaimer
This scraper is intended for educational and personal use only. Ensure you comply with the website's terms of service and legal guidelines before using this scraper.

---
Happy scraping!
