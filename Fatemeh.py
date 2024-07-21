import pandas as pd

df = pd.read_csv('products_data.csv')

cs = 15 
cm = 6
p = 10   

df['Manual Price'] = None

new_products = [
    {"Phone names":"Original LG Smart Folder 4G LTE Mobile Phone Unlocked LG X100 3.3'' 2GB RAM 16GB ROM 4.9MP Camera FM Radio Android SmartPhone" , "Newegg Price": None, "Microless Price": None, "Manual Price": 139.00},
    {"Phone names":"HTC Status ChaCha A810a Unlocked Phone with QWERTY Keyboard, 5MP Camera, Wi-Fi and GPS - US Warranty - Silver" , "Newegg Price": None, "Microless Price": None, "Manual Price": 123.52},
    {"Phone names": "Sony Ericsson Xperia X10 Mini E10i", "Newegg Price": None, "Microless Price": None, "Manual Price": 199.99},
    {"Phone names": "ASUS Phone ZA550KL-S425-1G16G-BK Zenfone Live L1 5.45 1GB 16GB Black Retail", "Newegg Price": None, "Microless Price": None, "Manual Price": 109.99}
]

new_df = pd.DataFrame(new_products)
df = pd.concat([df, new_df], ignore_index=True)

df['Product Price'] = df[['Newegg Price', 'Microless Price', 'Manual Price']].min(axis=1)
df['Shipping Cost'] = cs
df['Marketing Cost'] = cm
df['Profit'] = 0
df['Final Price'] = 0

for i, row in df.iterrows():
    cp = row['Product Price']
    min_competitor_price = row[['Newegg Price', 'Microless Price']].min()
    max_competitor_price = row[['Newegg Price', 'Microless Price']].max()
    
    base_price = cp + cs + cm
    profit = base_price * (p / 100)
    final_price = base_price + profit
    
    df.at[i, 'Final Price'] = final_price
    
    if pd.notna(min_competitor_price) and pd.notna(max_competitor_price):
        if min_competitor_price <= final_price <= max_competitor_price:
            df.at[i, 'Competitive Status'] = 'Competitive'
        else:
            df.at[i, 'Competitive Status'] = 'Not Competitive'
    else:
        df.at[i, 'Competitive Status'] = 'Manual Pricing'

result_df = df[['Phone names', 'Final Price', 'Competitive Status']]

print(result_df.head(20))


result_df.to_csv('final_prices_with_status.csv', index=False)

