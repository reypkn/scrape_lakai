import os
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Base URLs to scrape
BASE_URLS = {
    "shoes": "https://www.lakai.com/collections/shoes",
    "apparel": "https://www.lakai.com/collections/apparel"
}

# Headers for the HTTP request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Directory to save downloaded images
IMAGE_DIR = "product_images"

def fetch_html(url):
    """Fetch the HTML content of the given URL."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch {url}")
        return None

def parse_products(html, category):
    """Parse product data from the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    # Adjust selectors based on the website's HTML structure
    product_elements = soup.select('a.flex.flex-col.gap-2')  # Access product links
    for product in product_elements:
        try:
            # Extract product link
            product_link = product['href']
            product_url = urljoin(BASE_URLS[category], product_link)
            product_html = fetch_html(product_url)
            product_soup = BeautifulSoup(product_html, 'html.parser')

            product_unique_name = product_url.split("/products/")[1].split("?variantId=null")[0]
            
            # Extract name and price
            name_price_div = product_soup.find('div', id='name-price')
            name = name_price_div.find_all('h1')[0].get_text(strip=True)
            price = name_price_div.find_all('h1')[1].get_text(strip=True)
            
            # Extract color
            selected_variant_div = product_soup.find('div', id='selected-variant')
            color = selected_variant_div.find_all('span')[1].get_text(strip=True)
            
            # Extract image URLs
            image_gallery_div = product_soup.find('div', id='desktop-image-gallery')
            image_elements = image_gallery_div.find_all('img', class_='w-full object-fit')
            image_urls = [urljoin(BASE_URLS[category], img['src']) for img in image_elements]

            # Extract description
            description_div = product_soup.find('div', id='accordion_piece_yqU6pQ_content')
            description_paragraphs = description_div.find_all('p')
            description = " ".join(p.get_text(strip=True) for p in description_paragraphs)

            products.append({
                'Category': category,
                'Name': name,
                'Color': color,
                'Price': price,
                'Image URLs': ", ".join(image_urls),
                'Description': description,
                'Product URL': product_url,
                'Unique Name': product_unique_name
            })
        except Exception as e:
            print(f"Error parsing product: {e}")
    
    return products

def save_to_csv(products, filename):
    """Save the product data to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Category', 'Name', 'Color', 'Price', 'Image URLs', 'Description', 'Product URL', 'Unique Name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

def download_images_from_csv(csv_file):
    """Download images for products listed in the CSV file."""
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row['Category']
            product_unique_name = row['Unique Name']
            image_urls = row['Image URLs'].split(", ")
            
            category_dir = os.path.join(IMAGE_DIR, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)

            for idx, image_url in enumerate(image_urls):
                try:
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        image_filename = f"{product_unique_name}_{idx + 1}.jpg"
                        image_filepath = os.path.join(category_dir, image_filename)
                        with open(image_filepath, 'wb') as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        print(f"Downloaded: {image_filepath}")
                except Exception as e:
                    print(f"Error downloading {image_url}: {e}")

def main():
    print("Starting scraper...")
    all_products = []
    for category, url in BASE_URLS.items():
        print(f"Scraping category: {category}")
        html = fetch_html(url)
        if html:
            products = parse_products(html, category)
            all_products.extend(products)
        else:
            print(f"Failed to retrieve content for {category}")
    
    if all_products:
        csv_filename = 'products.csv'
        save_to_csv(all_products, csv_filename)
        print(f"Scraped {len(all_products)} products. Data saved to {csv_filename}")
        
        # Download images after CSV is created
        download_images_from_csv(csv_filename)
    else:
        print("No products found.")

if __name__ == "__main__":
    main()