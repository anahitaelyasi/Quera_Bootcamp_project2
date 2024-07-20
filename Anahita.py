import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of phone names
phone_names = [
    "Samsung Galaxy A15 5G 128GB Blue Black",
    "Apple iPhone 14 Pro Max 256GB Purple",
    "Samsung Galaxy A55",
    "Samsung Galaxy S24 Ultra 512GB 12GB RAM Titanium Black", 
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM 256GB", 
    "Samsung Galaxy A34 Dual SIM 6GB RAM 128GB Storage",
    "Xiaomi 14 Ultra Dual SIM 5G 512GB 16GB 5G White",

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
        #product_storage = 
    
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
