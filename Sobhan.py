import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Step 1 -- > Create a database
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


# Define phone lists
common_phones = [
    "Samsung Galaxy A15 5G 128GB Blue Black",
    "Apple iPhone 14 Pro Max 256GB Purple",
    "Samsung Galaxy A55",
    "Samsung Galaxy S24 Ultra 512GB 12GB RAM Titanium Black",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM 256GB",
    "Samsung Galaxy A34 Dual SIM 6GB RAM 128GB Storage",
    "Xiaomi 14 Ultra Dual SIM 5G 512GB 16GB 5G White"
]
only_microless = [
    "Apple iPhone 15 Pro Max, 6.7 OLED Super Retina XDR Display A17 Pro Chip  256GB Storage Bluetooth 5.3 Face ID TRA Version Natural Titanium",
    "HUAWEI nova 10 Dual Sim Smartphone, 6.67 Curved OLED Display, 8GB RAM 256 GB Storage, LTE 4G, 60 MP Front Ultra Wide Camera",
    "HUAWEI nova 11i SmartPhone 8GB 128GB Starry Black",
    "vivo V30 5G Noble Black 12GB 12GB RAM 512GB",
    "Samsung Galaxy Z Flip6 AI Smartphone 12GB RAM 512GB Storage Silver Shadow"
]
only_newegg = [
    "Apple iPhone 13 Pro Max, 128GB, Graphite - Unlocked",
    "SAMSUNG Galaxy S24 Ultra Cell Phone 256GB AI Smartphone Unlocked Android 200MP 100x Zoom Cameras",
    "Apple iPhone 11 A13 Bionic 4GB, 64GB 6.1inch iOS A GRADE Red (Unlocked) Refurbished",
    "Apple iPhone 12 128GB GSM/CDMA Fully Unlocked - Blue",
    "Samsung Galaxy S22 Ultra 5G 128GB Fully Unlocked SM-S908 (2022) - Red - Good Condition"
]
new_products = [
    "Original LG Smart Folder 4G LTE Mobile Phone Unlocked LG X100 3.3'' 2GB RAM 16GB ROM 4.9MP Camera FM Radio Android SmartPhone",
    "HTC Status ChaCha A810a Unlocked Phone with QWERTY Keyboard, 5MP Camera, Wi-Fi and GPS - US Warranty - Silver",
    "Sony Ericsson Xperia X10 Mini E10i",
    "ASUS Phone ZA550KL-S425-1G16G-BK Zenfone Live L1 5.45 1GB 16GB Black Retail"
]


# Combine all phones into one list
phone_names = common_phones + only_newegg + only_microless + new_products

# DataFrame
df = pd.DataFrame(phone_names, columns=["Phone names"])
df["Newegg Price"] = "0"
df["Microless Price"] = "0"


# Step 2 -- > Define functions to scrape the websites
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


# Scraping newegg.com
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

#Scraping microless.com
def scrape_microless(phone_name):
    url = f"https://global.microless.com/search/?query={phone_name.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_link_tag = soup.find('div', class_='product-title').find('a')

    if product_link_tag:
        product_link = product_link_tag['href']
        response2 = requests.get(product_link)
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        price_tag = soup2.find('div', class_='product-main-price')

        if price_tag:
            return price_tag.text.strip()

    return 'N/A'

# Function to handle scraping based on phone list categories
def scrape_phone_data(phone_name):
    newegg_price = scrape_newegg(phone_name)
    microless_price = scrape_microless(phone_name)
    return phone_name, newegg_price, microless_price

# Concurrent execution for scraping
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_phone = {executor.submit(scrape_phone_data, phone_name): phone_name for phone_name in phone_names}
    for future in concurrent.futures.as_completed(future_to_phone):
        phone_name, newegg_price, microless_price = future.result()
        df.loc[df['Phone names'] == phone_name, 'Newegg Price'] = newegg_price
        df.loc[df['Phone names'] == phone_name, 'Microless Price'] = microless_price


# Cleaning price columns and converting to numeric
df['Newegg Price'] = pd.to_numeric(df['Newegg Price'].str.replace('[$,]', '', regex=True), errors='coerce')
df['Microless Price'] = pd.to_numeric(df['Microless Price'].str.replace('[$,]', '', regex=True), errors='coerce')


# Step 3 -- > Calculate the price range of the products
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


#new_df = pd.DataFrame(new_products)
#df = pd.concat([df,new_df],ignore_index=True)
for i, row in df.iterrows():
    if pd.isna(row['Newegg Price']) and pd.isna(row['Microless Price']):
        df.at[i, 'Min price'] = '_'
    elif pd.notna(row['Newegg Price']) and pd.isna(row['Microless Price']):
        df.at[i, 'Min price'] = row['Newegg Price']
    elif pd.isna(row['Newegg Price']) and pd.notna(row['Microless Price']):
        df.at[i, 'Min price'] = row['Microless Price']
    else:
        df.at[i, 'Min price'] = min(row['Newegg Price'], row['Microless Price'])

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
