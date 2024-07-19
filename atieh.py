import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re
import concurrent.futures

phone_names = [
    "Samsung Galaxy A15 5G Dual SIM, 4GB RAM, 128GB Storage, Blue Black (UAE Version)",
    "Apple iPhone 14 Pro Max, 6.7 Super Retina XDR Display, A16 Bionic Chip, 6GB RAM, 256GB Storage, Physical Sim & e-Sim, 5G Network, Face ID, 48+12+12 MP Camera, Japan Version, Purple | JP14MX256P",
    "Samsung Galaxy A55",
    "Samsung Galaxy S24 Ultra, 512GB, Black, 12GB RAM, Android Smartphone, 200MP Camera, (International Version)",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera",
    "OnePlus 12 5G Dual Sim Mobile Phone, 6.8 QHD+ ProXDR 120Hz Display, 12GB RAM, 256GB Storage, Snapdragon 8 Gen 3 Chipset, 50mp+64mp+48mp Main Camera, 32mp Selfie Camera, Silky Black | OP1212R256S",
    "Samsung Galaxy A34 Dual SIM Smartphone, 6.6 Super AMOLED Display, 6GB RAM, 128GB Storage, LTE 4G / 5G, 48 MP /13 MP Camera, 5000mAh Battery, UAE Version, Awesome Lime",
    "Xiaomi 14 Ultra Dual SIM 5G 512GB 16GB 5G White - Chines Version",
    "Samsung Galaxy A15 5G Dual SIM, 4GB RAM, 128GB Storage, Blue Black (UAE Version)",
    "Apple iPhone 15 Pro Max",
    "HUAWEI nova 10 Dual Sim Smartphone, 6.67 Curved OLED Display, 8GB RAM 256 GB Storage, LTE 4G, 60 MP Front Ultra Wide Camera",
    "HUAWEI nova 11i SmartPhone",
    "vivo V30 5G (Noble Black, 12GB+12GB RAM, 512GB)",
    "Samsung Galaxy Z Flip6 AI Smartphone",
    "HUAWEI nova 10 Pro Dual SIM Smartphone, 6.7 120 Hz Curved Display, Star Orbit Ring Design, 8GB RAM, 256GB Storage, 4G LTE Network, 60 MP/50MP Camera, 4500 mAh Battery, Starry Black | 51097EWH"
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
        df.loc[df['Phone names'] == phone_name, 'Price'] = price    
print(df)  
 