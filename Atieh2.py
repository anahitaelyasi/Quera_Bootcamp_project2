import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of phone names
phone_names = ["Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
               "SAMSUNG Galaxy S24 Ultra"
               ]

# DataFrame
df = pd.DataFrame(phone_names, columns=["Phone names"])

# Function to scrape Newegg
def scrape_newegg(phone_name):
    url = f"https://global.microless.com/search/?query={phone_name.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser') 
    product_link_tag = soup.find('div', class_='product-title').find('a') 

    if product_link_tag:
        product_link = product_link_tag['href'] 
        response2 = requests.get(product_link)
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        price_tag = soup2.find('div', class_='product-main-price') 

        return price_tag.text.strip()


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


print(phone_info)
