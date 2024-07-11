"""Python script that will get a list of products that are out of stock in the dev site."""

from cred import url, key, secret
from woocommerce import API 
import json
import csv



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
out_of_stock = []
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
                  out_of_stock.append({'id': product['id'], 'product_name': product['name']})
            else:
                  ISname = product['name'] +',' + product['stock_status']
                  in_stock.append(ISname)

        current_page += 1 



with open('ofs.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      for i in out_of_stock:
            row = f'{i['id']}: {i['product_name']}'
            # f'id: {i['id']}, product_name: {i['product_name']}'
        # for key, value in i.items():
            writer.writerow([row])
         


      

print(count)
print(skipped_items)
print(f'List of out of stock products:{out_of_stock}')
print(f'List of in stock products: {in_stock}')




