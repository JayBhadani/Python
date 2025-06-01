import mysql.connector
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import requests
from collections import Counter

import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)  # autoreset resets the color code after every print statement.

# Wassenger API Key (Replace with your actual API key)
WASSENGER_API_KEY = "98b4111c5bc4d4748c82c9fc01d3af3475788d3b693c3f72997d16c5790d7003d1190ab9f6825909"

def send_whatsapp_message(phone_number, message):
    url = "https://api.wassenger.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Token": WASSENGER_API_KEY
    }
    payload = {
        "phone": phone_number,
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Bill sent successfully via WhatsApp!")
    else:
        print(f"Failed to send bill. Response: {response.text}")

# Mobile Number Start with +91 portal;
def format_phone_number(phone):
    if phone.startswith("+91"):
        return phone
    else:
        print(Fore.RED + "Invalid country code! Please enter a valid Indian phone number starting with +91.")
        return None

def get_valid_phone_number():
    while True:
        phone = input("Enter your phone number (must start with +91): ")
        if phone.startswith("+91"):
            return phone
        print(Fore.RED + "Invalid country code! Please enter a valid Indian phone number starting with +91.")

# Admin portal;
def admin():
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
    cursor = conn.cursor(buffered=True)
    
    name = input("Enter Admin Name: ")
    password = input("Enter Admin Password: ")
    cursor.execute("SELECT first_name FROM admin WHERE first_name = %s AND password = %s", (name, password))
    admin = cursor.fetchone()
    
    if admin:
        print(Fore.YELLOW + f"Welcome, {admin[0]}! You have admin access.")
        while True:
            print(Fore.BLUE + "1. Add Book\n2. View Books\n3. Graph\n4. Exit")
            try:
                ch1 = int(input("Enter Choice: "))
                if ch1 == 1:
                    add_book()
                elif ch1 == 2:
                    view_book()
                elif ch1 == 3:
                    chat_bar = True
                    while chat_bar:
                        print(Fore.BLUE + "1. Bar Chart\n2. Pie Chart\n3. Exit")
                        try:
                            chat = int(input("Enter Choice: "))
                            if chat == 1:
                                Bar_chart()
                            elif chat == 2:
                                Pi_chat()
                            else:
                                print(Fore.GREEN + "Exiting Admin graph panel.")
                                chat_bar = False
                                break
                        except ValueError:
                            print(Fore.RED + "Please enter a valid number.")
                elif ch1 == 4:
                    print(Fore.GREEN + "Exiting admin panel.")
                    break
                else:
                    print(Fore.RED + "Invalid choice! Try again.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
    else:
        print(Fore.RED + "Invalid admin credentials!")
    conn.close()

# Add Book Only Admin Portal;
def add_book():
    print(Fore.BLUE + "1. General Knowledge\n2. Mythology\n3. Social Science\n4. Exit")
    try:
        ch = int(input("Enter choice: "))
        if ch in [1, 2, 3]:
            name = input("Enter book name: ")
            qty = int(input("Book quantity: "))
            price = int(input("Book price: "))
            category = ["General Knowledge", "Mythology", "Social Science"][ch - 1]
            file_name = ["General_Knowledge.txt", "Mythology.txt", "Social_science.txt"][ch - 1]

            try:
                with open(file_name, 'r') as f:
                    books = [line.strip().split(',') for line in f.readlines()]
            except FileNotFoundError:
                books = []

            book_found = False
            for book in books:
                if book[0] == name:
                    book[1] = str(int(book[1]) + qty)
                    book[2] = str(price)
                    book_found = True
                    break

            if not book_found:
                books.append([name, str(qty), str(price)])

            with open(file_name, 'w') as f:
                for updated_book in books:
                    f.write(",".join(updated_book) + "\n")

            conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT quantity FROM books WHERE name = %s AND category = %s", (name, category))
            existing_book = cursor.fetchone()

            if existing_book:
                new_qty = existing_book[0] + qty
                cursor.execute("UPDATE books SET quantity = %s, price = %s WHERE name = %s AND category = %s",
                               (new_qty, price, name, category))
            else:
                cursor.execute("INSERT INTO books (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
                               (name, category, qty, price))
    
            conn.commit()
            conn.close()
            print(Fore.GREEN + "Book added successfully in both text file and database!")
        else:
            print(Fore.RED + "Invalid Input!")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")

# User Portal;
def user():
    store = True
    while store:
        exists = input(Fore.LIGHTGREEN_EX + "Does user already exist? (yes/no): ").strip().lower()
        
        if exists == "yes":
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
            cursor = conn.cursor(buffered=True)
            phone_number = input("Enter Your Phone Number: ")
            cursor.execute("SELECT id, first_name FROM user WHERE phone_number = %s", (phone_number,))
            user = cursor.fetchone()
            
            if user:
                print(Fore.GREEN + f"Welcome, {user[1]}! You have user access.")
                while True:
                    print(Fore.BLUE + "1. View Book\n2. Purchase Book\n3. Print Bill\n4. Exit")
                    try:
                        ch2 = int(input("Enter Choice: "))
                        if ch2 == 1:
                            view_book()
                        elif ch2 == 2:
                            purchase_book()
                        elif ch2 == 3:
                            bill_print()
                        elif ch2 == 4:
                            print(Fore.GREEN + "Exiting user panel.")
                            store = False
                            break
                        else:
                            print(Fore.RED + "Invalid choice! Try again.")
                    except ValueError:
                        print(Fore.RED + "Please enter a valid number.")
            else:
                print(Fore.RED + "User not found!")
            
            conn.close()

        elif exists == "no":
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
            cursor = conn.cursor(buffered=True)
            first_name = input("Enter User Name: ")
            phone_number = input("Enter User Phone Number: ")

            cursor.execute("INSERT INTO user (first_name, phone_number) VALUES (%s, %s)", (first_name, phone_number))
            conn.commit()
            conn.close()

            print("User registered successfully!")

            conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT id, first_name FROM user WHERE phone_number = %s", (phone_number,))
            user = cursor.fetchone()

            if user:
                print(f"Welcome, {user[1]}! You have user access.")
                while True:
                    print(Fore.BLUE + "1. View Book\n2. Purchase Book\n3. Print Bill\n4. Exit")
                    try:
                        ch3 = int(input("Enter Choice: "))
                        if ch3 == 1:
                            view_book()
                        elif ch3 == 2:
                            purchase_book()
                        elif ch3 == 3:
                            bill_print()
                        elif ch3 == 4:
                            print(Fore.GREEN + "Exiting user panel.")
                            store = False
                            break
                        else:
                            print(Fore.RED + "Invalid choice! Try again.")
                    except ValueError:
                        print(Fore.RED + "Please enter a valid number.")
            else:
                print(Fore.RED + "User not found!")

            conn.close()

        else:
            print("Enter a valid choice.")

# Admin and User View Book Portal;
def view_book():
    files = ["General_Knowledge.txt", "Mythology.txt", "Social_science.txt"]
    
    for file in files:
        try:
            df = pd.read_csv(file, header=None, names=['Book Name', 'Quantity', 'Price'])
            
            if df.empty:
                print(Fore.RED + f"No books found in {file}.")
            else:
                print(Fore.LIGHTMAGENTA_EX + f"Books from {file}:\n", df)
                print()
        
        except FileNotFoundError:
            print(Fore.RED + f"File {file} not found.")
        except pd.errors.EmptyDataError:
            print(Fore.RED + f"File {file} is empty.")
        except pd.errors.ParserError:
            print(Fore.RED + f"File {file} is not in the correct format.")
        except Exception as e:
            print(Fore.RED + f"An error occurred while reading {file}: {e}")

# User Purchase Book Portal;
def purchase_book():
    user_phone = input("Enter your phone number for billing: ").strip()
    
    # Connect to the database using a buffered cursor
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
    cursor = conn.cursor(buffered=True)
    
    cursor.execute("SELECT id FROM user WHERE phone_number = %s", (user_phone,))
    user = cursor.fetchone()

    if not user:
        print(Fore.RED + "User not found in database. Please register first.")
        conn.close()
        return

    user_id = user[0]
    total_purchases = []  # To store all books purchased in this session

    while True:
        print(Fore.BLUE + "1 for General Knowledge\n2 for Mythology\n3 for Social Science")
        
        try:
            n = int(input("Book Type Number: "))
            if n not in [1, 2, 3]:
                print("Invalid Book Type!")
                continue
        except ValueError:
            print(Fore.RED + "Please enter a valid number!")
            continue

        file_name = ["General_Knowledge.txt", "Mythology.txt", "Social_science.txt"][n - 1]
        category = ["General Knowledge", "Mythology", "Social Science"][n - 1]

        try:
            with open(file_name, 'r') as f:
                books = [line.strip().split(',') for line in f.readlines()]
        except FileNotFoundError:
            print(Fore.RED + "File not found.")
            continue

        bookname = input("Enter Book Name: ").strip()
        
        for book in books:
            if len(book) < 3:
                print(Fore.RED + "Error in book file formatting!")
                return
            
            if book[0].strip().lower() == bookname.lower():
                try:
                    available_qty = int(book[1])
                    price = float(book[2])
                except ValueError:
                    print(Fore.RED + "Invalid book data in file!")
                    return

                try:
                    q = int(input("Enter quantity: "))
                except ValueError:
                    print(Fore.RED + "Invalid quantity entered!")
                    return

                if available_qty >= q:
                    print(Fore.YELLOW + "Order is successful!")

                    book[1] = str(available_qty - q)
                    with open(file_name, 'w') as f:
                        for updated_book in books:
                            f.write(",".join(updated_book) + "\n")

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    total_price = price * q

                    cursor.execute("""
                        INSERT INTO orders (user_id, order_date, book_category, book_name, quantity, price, total_price)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (user_id, now, category, bookname, q, price, total_price))

                    conn.commit()

                    total_purchases.append((now, category, bookname, q, price, total_price))

                    print(Fore.GREEN + "Book added to order.")
                else:
                    print(Fore.RED + "Stock is insufficient!")
                break
        else:
            print(Fore.RED + "Book not found!")

        another = input(Fore.LIGHTGREEN_EX + "Do you want to purchase another book? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    conn.close()

    if total_purchases:  # Only generate bill if there are purchases
        print(Fore.BLUE + "Generating bill...")
        generate_bill(user_phone, total_purchases)
    else:
        print(Fore.RED + "No books purchased. No bill generated.")

# Store This Record in Database portal;
def store_bill_in_db(user_id, order): 
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
    cursor = conn.cursor(buffered=True)
    
    cursor.execute("""
        INSERT INTO Bill (user_id, order_date, book_category, book_name, quantity, price, total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, order[0], order[1], order[2], order[3], order[4], order[5]))
    
    conn.commit()
    conn.close()
    print("Bill stored in database successfully!")

# Multiple Book Add portal;
def generate_bill(user_phone, total_purchases):
    bill_content = f"\n--- Bookstore Bill ---\n"
    total_sum = 0

    for order in total_purchases:
        bill_content += f"""
Date: {order[0]}
Category: {order[1]}
Book Name: {order[2]}
Quantity: {order[3]}
Price per Book: {order[4]}
Total Price: {order[5]}
-----------------------
"""
        total_sum += order[5]

    bill_content += f"\nTotal Amount Payable: {total_sum}\n-----------------------"

    file_name = f"{user_phone}.txt"
    with open(file_name, "w") as file:
        file.write(bill_content)

    print(Fore.LIGHTMAGENTA_EX + f"Bill saved as {file_name}")

    send_whatsapp = input(Fore.LIGHTGREEN_EX + "Do you want the bill on your WhatsApp number? (yes/no): ").strip().lower()
    if send_whatsapp == "yes":
        send_whatsapp_message(user_phone, bill_content)

# File and WhatsApp Bill portal;
def bill_print():
    user_phone = input("Enter your phone number to fetch bill: ")
    
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
    cursor = conn.cursor(buffered=True)

    cursor.execute("SELECT id FROM user WHERE phone_number = %s", (user_phone,))
    user = cursor.fetchone()

    if not user:
        print(Fore.RED + "User not found in database.")
        conn.close()
        return

    user_id = user[0]
    cursor.execute("""
        SELECT order_date, book_category, book_name, quantity, price, total_price 
        FROM orders WHERE user_id = %s ORDER BY order_date DESC
    """, (user_id,))

    orders = cursor.fetchall()

    if not orders:
        print(Fore.RED + "No orders found for this user.")
        conn.close()
        return

    total_sum = sum(order[5] for order in orders)
    bill_content = f"\n--- Bookstore Bill ---\n"

    for order in orders:
        bill_content += f"""
Date: {order[0]}
Category: {order[1]}
Book Name: {order[2]}
Quantity: {order[3]}
Price per Book: {order[4]}
Total Price: {order[5]}
-----------------------
"""

    bill_content += f"\nTotal Amount Payable: {total_sum}\n-----------------------"

    file_name = f"{user_phone}.txt"
    with open(file_name, "w") as file:
        file.write(bill_content)

    print(Fore.GREEN + f"Bill saved as {file_name}")

    send_whatsapp = input(Fore.LIGHTGREEN_EX + "Do you want the bill on your WhatsApp number? (yes/no): ").strip().lower()
    if send_whatsapp == "yes":
        send_whatsapp_message(user_phone, bill_content)

    conn.close()

# Fetch Book From Files portal;
def fetch_books_from_files():
    file_paths = {
        "General Knowledge": "General_Knowledge.txt",
        "Mythology": "Mythology.txt",
        "Social Science": "Social_science.txt"
    }
    
    books = []
    
    for category, file_path in file_paths.items():
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        book_name, quantity, _ = parts  # Extract book name and quantity
                        books.append((book_name, category, int(quantity)))
        except FileNotFoundError:
            print(Fore.RED + f"Warning: {file_path} not found.")
    
    return books

# Print Bar Chart: X-axis Book Name and Y-axis Quantity portal;
def Bar_chart():
    books = fetch_books_from_files()
    
    if not books:
        print(Fore.RED + "No books found in files.")
        return
    
    df = pd.DataFrame(books, columns=['Book Name', 'Category', 'Quantity'])
    categories = df['Category'].unique()
    
    fig, axes = plt.subplots(1, len(categories), figsize=(15, 5))
    
    if len(categories) == 1:
        axes = [axes]  # Ensure axes is iterable if there's only one category
    
    for ax, category in zip(axes, categories):
        category_df = df[df['Category'] == category]
        ax.bar(category_df['Book Name'], category_df['Quantity'], color='blue', width=0.2)
        ax.set_title(category)
        ax.set_xlabel("Book Name")
        ax.set_ylabel("Quantity")
    
    plt.tight_layout()
    plt.show()

# Print Pie Chart portal (Fetching book category data from database);
def Pi_chat():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='bookstore1')
        cursor = conn.cursor(buffered=True)
        # Query to get total quantity per category from the orders table
        query = "SELECT book_category, SUM(quantity) FROM orders GROUP BY book_category"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print(Fore.RED + "No data found in orders table for pie chart.")
            return

        categories = [row[0] for row in results]
        quantities = [row[1] for row in results]
        
        plt.figure(figsize=(8, 8))
        plt.pie(quantities, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Book Category Distribution")
        plt.legend(categories, title="Categories", loc="upper right")
        plt.show()
    except Exception as e:
        print(Fore.RED + f"An error occurred while generating pie chart: {e}")

# Main
while True:
    print(Fore.MAGENTA + Style.BRIGHT + "------Welcome--------")
    print(Fore.BLUE + "1. Admin\n2. User\n3. Exit")
    try:
        ch = int(input("Enter your choice: "))
        if ch == 1:
            admin()
        elif ch == 2:
            user()
        elif ch == 3:
            print(Fore.GREEN + "Exiting program.")
            break
        else:
            print(Fore.RED + "Invalid choice! Try again.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")
