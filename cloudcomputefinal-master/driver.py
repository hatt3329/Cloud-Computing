import requests 
import json

BASE_URLS = {
    "user": "http://127.0.0.1:8001",
    "vendor": "http://127.0.0.1:8002",
    "product_search": "http://127.0.0.1:8003",
    "profile": "http://127.0.0.1:8004",
    "reviews": "http://127.0.0.1:8005",
    "product_mgmt": "http://127.0.0.1:8006",
    "cart": "http://127.0.0.1:8007",
    "order": "http://127.0.0.1:8008",
    "vendor_profile": "http://127.0.0.1:8009",
    "returns": "http://127.0.0.1:8010"
}

session = requests.Session()
session_tokens = []

work = True
while work:
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

    # Register
    if answer == 1:
        role = input("1. Vendor or 2. User: ")
        if role == '1':
            payload = {
                "vendor_name": input("Vendor Name: ").strip(),
                "email_address": input("Email: ").strip(),
                "password": input("Password: ").strip(),
                "phone": input("Phone: ").strip(),
                "address": input("Address: ").strip()
            }
            r = session.put(f"{BASE_URLS['vendor']}/vendor/register", json=payload)
        elif role == '2':
            payload = {
                "email_address": input("Email: ").strip(),
                "password": input("Password: ").strip(),
                "first_name": input("First Name: ").strip(),
                "last_name": input("Last Name: ").strip()
            }
            r = session.put(f"{BASE_URLS['user']}/register", json=payload)
        else:
            continue
        print(r.status_code, r.json())

    # Login
    elif answer == 2:
        print("1. Customer  2. Vendor")
        role = input("Enter: ")
        payload = {
            "email_address": input("Email: ").strip(),
            "password": input("Password: ").strip()
        }
        endpoint = "login" if role == '1' else "vendor/login"
        url = f"{BASE_URLS['user']}/{endpoint}" if role == '1' else f"{BASE_URLS['vendor']}/{endpoint}"
        r = session.put(url, json=payload)
        print(r.status_code, r.json())
        token = r.json().get("token")
        if token:
            session_tokens.append(token)

    # Profile
    elif answer == 3:
        token = session_tokens[-1] if session_tokens else None
        if not token:
            print("Please log in first.")
            continue
        headers = {"Authorization": f"Bearer {token}"}
        r = session.get(f"{BASE_URLS['profile']}/profile", headers=headers)
        print(r.json())

    # Logout
    elif answer == 4:
        r = session.get(f"{BASE_URLS['profile']}/Logout")
        print(r.status_code, r.json())

    # Product Search
    elif answer == 5:
        print("1. All Products  2. By ID  3. Filter")
        sub = input("Choose: ")
        if sub == '1':
            r = session.get(f"{BASE_URLS['product_search']}/products")
        elif sub == '2':
            pid = input("Product ID: ")
            r = session.get(f"{BASE_URLS['product_search']}/product/{pid}")
        elif sub == '3':
            params = {
                "category": input("Category: "),
                "min_price": input("Min Price: "),
                "max_price": input("Max Price: ")
            }
            r = session.get(f"{BASE_URLS['product_search']}/products/filter", params=params)
        else:
            continue
        print(r.json())

    # Reviews
    elif answer == 6:
        print("1. Add  2. Edit  3. Delete")
        sub = input("Choose: ")
        token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {token}"}
        if sub == '1':
            data = {
                "product_id": int(input("Product ID: ")),
                "rating": int(input("Rating 1-5: ")),
                "review_text": input("Text: ")
            }
            r = session.put(f"{BASE_URLS['reviews']}/review", json=data, headers=headers)
        elif sub == '2':
            rid = int(input("Review ID: "))
            data = {
                "product_id": 0,
                "rating": int(input("New Rating: ")),
                "review_text": input("New Text: ")
            }
            r = session.put(f"{BASE_URLS['reviews']}/review/{rid}", json=data, headers=headers)
        elif sub == '3':
            rid = int(input("Review ID: "))
            r = session.delete(f"{BASE_URLS['reviews']}/review/{rid}", headers=headers)
        else:
            continue
        print(r.json())

    # Product Management
    elif answer == 7:
        print("1. Update Product  2. Delete Product")
        sub = input("Choose: ")
        token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {token}"}
        if sub == '1':
            pid = input("Product ID: ")
            payload = {
                "product_name": input("Name: "),
                "product_description": input("Description: "),
                "unit_price": float(input("Price: ")),
                "stock_quantity": int(input("Quantity: "))
            }
            r = session.put(f"{BASE_URLS['product_mgmt']}/product/{pid}", json=payload, headers=headers)
        elif sub == '2':
            pid = int(input("Product ID: "))
            r = session.delete(f"{BASE_URLS['product_mgmt']}/product/{pid}", headers=headers)
        else:
            continue
        print(r.status_code, r.text)

    # Shopping Cart
    elif answer == 8:
        print("1. Add to Cart  2. Checkout")
        sub = input("Choose: ")
        token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {token}"}
        if sub == '1':
            payload = {
                "product_id": int(input("Product ID: ")),
                "quantity": int(input("Quantity: "))
            }
            r = session.put(f"{BASE_URLS['cart']}/cart", json=payload, headers=headers)
        elif sub == '2':
            r = session.put(f"{BASE_URLS['cart']}/checkout", headers=headers)
        else:
            continue
        print(r.json())

    # Return Order
    elif answer == 9:
        oid = int(input("Order ID to return: "))
        token = session_tokens[-1] if session_tokens else None
        headers = {"Authorization": f"Bearer {token}"}
        r = session.put(f"{BASE_URLS['returns']}/return/{oid}", headers=headers)
        print(r.json())
