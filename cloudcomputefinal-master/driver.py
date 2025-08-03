import requests 
import json

BASE_URL = "http://127.0.0.1:8000"

work = True

session = requests.Session()
session_tokens = []

while (work):
    print("Vegetable Storefront")
    print("1. Register")
    print("2. Login")
    print("3. Profile")
    print("4. Logout")
    print("5. Product Search")
    print("6. Review Services")
    print("7. Product Management")
    print("8. Shopping Cart")
    print("9. Return an Order")
    print("0. Exit")
    answer = input("Vegtable Storefront: ")

    if answer == '0':
        work = False
        print("Exiting.")
        continue

    try:
        answer = int(answer)
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
#Register
    if answer == 1:
        VendorOrUserRegister = input("1. Vendor or 2. User: ")
        print("Enter: ")
        if (VendorOrUserRegister == '1'):
            vendor_name = input("Enter your vendor name: ")
            email_address = input("Enter your email: ")
            password = input("Enter your password: ")
            phone = input("Enter your phone: ")
            address = input("Enter your address: ")

            payload = {
                "vendor_name": vendor_name.strip(),
                "email_address": email_address.strip(),
                "password": password.strip(),
                "phone": phone.strip(),
                "address": address.strip()
            }
            payload = {key: value for key, value in payload.items() if value is not None}

            try:
                response = session.put(f"{BASE_URL}/vendor/register", json=payload)
                print(f"Status Code: {response.status_code}")
                print("Response:", response.json())
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. Make sure FastAPI is running.")
            
        elif (VendorOrUserRegister == '2'):
            email_address = input("Enter your email: ")
            password = input("Enter your password: ")
            first_name = input("Enter your first name")
            last_name = input("Enter your last name")

            payload = {
                    "email_address": email_address,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                }   
            payload = {key: value for key, value in payload.items() if value is not None}

            try:
                response = session.put(f"{BASE_URL}/register", json=payload)
                print(f"Status Code: {response.status_code}")
                print("Response:", response.json())
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. Make sure FastAPI is running.")
        else:
            break
#login
    if answer == 2:
        print("User type: ")
        print("1. Customer")
        print("2. Vendor")
        VendorOrUser = input("Enter: ")
        if (VendorOrUser == '1') :
            print("User login")
            email_address = input("Enter your email: ")
            password = input("Enter your password: ")

            payload = {
                    "email_address": email_address,
                    "password": password,
                }   
            payload = {key: value for key, value in payload.items() if value is not None}

            try:
                response = session.put(f"{BASE_URL}/login", json=payload)
                print(f"Status Code: {response.status_code}")
                print("Response:", response.json())
                #header/tokens
                auth_token = response.json().get("token")
                if auth_token:
                    session_tokens.append(auth_token)
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. Make sure FastAPI is running.")
        else:
            print("Vendor Login")
            email_address = input("Enter your email: ")
            password = input("Enter your password: ")

            payload = {
                    "email_address": email_address.strip(),
                    "password": password.strip(),
                }   
            payload = {key: value for key, value in payload.items() if value is not None}

            try:
                response = session.put(f"{BASE_URL}/vendor/login", json=payload)
                print(f"Status Code: {response.status_code}")
                print("Response:", response.json())
                auth_token = response.json().get("token")
                if auth_token:
                    session_tokens.append(auth_token)
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. Make sure FastAPI is running.")
#update user info
    if answer == 3:
        try:
            auth_token = session_tokens[-1] if session_tokens else None

            if not auth_token:
                print("No token found. Please log in.")
                continue

            # Send both cookie and header
            headers = { "Authorization": f"Bearer {auth_token}" }

            response = session.get(f"{BASE_URL}/profile", headers=headers)
            if response.status_code == 200:
                profile_data = response.json()
                
                if "customer_id" in profile_data["profile"]:
                    #Display customer info
                    customer = profile_data['profile']

                    print(f"\n {customer['first_name']}'s Profile")
                    print("-" * 40)
                    print(f"{'Email:':<15}{customer['email_address']}")
                    print(f"{'First Name:':<15}{customer['first_name']}")
                    print(f"{'Last Name:':<15}{customer['last_name']}")
                    print("-" * 40)
                    while True:
                        print("\nWhat would you like to do?")
                        print("1. Edit profile")
                        print("2. View your orders")
                        print("3. Return to main menu")

                        choice = input("Enter choice: ").strip()
                        if choice == "1":
                            password = input("Enter new password (or leave blank): ")
                            if (password == ""):
                                password = None
                            first_name = input("Enter new first name (or leave blank): ")
                            if (first_name == ""):
                                first_name = None
                            last_name = input("Enter new last name (or leave blank): ")
                            if (last_name == ""):
                                last_name = None
                            email = input("Enter new email (or leave blank): ")
                            if (email == ""):
                                email = None
                            
                            payload = {
                            "password": password.strip() if password else None,
                            "first_name": first_name.strip() if first_name else None,
                            "last_name": last_name.strip() if last_name else None,
                            "email": email.strip() if email else None
                            }
                            payload = {key: value for key, value in payload.items() if value is not None}
                            try:
                                response = session.put(f"{BASE_URL}/update_user_info/{customer['customer_id']}", json=payload)
                                print(f"Status Code: {response.status_code}")
                                print("Response:", response.text)
                            except requests.exceptions.ConnectionError:
                                print("Error: Could not connect to the API. Make sure FastAPI is running.")
                            break
                        elif choice == "2":
                            try:
                                response = session.get(f"{BASE_URL}/order", headers=headers)
                                data2 = response.json()
                                print("\nYour Orders")
                                headers = ["Order ID", "Product Name", "Quantity", "Price at Order"]

                                print(f"{headers[0]:<10}{headers[1]:<15}{headers[2]:<10}{headers[3]:<15}")
                                print("-" * 50) 
                                for row in data2:
                                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<15}")
                            except requests.exceptions.ConnectionError:
                                print("Error: Could not connect to the API.")
                            
                        elif choice == "3":
                            break
                        else:
                            print("Invalid choice. Please select 1, 2, or 3.")
                elif "vendor_id" in profile_data["profile"]:
                    # Display vendor info
                    vendor = profile_data['profile']

                    print(f"\n {vendor['vendor_name']}'s Profile")
                    
                    print("-" * 40)
                    print(f"{'Vendor Name:':<15}{vendor['vendor_name']}")
                    print(f"{'Email:':<15}{vendor['email_address']}")
                    print(f"{'Phone:':<15}{vendor['phone']}")
                    print(f"{'Address:':<15}{vendor['address']}")
                    print("-" * 40)


                    while True:
                        print("\nWhat would you like to do?")
                        print("1. Edit profile")
                        print("2. View your products")
                        print("3. Add products")
                        print("4. Return to main menu")

                        choice = input("Enter choice: ").strip()
                        if choice == "1":
                            vendor_name = input("Enter new vendor name (or leave blank): ")
                            if (vendor_name == ""):
                                vendor_name = None
                            email = input("Enter new email (or leave blank): ")
                            if (email == ""):
                                email = None
                            password = input("Enter new password (or leave blank): ")
                            if (password == ""):
                                password = None
                            phone = input("Enter new phone (or leave blank): ")
                            if (phone == ""):
                                phone = None
                            address = input("Enter new address (or leave blank): ")
                            if (address == ""):
                                address = None
                            
                            payload = {
                            "vendor_name": vendor_name.strip() if vendor_name else None,
                            "email": email.strip() if email else None,
                            "password": password.strip() if password else None,
                            "phone": phone.strip() if phone else None,
                            "address": address.strip() if address else None
                            }
                            payload = {key: value for key, value in payload.items() if value is not None}
                            try:
                                response = session.put(f"{BASE_URL}/myproducts/{vendor['vendor_id']}", json=payload)
                                print(f"Status Code: {response.status_code}")
                                print("Response:", response.text)
                            except requests.exceptions.ConnectionError:
                                print("Error: Could not connect to the API. Make sure FastAPI is running.")
                        elif choice == "2":
                            try:
                                headers = { "Authorization": f"Bearer {auth_token}" }
                                response = session.get(f"{BASE_URL}/myproducts", headers=headers)
                                print(f"Status Code: {response.status_code}")
                                print("Response:", response.text)
                                products = json.loads(response.text)
                                print(f"{'ProductID':<15}{'Name':<15} {'Description':<25} {'Price':<10} {'Quantity':<10}")
                                print("-" * 60)

                                for product in products:
                                    pid, name, desc, price, qty = product
                                    print(f"{pid:<15} {name:<15} {desc:<25} ${price:<9.2f} {qty:<10}")
                            except requests.exceptions.ConnectionError:
                                print("Error: Could not connect to the API. Make sure FastAPI is running.")
                        elif choice == "3":
                            product_name = input("Enter product name: ")
                            if (product_name == ""):
                                product_name = None
                            product_description = input("Enter product description: ")
                            if (product_description == ""):
                                product_description = None
                            unit_price = input("Enter price of product: ")
                            if (unit_price == ""):
                                unit_price = None
                            stock_quantity = input("Enter stock amount: ")
                            if (stock_quantity == ""):
                                stock_quantity = None
                            category = input("Enter category in which product belongs in. (Leafy Greens),  (Cruciferous), (Root Vegetables), (Fruit Vegatables), (Bulbs & Alliums) (or enter N/A): ")
                            if (category == ""):
                                category = None
                            
                            unit_price = float(unit_price) if unit_price else None
                            stock_quantity = int(stock_quantity) if stock_quantity else None

                            payload = {
                            "product_name": product_name.strip() if product_name else None,
                            "product_description": product_description.strip() if product_description else None,
                            "unit_price": unit_price,
                            "stock_quantity": stock_quantity,
                            "category": category.strip() if category else None
                            }
                            payload = {key: value for key, value in payload.items() if value is not None}
                            try:
                                headers = { "Authorization": f"Bearer {auth_token}" }
                                response = session.put(f"{BASE_URL}/addproduct/", json=payload, headers=headers)
                                print(f"Status Code: {response.status_code}")
                                print("Response:", response.text)
                            except requests.exceptions.ConnectionError:
                                print("Error: Could not connect to the API. Make sure FastAPI is running.")
                        elif choice == "4":
                            break
                        else:
                            print("Invalid choice. Please select 1, 2, or 3.")

                else:
                    print("Invalid profile data.")
            else:
                print("Failed to fetch profile. Status Code:", response.status_code)
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the API. Make sure FastAPI is running.")
#Logout
    if answer == 4:
        try:
            response = session.get(f"{BASE_URL}/Logout")
            for cookie in session.cookies:
                if cookie.name == "session_id":
                    session.cookies.clear(domain=cookie.domain, path=cookie.path, name="session_id")
            print(f"Status Code: {response.status_code}")
            print("Response:", response.json())
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the API. Make sure FastAPI is running.")


# === Service 3: Product Search ===
    if answer == 5:
        print("\n[Product Search]")
        print("1. View All Products")
        print("2. View Product by ID")
        print("3. Filter Products")
        sub = input("Choose: ")
        if sub == '1':
            try:
                r = session.get(f"{BASE_URL}/products")
                response_data = r.json() 

                product_keys = ["product_id", "category_id", "vendor_id", "sku", "product_name", "description", "unit_price", "stock_quantity", "date_added"]

                products = []
                for product in response_data:
                    product_dict = dict(zip(product_keys, product))
                    products.append(product_dict)

                if products:
                    print(f"\n{'Product ID':<25}{'Product Name':<25} {'Category ID':<15} {'Vendor ID':<15} {'Price':<10} {'Stock Quantity':<15} {'Description'}")
                    print("-" * 150)

                    for product in products:
                        product_id = product.get('product_id', 'N/A')
                        product_name = product.get('product_name', 'N/A')
                        category_id = product.get('category_id', 'N/A')
                        vendor_id = product.get('vendor_id', 'N/A')
                        price = product.get('unit_price', 0)
                        stock_quantity = product.get('stock_quantity', 0)
                        description = product.get('description', 'N/A')

                        print(f"{product_id:<25} {product_name:<25} {category_id:<15} {vendor_id:<15} ${price:<9.2f} {stock_quantity:<15} {description}")
                else:
                    print("No products available.")
                    
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. Make sure FastAPI is running.")
        elif sub == '2':
            pid = input("Enter product ID: ")
            r = session.get(f"{BASE_URL}/product/{pid}")
            response_data = r.json() 

            product_keys = ["product_id", "category_id", "vendor_id", "sku", "product_name", "description", "unit_price", "stock_quantity", "date_added"]

            product_dict = dict(zip(product_keys, response_data))
            product_id = product_dict.get('product_id', 'N/A')
            product_name = product_dict.get('product_name', 'N/A')
            category_id = product_dict.get('category_id', 'N/A')
            vendor_id = product_dict.get('vendor_id', 'N/A')
            price = product_dict.get('unit_price', 0)
            stock_quantity = product_dict.get('stock_quantity', 0)
            description = product_dict.get('description', 'N/A')

            print(f"\n{'Product ID':<25}{'Product Name':<25} {'Category ID':<15} {'Vendor ID':<15} {'Price':<10} {'Stock Quantity':<15} {'Description'}")
            print("-" * 150)
            print(f"{product_id:<25} {product_name:<25} {category_id:<15} {vendor_id:<15} ${price:<9.2f} {stock_quantity:<15} {description}")
        elif sub == '3':
            cat = input("Category (optional): ")
            minp = input("Min Price (optional): ")
            maxp = input("Max Price (optional): ")
            params = {"category": cat, "min_price": minp, "max_price": maxp}
            r = session.get(f"{BASE_URL}/products/filter", params=params)
            print(r.json())

# === Service 5: Reviews ===
    if answer == 6:
        print("\n[Review Services]")
        print("1. Add Review")
        print("2. Edit Review")
        print("3. Delete Review")
        sub = input("Choose: ")
        auth_token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {auth_token}"}
        if sub == '1':
            pid = int(input("Product ID: "))
            rating = int(input("Rating 1-5: "))
            text = input("Review: ")
            data = {"product_id": pid, "rating": rating, "review_text": text}
            r = session.put(f"{BASE_URL}/review", json=data, headers=headers)
            print(r.json())
        elif sub == '2':
            rid = int(input("Review ID: "))
            rating = int(input("New Rating: "))
            text = input("New Review Text: ")
            data = {"product_id": 0, "rating": rating, "review_text": text}
            r = session.put(f"{BASE_URL}/review/{rid}", json=data, headers=headers)
            print(r.json())
        elif sub == '3':
            rid = int(input("Review ID: "))
            r = session.delete(f"{BASE_URL}/review/{rid}", headers=headers)
            print(r.json())

# === Service 6: Product Management ===
    if answer == 7:
        print("\n[Product Management]")
        print("1. Update Product")
        print("2. Delete Product")
        print("0. Exit")
        sub = input("Choose: ")
        auth_token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {auth_token}"}
        if sub == '1':
            pid = input("Enter product ID: ")
            product_name = input("Enter new product name (or leave blank): ")
            if (product_name == ""):
                product_name = None
            product_description = input("Enter new product description (or leave blank): ")
            if (product_description == ""):
                product_description = None
            unit_price = input("Enter new price of product (or leave blank): ")
            if (unit_price == ""):
                unit_price = None
            stock_quantity = input("Enter new stock amount(or leave blank): ")
            if (stock_quantity == ""):
                stock_quantity = None
            category = None
            
            unit_price = float(unit_price) if unit_price else None
            stock_quantity = int(stock_quantity) if stock_quantity else None

            payload = {
            "product_name": product_name.strip() if product_name else None,
            "product_description": product_description.strip() if product_description else None,
            "unit_price": unit_price,
            "stock_quantity": stock_quantity,
            "category": category.strip() if category else None
            }
            payload = {key: value for key, value in payload.items() if value is not None}

            r = session.put(f"{BASE_URL}/product/{pid}", json=payload, headers=headers)
            print("Response:", response.text)
        elif sub == '2':
            pid = int(input("Product ID to delete: "))
            r = session.delete(f"{BASE_URL}/product/{pid}", headers=headers)
            print(f"Status Code: {r.status_code}")
            print("Response:", r.text)
        else:
            continue

# === Service 7: Shopping Cart ===
    if answer == 8:
        print("\n[Shopping Cart]")
        print("1. Add to Cart")
        print("2. Checkout")
        print("0. Exit")
        sub = input("Choose: ")
        auth_token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {auth_token}"}
        if sub == '1':
            pid = int(input("Product ID: "))
            qty = int(input("Quantity: "))
            data = {"product_id": pid, "quantity": qty}
            r = session.put(f"{BASE_URL}/cart", json=data, headers=headers)
            print(r.text)
        elif sub == '2':
            r = session.put(f"{BASE_URL}/checkout", headers=headers)
            print(r.json())
        else:
            continue

# === Service 10: Return Service ===
    if answer == 9:
        print("\n[Return Order]")
        oid = int(input("Order ID to return: "))
        auth_token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {auth_token}"}
        r = session.put(f"{BASE_URL}/return/{oid}", headers=headers)
        print(r.json())