import pandas as pd


# Step 1 --> Create Dataset
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
commom_phones = ["Motorola Moto G Play 2023 3GB/32GB 16MP Camera - Navy Blue",
                "Samsung Galaxy S24 Ultra STANDARD EDITION DUAL SIM 512GB ROM + 12GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (Titanium Black)",
                "OnePlus 12 12GB RAM+256GB Dual-SIM Unlocked Android Smartphone Supports Fastest 50W Wireless Charging",
                "Samsung Galaxy A34 EE DUAL SIM 128GB ROM + 6GB RAM (GSM Only | No CDMA) Factory Unlocked 5G Smartphone",
                "Xiaomi 14 Ultra DUAL SIM 512GB ROM + 16GB RAM (GSM | CDMA) Factory Unlocked 5G Smartphone (White)", 
                "Samsung - Galaxy A15 5G 128GB (Unlocked) - Blue Black",
                "Apple iPhone 14 Pro Max 256GB Fully Unlocked Purple - Grade B",
                "Samsung Galaxy A55"
]
# www.newegg.com
only_newegg = [
    "iPhone 13 Pro Max 5G 128GB", 
    "SAMSUNG Galaxy S24 Ultra Cell Phone 256GB AI Smartphone Unlocked Android 200MP 100x Zoom Cameras",
    "Apple iPhone 11 A13 Bionic 4GB, 64GB 6.1inch iOS A GRADE Red (Unlocked) Refurbished",
    "Apple iPhone 12 128GB GSM/CDMA Fully Unlocked - Blue",
    "Samsung Galaxy S22 Ultra 5G 128GB Fully Unlocked SM-S908 (2022) - Red - Good Condition"
] 
# microless.com
only_microless = [
    "Samsung Galaxy A15 5G Dual SIM, 4GB RAM, 128GB Storage, Blue Black (UAE Version)",
    "Apple iPhone 15 Pro Max",
    "HUAWEI nova 10 Dual Sim Smartphone, 6.67 Curved OLED Display, 8GB RAM 256 GB Storage, LTE 4G, 60 MP Front Ultra Wide Camera",
    "HUAWEI nova 11i SmartPhone",
    "vivo V30 5G (Noble Black, 12GB+12GB RAM, 512GB)",
    "Samsung Galaxy Z Flip6 AI Smartphone",
    "HUAWEI nova 10 Pro Dual SIM Smartphone, 6.7 120 Hz Curved Display, Star Orbit Ring Design, 8GB RAM, 256GB Storage, 4G LTE Network, 60 MP/50MP Camera, 4500 mAh Battery, Starry Black | 51097EWH"
]

uncommon_phones = ["Original LG Smart Folder 4G LTE Mobile Phone Unlocked LG X100 3.3'' 2GB RAM 16GB ROM 4.9MP Camera FM Radio Android SmartPhone",
               "HTC Status ChaCha A810a Unlocked Phone with QWERTY Keyboard, 5MP Camera, Wi-Fi and GPS - US Warranty - Silver",
               "Sony Ericsson Xperia X10 Mini E10i",
               "ASUS Phone ZA550KL-S425-1G16G-BK Zenfone Live L1 5.45 1GB 16GB Black Retail"
]

df1 = pd.DataFrame(commom_phones,columns='Common phones')
df2 = pd.DataFrame(only_newegg,columns='Only Newegg')
df3 = pd.DataFrame(only_microless,columns='Only Microless') 
df4 = pd.DataFrame(uncommon_phones,columns='Uncommon_phones') 

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
