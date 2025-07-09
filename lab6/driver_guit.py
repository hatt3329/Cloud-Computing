import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Ping
print("1. Ping:", requests.get(f"{BASE_URL}/ping").json())

# 2. Get all products
print("2. All Products:", requests.get(f"{BASE_URL}/products").json())

# 3. Product Count
print("3. Product Count:", requests.get(f"{BASE_URL}/products/count").json())

# 4. Get Product by ID
print("4. Get Product by ID:", requests.get(f"{BASE_URL}/products/1").json())

# 5. Update Product Price
price_update = 999.99
print("5. Update Product Price:", requests.put(f"{BASE_URL}/products/1/price", json=price_update).json())

# 6. Update Product Name
name_update = "Updated Guitar Name"
print("6. Update Product Name:", requests.put(f"{BASE_URL}/products/1/name", json=name_update).json())

# 7. Expensive Products
print("7. Expensive Products:", requests.get(f"{BASE_URL}/products/expensive").json())

# 8. Affordable Products
print("8. Affordable Products:", requests.get(f"{BASE_URL}/products/affordable").json())

# 9. Discounted Products
print("9. Discounted Products:", requests.get(f"{BASE_URL}/products/discounted").json())

# 10. Update Product Discount
new_discount = 15.0
print("10. Update Product Discount:", requests.put(f"{BASE_URL}/products/1/discount", json=new_discount).json())