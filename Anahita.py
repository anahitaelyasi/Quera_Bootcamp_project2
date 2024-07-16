from bs4 import BeautifulSoup
import requests
import pandas 
import re

common_urls = ["https://tellstar.ir/product/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84--%D9%85%D8%AF%D9%84-Galaxy-A55-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-|-5G" ,
        "https://tellstar.ir/product/samsung-galaxy-s24-ultra-256-12-5g-%DA%AF%D9%88%D8%B4%DB%8C-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%DA%AF%D9%84%DA%A9%D8%B3%DB%8C-%D8%A7%D8%B3-24-%D8%A7%D9%88%D9%84%D8%AA%D8%B1%D8%A7-256-12-5" ,
        "https://tellstar.ir/product/samsung-galaxy-a15-5g-256-8-gb-%DA%AF%D9%88%D8%B4%DB%8C-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%DA%AF-%DA%AF%D9%84%DA%A9%D8%B3%DB%8C-%D8%A215-256-8-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA" ,
        "https://tellstar.ir/product/xiaomi-note-13-pro-5g-512-12-%DA%AF%D9%88%D8%B4%DB%8C-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C-%D9%86%D9%88%D8%AA-13-%D9%BE%D8%B1%D9%88-%D8%AD%D8%A7%D9%81%D8%B8%D9%87-512-%D8%B1%D9%85-12-%DA%AF",
        "https://tellstar.ir/product/128-4-Xiaomi-Redmi-A3_-%D8%B4%DB%8C%D8%A7%D8%A6%D9%88%D9%85%DB%8C--%D8%B1%D8%AF%D9%85%DB%8C-%D8%A2-%D8%B3%D9%87--128-%D8%B1%D8%A7%D9%85-4",
        "https://tellstar.ir/product/Apple-iPhone-13-(Not-Active)-128-4GB---%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D8%A7%DB%8C%D9%81%D9%88%D9%86-13%D8%AD%D8%A7%D9%81%D8%B8%D9%87--128-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA-%D8%B1%D9%85-4-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA--%D9%86%D8%A7%D8%AA-%D8%A7%DA%A9%D8%AA%DB%8C%D9%88-"
        ] 

phone_data = [] 

def scrape_tellstar(url) : 
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    pattern = re.compile(r'([A-Za-z0-9\s]+[A-Za-z0-9\s\/]*)') 
    phone_name = soup.find_all('h5',class_="font-16")[0].text.replace(' ','') 
    phone_price = soup.find_all('span',{"id":"product_off_price" , "class" : "main-color-one-color"})[0].text.replace(' ','') 
    find_phone_name = pattern.findall(phone_name)[0]
    phone_data.append(find_phone_name)
    phone_data.append(phone_price)
    #phone_name['Name'] = find_phone_name
    #phone_data['Price'] = phone_price 



for url in common_urls :
    phone_info = scrape_tellstar(url) 

print(phone_data) 
