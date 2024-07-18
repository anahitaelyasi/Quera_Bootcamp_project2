import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of phone names
phone_names = [
    "Samsung Galaxy S24 Ultra STANDARD EDITION DUAL SIM 512GB ROM + 12GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (Titanium Black)",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM+256GB Dual-SIM Unlocked Android Smartphone Supports Fastest 50W Wireless Charging",
    "Samsung Galaxy A34 EE DUAL SIM 128GB ROM + 6GB RAM (GSM Only | No CDMA) Factory Unlocked 5G Smartphone",
    "Xiaomi 14 Ultra DUAL SIM 512GB ROM + 16GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (White)",
    "Samsung - Galaxy A15 5G 128GB (Unlocked) - Blue Black",
    "Apple iPhone 14 Pro Max 256GB Fully Unlocked Purple - Grade B",
    "Samsung Galaxy A55",
    "iPhone 13 Pro Max 5G 128GB", 
    "SAMSUNG Galaxy S24 Ultra Cell Phone 256GB AI Smartphone Unlocked Android 200MP 100x Zoom Cameras",
    "Apple iPhone 11 A13 Bionic 4GB, 64GB 6.1inch iOS A GRADE Red (Unlocked) Refurbished",
    "Apple iPhone 12 128GB GSM/CDMA Fully Unlocked - Blue",
    "Samsung Galaxy S22 Ultra 5G 128GB Fully Unlocked SM-S908 (2022) - Red - Good Condition"
]

# DataFrame
df = pd.DataFrame(phone_names, columns=["Phone names"])

# Function to scrape Newegg
def scrape_newegg(phone_name):
    url = f"https://www.newegg.com/p/pl?d={phone_name.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_link_tag = soup.find('a', class_='item-title')

    if product_link_tag:
        product_link = product_link_tag['href']
        response2 = requests.get(product_link)
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        price_tag = soup2.find('li', class_='price-current')

        if price_tag:
            return price_tag.text.strip()
    
    return 'N/A'

# Dictionary to hold phone information
phone_info = {}

# Using ThreadPoolExecutor for concurrent execution
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_phone = {executor.submit(scrape_newegg, phone_name): phone_name for phone_name in phone_names}
    for future in concurrent.futures.as_completed(future_to_phone):
        phone_name = future_to_phone[future]
        try:
            price = future.result()
        except Exception as exc:
            price = 'Error'
            print(f'{phone_name} generated an exception: {exc}')
        phone_info[phone_name] = {'Price': price} 

        df.loc[df['Phone names'] == phone_name, 'Price'] = price



print(df)
