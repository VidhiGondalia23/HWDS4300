Part I 
Authors: (Vidhi & Kristie)

1. This model will result in longer query time because everything is in the same table. It would require joins or more attribute
filtering. The model will take up a lot of space because every product will need a column for every potential property being 
documented, even if they are irrelevant. Since different products have varying attributes this model will not be efficient 
to store all of them together, because it is bound to have a lot of empty columns. Assuming this table (named product) will
include a column with category classification, like Watches, we can query using:

SELECT * FROM PRODUCT WHERE category_id = ‘WATCHES’ AND diameter = 44 AND brand = “Tommy Hilfiger” AND dial_color = “Beige”

2. Assuming the tables in this database are connected to each other with Category ID and product ID, querying will be easier 
because we can search directly within a table that includes only watches. Each row will only have relevant columns, so it 
will take up less space. 

SELECT * FROM WATCHES WHERE diameter = 44 AND brand = “Tommy Hilfiger” AND dial_color = “Beige”

3. This will result in multiple tuples existing per product to represent multiple attributes. This makes querying time
consuming because we have to search for the product_id through the Property table multiple times to ensure all three 
attributes exist. Additionally, it will take more space, this will also require a join with the product table if we do 
not know the property ID for watches(assuming it is a numeric or alphanumeric ID).

SELECT * FROM PRODUCT WHERE product_id IN (SELECT product_id FROM PROPERTY WHERE category = “WATCHES” AND key = “diameter”
AND value = “44”) AND product_id IN (SELECT product_id FROM PROPERTY WHERE key = “brand” AND value = “Tommy Hilfiger”) AND 
product_id IN ((SELECT product_id FROM PROPERTY WHERE key = “dial_color” AND value = “Beige”)

4. Create HMSET keyed by product_id that includes properties, like category, brand, dial_color, etc. Maintain indices to
map the properties to products using sets. Then search products by intersecting sets. This can be time consuming because we 
will need to maintain index sets for every property to maintain searchability. 
sinter category:”Watches” diameter:44 brand:”Tommy Hilfiger” dial_color:”Beige”
Using python, we can make a function look up values based on the input (category of interest) provided. 

5. This may be the fastest query of all, mostly because there was no need for joins and the query included all the keys 
and values. It also meant that we didn’t need to save different kinds of products in different collections or tables. 
We could add products with specific attributes pertaining to the type of product. They can all exist in one place without 
taking unnecessary space like in 1. 

 For product in products.find({“diameter”:”44mm”, “brand”:”Tommy Hilfiger”,”dial_color”:”Beige”})
