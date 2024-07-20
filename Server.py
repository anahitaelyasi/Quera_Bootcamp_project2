import socket
import threading

import requests
from bs4 import BeautifulSoup


def scrape_newegg(conn):
    while True: 
        phone_name = client_socket.recv(1024).decode('utf-8')
        if not phone_name:
            break
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
                message = price_tag.text.strip()
                client_socket.send(message.encode('utf-8'))

        return 'N/A'
    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen()
print("Server is listening to 9080")

while True:
    client_socket, client_address = server.accept()
    print("Connected by", client_address)
    thread = threading.Thread(target=scrape_newegg,args=(client_socket,))
    thread.start()

server.close()