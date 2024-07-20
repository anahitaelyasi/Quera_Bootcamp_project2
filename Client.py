import socket

phone_names = [
    "Samsung Galaxy S24 Ultra STANDARD EDITION DUAL SIM 512GB ROM + 12GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (Titanium Black)",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM+256GB Dual-SIM Unlocked Android Smartphone Supports Fastest 50W Wireless Charging",
    "Samsung Galaxy A34 EE DUAL SIM 128GB ROM + 6GB RAM (GSM Only | No CDMA) Factory Unlocked 5G Smartphone",
    "Xiaomi 14 Ultra DUAL SIM 512GB ROM + 16GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (White)",
    "Samsung - Galaxy A15 5G 128GB (Unlocked) - Blue Black",
    "Apple iPhone 14 Pro Max 256GB Fully Unlocked Purple - Grade B",
    "Samsung Galaxy A55",
    "iPhone 13 Pro Max 5G 128GB",
    "SAMSUNG Galaxy S24 Ultra Cell Phone 256GB AI Smartphone Unlocked Android 200MP 100x Zoom Cameras",
    "Apple iPhone 11 A13 Bionic 4GB, 64GB 6.1inch iOS A GRADE Red (Unlocked) Refurbished",
    "Apple iPhone 12 128GB GSM/CDMA Fully Unlocked - Blue",
    "Samsung Galaxy S22 Ultra 5G 128GB Fully Unlocked SM-S908 (2022) - Red - Good Condition"
]

phone_info = {}


def recieve_message(client_socket):
    while True:
        price = client_socket.recv(1024).decode('utf-8')
        if not price:
            break
        phone_info[phone_name] = {'Price': price}
    client_socket.close()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))

for phone_name in phone_names:
    client.send(phone_name.encode('utf-8'))

client.close() 