import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


urls = [
    'https://gooshishop.com/category/mobile',
    #"https://gooshishop.com/gsp-12130/samsung-galaxy-a55-vietnam-256-8",
    #"https://gooshishop.com/gsp-9562/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D8%A2%DB%8C%D9%81%D9%88%D9%86-13-apple-iphone-13",
    #"https://gooshishop.com/gsp-11433/xiaomi-redmi-note-13-pro-plus-12gb-512gb",
    #"https://gooshishop.com/gsp-12166/xiaomi-redmi-a3-4g-128-4",
    #"https://gooshishop.com/gsp-11468/samsung-galaxy-s24-ultra-5g-12-256-vietnam",
    #"https://gooshishop.com/gsp-11129/samsung-galaxy-a15-4g-256-8-vietnam",
    #"https://tellstar.ir/product/apple-iphone-13-pro-256g-%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%A7%D9%BE%D9%84-%D8%A7%DB%8C%D9%81%D9%88%D9%86-13-%D9%BE%D8%B1%D9%88-256-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8",
    #"https://gooshishop.com/gsp-14039/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-%D8%AC%DB%8C-%D8%A7%D9%84-%D8%A7%DB%8C%DA%A9%D8%B3-classic-125",
    #"https://gooshishop.com/gsp-1915/%D8%AC%DB%8C-%D8%A7%D9%84-%D8%A7%DB%8C%DA%A9%D8%B3-%D8%AF%DB%8C-6-glx-d6",
    #"https://gooshishop.com/gsp-3400/%D8%AC%DB%8C%E2%80%8C-%D8%A7%D9%84%E2%80%8C-%D8%A7%DB%8C%DA%A9%D8%B3-%D8%A2%D8%B1%DB%8C%D8%A7-glx-arya"
]

def goshi_shop_product(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,"html.parser")
        product_name1= soup.find("h2", class_="pdp-title-en h4 m-h5 hint-text font-weight-normal")
        product_name = product_name1.text.strip() 
        product_price = soup.find('div', class_='prices').span.get_text(strip=True)
        return {"name" : product_name, "price" : product_price, "url" : url}
    else:
       return {"name" : None, "price" : None, "url" : url} 
    
with ThreadPoolExecutor() as ex:
    goshi_shop_products = list(ex.map(goshi_shop_product,urls))   

for product in goshi_shop_products:
    print(f"product name : {product['name']}")
    print(f"product price : {product['price']}")
    print(f"product url : {product['url']}")
    print("-"*60)


