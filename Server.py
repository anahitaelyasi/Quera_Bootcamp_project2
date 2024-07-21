import socket
import threading
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures


# -------------------------------------------------------
# -------------------------------------------------------

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


def scrape_phone_data(phone_name):
    newegg_price = scrape_newegg(phone_name)
    microless_price = scrape_microless(phone_name)
    return phone_name, newegg_price, microless_price


# -------------------------------------------------------
# -------------------------------------------------------

def calculate_cp(min_price):
    if min_price == '_':
        return 1000
    else:
        return min_price * 0.55


def calculate_base_price(cp):
    return cp + 15


def sell_price(cp):
    return (cp + 15) * 1.1


def is_competitive(row):
    if row['Min price(Shops)'] == '_':
        return 'No'
    return 'Yes' if row['cp(min)'] <= row['sell price'] <= row['Min price(Shops)'] else 'No'


# -------------------------------------------------------
# -------------------------------------------------------

def handle_client(client_socket):
    request = client_socket.recv(8080)
    phone_names = json.loads(request.decode('utf-8'))
    df = pd.DataFrame(phone_names, columns=["Phone names"])
    df["Newegg Price"] = "0"
    df["Microless Price"] = "0"
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_phone = {executor.submit(scrape_phone_data, phone_name): phone_name for phone_name in phone_names}
        for future in concurrent.futures.as_completed(future_to_phone):
            phone_name, newegg_price, microless_price = future.result()
            df.loc[df['Phone names'] == phone_name, 'Newegg Price'] = newegg_price
            df.loc[df['Phone names'] == phone_name, 'Microless Price'] = microless_price
    df['Newegg Price'] = pd.to_numeric(df['Newegg Price'].str.replace('[$,]', '', regex=True), errors='coerce')
    df['Microless Price'] = pd.to_numeric(df['Microless Price'].str.replace('[$,]', '', regex=True), errors='coerce')
    for i, row in df.iterrows():
        if pd.isna(row['Newegg Price']) and pd.isna(row['Microless Price']):
            df.at[i, 'Min price(Shops)'] = '_'
        elif pd.notna(row['Newegg Price']) and pd.isna(row['Microless Price']):
            df.at[i, 'Min price(Shops)'] = row['Newegg Price']
        elif pd.isna(row['Newegg Price']) and pd.notna(row['Microless Price']):
            df.at[i, 'Min price(Shops)'] = row['Microless Price']
        else:
            df.at[i, 'Min price(Shops)'] = min(row['Newegg Price'], row['Microless Price'])
    df['cp(min)'] = df['Min price(Shops)'].apply(lambda x: calculate_cp(x) if x != '_' else 1000)
    df['base price'] = df['cp(min)'].apply(calculate_base_price)
    df['sell price'] = df['base price'].apply(sell_price)
    df['competitive'] = df.apply(is_competitive, axis=1)
    result = df.to_json(orient='records')
    client_socket.sendall(result.encode('utf-8'))
    client_socket.close()


# -------------------------------------------------------
# -------------------------------------------------------

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)
print("Server listening on port 8080")
while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
