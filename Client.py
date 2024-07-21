import socket
import json
import pandas as pd


# -------------------------------------------------------
# -------------------------------------------------------

def receive_all(sock):
    buffer_size = 4096
    data = b''
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data


def request_data_from_server(phone_names):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    request = json.dumps(phone_names)
    client.send(request.encode('utf-8'))
    response = receive_all(client)
    data = json.loads(response.decode('utf-8'))
    df = pd.DataFrame(data)
    return df


# -------------------------------------------------------
# -------------------------------------------------------

phone_names = [
    "Samsung Galaxy A15 5G 128GB Blue Black",
    "Apple iPhone 14 Pro Max 256GB Purple",
    "Samsung Galaxy A55",
    "Samsung Galaxy S24 Ultra 512GB 12GB RAM Titanium Black",
    "Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
    "OnePlus 12 12GB RAM 256GB",
    "Samsung Galaxy A34 Dual SIM 6GB RAM 128GB Storage",
    "Xiaomi 14 Ultra Dual SIM 5G 512GB 16GB 5G White",
    "Apple iPhone 15 Pro Max, 6.7 OLED Super Retina XDR Display A17 Pro Chip  256GB Storage Bluetooth 5.3 Face ID TRA Version Natural Titanium",
    "HUAWEI nova 10 Dual Sim Smartphone, 6.67 Curved OLED Display, 8GB RAM 256 GB Storage, LTE 4G, 60 MP Front Ultra Wide Camera",
    "HUAWEI nova 11i SmartPhone 8GB 128GB Starry Black",
    "vivo V30 5G Noble Black 12GB 12GB RAM 512GB",
    "Samsung Galaxy Z Flip6 AI Smartphone 12GB RAM 512GB Storage Silver Shadow",
    "Apple iPhone 13 Pro Max, 128GB, Graphite - Unlocked",
    "SAMSUNG Galaxy S24 Ultra Cell Phone 256GB AI Smartphone Unlocked Android 200MP 100x Zoom Cameras",
    "Apple iPhone 11 A13 Bionic 4GB, 64GB 6.1inch iOS A GRADE Red (Unlocked) Refurbished",
    "Apple iPhone 12 128GB GSM/CDMA Fully Unlocked - Blue",
    "Samsung Galaxy S22 Ultra 5G 128GB Fully Unlocked SM-S908 (2022) - Red - Good Condition",
    "Original LG Smart Folder 4G LTE Mobile Phone Unlocked LG X100 3.3'' 2GB RAM 16GB ROM 4.9MP Camera FM Radio Android SmartPhone",
    "HTC Status ChaCha A810a Unlocked Phone with QWERTY Keyboard, 5MP Camera, Wi-Fi and GPS - US Warranty - Silver",
    "Sony Ericsson Xperia X10 Mini E10i",
    "ASUS Phone ZA550KL-S425-1G16G-BK Zenfone Live L1 5.45 1GB 16GB Black Retail"
]
df = request_data_from_server(phone_names)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
