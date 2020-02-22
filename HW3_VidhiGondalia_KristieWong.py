import pprint
#Author:Vidhi Gondalia
from pymongo import MongoClient

client = MongoClient('localhost')

db = client['product_catalog']

#make product catelog with different cateogory products
product_catalog = [{"productID": 12884,
           "product_name": "Gucci Guilty",
           "category":"Fragrance",
           "brand": "Gucci",
           "price":40,
           "profile":["woody", "aqua", "fresh"], 
           "is_available": True},
        {"productID": 12885,
           "product_name": "fossil Timeless",
           "category":"Watch",
           "brand":"Fossil",
           "price":190,
           "diameter": "50mm",
           "dial_color": "Bblue",
           "is_available": False},
        {"productID": 12886,
           "product_name": "Tick558",
           "category":"Watch",
           "price":200,
           "diameter":"44mm",
           "brand":"Tommy Hilfiger",
           "dial_color":"Beige",
           "is_available": True},
        {"productID": 12887,
           "product_name": "peacoat",
           "category":"Clothing",
           "price":73,
           "brand": "Tommy Hilfiger",
           "clothtype":["Cotton", "Polyester"],
           "is_available": True},
        {"productID": 12888,
           "product_name": "Burberry Coat",
           "category":"Clothing",
           "price":899,
           "clothtype": ["Cotton", "Wool"],
           "is_available": True},
        {"productID": 12889,
           "product_name": "Delino Bag",
           "category":"Bag",
           "price":899,
           "brand":"Prada",
           "type":'Leather',
           "is_available": True}]

products = db.products
#insert products in database
result = products.insert_many(product_catalog)


#find name of all collections in the database
db.list_collection_names()

#query to find products that have the following attributes
for product in products.find({"diameter":"44mm", "brand":"Tommy Hilfiger","dial_color":"Beige"}):
    pprint.pprint(product)

#query to find all products that are not available
for product in products.find({"is_available":False}):
    pprint.pprint(product)

#query to find products that are in the clothing category
products.count_documents({"category":"Clothing"})



