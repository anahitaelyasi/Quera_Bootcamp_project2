import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re
import concurrent.futures

phone_names = [
    "Samsung - Galaxy A15 5G 128GB (Unlocked) - Blue Black",
    "Apple iPhone 14 Pro Max 256GB Fully Unlocked Purple - Grade B",
    "Samsung Galaxy A55",
    "Samsung Galaxy S24 Ultra STANDARD EDITION DUAL SIM 512GB ROM + 12GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (Titanium Black)",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM+256GB Dual-SIM Unlocked Android Smartphone Supports Fastest 50W Wireless Charging",
    "Samsung Galaxy A34 EE DUAL SIM 128GB ROM + 6GB RAM (GSM Only | No CDMA) Factory Unlocked 5G Smartphone",
    "Xiaomi 14 Ultra DUAL SIM 512GB ROM + 16GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (White)",
    "Samsung - Galaxy A15 5G 128GB (Unlocked) - Blue Black",
    "Apple iPhone 14 Pro Max 256GB Fully Unlocked Purple - Grade B",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "HUAWEI nova 10 Dual Sim Smartphone, 6.67 Curved OLED Display, 8GB RAM 256 GB Storage, LTE 4G, 60 MP Front Ultra Wide Camera, "
    "HUAWEI nova 11i SmartPhone, 6.8 FullView Display, 94.9 Screen-to-Body Ratio, 8GB+128GB, 40W SuperCharge, 5000 mAh Battery"
    "vivo V30 5G (Noble Black, 12GB+12GB RAM, 512GB)"
    "Samsung Galaxy Z Flip6 AI Smartphone, 6.7 FHD+ AMOLED 2X Display, Octa-Core CPU, 12GB RAM, 512GB Storage, 50MP Camera, Dual-SIM - 5G Network"
]

df = pd.DataFrame(phone_names, columns=["Phone names"])
def global_microless(phone_name):
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
phone_info = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_phone = {executor.submit(global_microless, phone_name): phone_name for phone_name in phone_names}
    for future in concurrent.futures.as_completed(future_to_phone):
        phone_name = future_to_phone[future]
        try:
            price = future.result()
        except Exception as exc:
            price = 'Error'
            print(f'{phone_name} generated an exception: {exc}')
        phone_info[phone_name] = {'Price': price}
    
    
print(phone_info)   