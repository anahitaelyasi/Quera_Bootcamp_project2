import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


urls = [
    'https://ithome.ir/product/smartphone-samsung-galaxy-a35-5g-256-8-vn/'
    
]

def goshi_shop_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    product_name= soup.find("h1").text.strip()
    product_price = soup.find('span', class_='amount').text.strip()
    return {"name" : product_name, "price" : product_price, "url" : url}
    
    
with ThreadPoolExecutor() as ex:
    goshi_shop_products = list(ex.map(goshi_shop_product,urls))   

for product in goshi_shop_products:
    print(f"product name : {product['name']}")
    print(f"product price : {product['price']}")
    print(f"product url : {product['url']}")
    print("-"*60)


