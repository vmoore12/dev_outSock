from cred import url, key, secret
from woocommerce import API 
import json
import csv


"""Create a script that that will get list of products that are out of stock in the dev site."""
woo_api = API(
    url=url,
    consumer_key= key,
    consumer_secret= secret,
    wp_api=True,
    version='wc/v3'

)


per_page = 100
current_page = 1
count = 0
skipped_items =[]
out_of_stockID = []
out_of_stockName = []
in_stock = []
while True:
        payload = {
            "per_page": per_page,
            "page": current_page, #Note: this show the specific page you want to see now
        }

        all_products = woo_api.get('products', params=payload).json()
        if not all_products:
                break 
        for product in all_products:
            #note: This goes through all the products and and ignore all the "collections" products/not simple in product type.
            if product['type'] != 'simple':
                s_name = product['name'] +',' + product['type']
                skipped_items.append(s_name)
                continue
            
            if product['stock_status'] == 'outofstock':
                  OFSname = product['name']
                  OFSid = product['id']
                  out_of_stockID.append(OFSid)
                  out_of_stockName.append(OFSname)
            else:
                  ISname = product['name'] +',' + product['stock_status']
                  in_stock.append(ISname)

        current_page += 1 



with open('ofs.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      for i in range(len(out_of_stockID)):
            writer.writerow([f'ID= {out_of_stockID[i]}: {out_of_stockName[i]}'])


      

print(count)
print(skipped_items)
print(f'List of out of stock products:{out_of_stockID}, {out_of_stockName}')
print(f'List of in stock products: {in_stock}')




