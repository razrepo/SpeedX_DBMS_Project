import mysql.connector
import random
import time

mydb = mysql.connector.connect(
    host="localhost", user="root", password="raz12345", database="speedx"
)

mycursor = mydb.cursor()

while True:
    # start
    print("\nWelcome to Speed X!")

    print("Options:")
    print("1. Enter as admin")
    print("2. Enter as customer")
    print("3. Register as customer")
    print("4. Exit")
    print()
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":

        admin_password = input("Enter admin password: ")

        if admin_password != "admin123":
            print("Incorrect password. Access denied.")
            continue

        # Code for entering as admin
        print("Entering as admin...")
        # Add admin features here if needed

        while True:

            print("Options:")
            print("1. Product management")
            print("2. Category addition")
            print("3. Discount addition")
            print("4. Back")
            choicecust = input("Enter your choice (1/2/3/4): ")

            if choicecust == "4":
                print("Returning to main menu...")
                break

            elif choicecust == "1":  # product management
                print("Options:")
                print("1. Add product")
                print("2. Discontinue product")
                print("3. Update product price")

                choiceproduct = input("Enter your choice: ")

                if choiceproduct == "1":  # add product
                    product_name = input("Enter product name: ")
                    category_ID = input("Enter category ID: ")
                    product_desc = input("Enter product description: ")
                    product_price = input("Enter product price: ")
                    product_stock = input("Enter product stock: ")

                    stor_id = input("Which store to add this product to: ")

                    # Get the last product_ID from the product table
                    mycursor.execute("SELECT MAX(product_ID) FROM product")
                    last_product_id = mycursor.fetchone()[0]

                    new_product_id = last_product_id + 1 if last_product_id else 1

                    # Insert into product table
                    insert_product_query = "INSERT INTO product (product_ID, product_name, category_ID, product_desc, product_price, product_stock) VALUES (%s, %s, %s, %s, %s, %s)"
                    insert_product_values = (
                        new_product_id,
                        product_name,
                        category_ID,
                        product_desc,
                        product_price,
                        product_stock,
                    )

                    # Insert into store_inventory table
                    insert_inventory_query = "INSERT INTO store_inventory (store_ID, product_ID, quantity) VALUES (%s, %s, %s)"
                    insert_inventory_values = (stor_id, new_product_id, product_stock)

                    try:
                        # Insert product
                        mycursor.execute(insert_product_query, insert_product_values)
                        mydb.commit()

                        # Insert into store_inventory
                        mycursor.execute(
                            insert_inventory_query, insert_inventory_values
                        )
                        mydb.commit()

                        print("Product added successfully!")
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")

                elif choiceproduct == "2":  # discontinue product
                    product_name = input("Enter product name to discontinue: ")

                    # Update product_stock to zero in product table
                    update_product_query = (
                        "UPDATE product SET product_stock = 0 WHERE product_name = %s"
                    )
                    update_product_values = (product_name,)

                    # Update quantity and cost to zero in store_inventory
                    update_inventory_query = "UPDATE store_inventory SET quantity = 0, cost = 0 WHERE product_ID = (SELECT product_ID FROM product WHERE product_name = %s)"
                    update_inventory_values = (product_name,)

                    try:
                        # Update product stock
                        mycursor.execute(update_product_query, update_product_values)
                        mydb.commit()

                        # Update store_inventory
                        mycursor.execute(
                            update_inventory_query, update_inventory_values
                        )
                        mydb.commit()

                        print(f"{product_name} discontinued successfully!")
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")

                elif choiceproduct == "3":  # update product price
                    product_name = input("Enter product name to update price: ")
                    new_price = input("Enter new product price: ")

                    update_query = (
                        "UPDATE product SET product_price = %s WHERE product_name = %s"
                    )
                    update_values = (new_price, product_name)

                    try:
                        mycursor.execute(update_query, update_values)
                        mydb.commit()
                        print(f"{product_name} price updated successfully!")
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")

                else:
                    print("Invalid choice. Please enter a valid option.")

            elif choicecust == "2":  # category addition
                print("Adding a new category...")

                category_name = input("Enter category name: ")

                # Get the last category_ID from the category table
                mycursor.execute("SELECT MAX(category_ID) FROM category")
                last_category_id = mycursor.fetchone()[0]

                new_category_id = last_category_id + 1 if last_category_id else 1

                try:
                    # Insert into category table
                    insert_query = "INSERT INTO category (category_ID, category_name) VALUES (%s, %s)"
                    insert_values = (new_category_id, category_name)
                    mycursor.execute(insert_query, insert_values)
                    mydb.commit()
                    print(f"Category '{category_name}' added successfully!")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")

            elif choicecust == "3":  # discount addition
                print("Adding a new discount...")

                try:

                    # Fetch the last highest discount_ID and increment by 1
                    mycursor.execute("SELECT MAX(discount_ID) FROM discount FOR UPDATE")
                    last_discount_id = mycursor.fetchone()[0]
                    new_discount_id = last_discount_id + 1 if last_discount_id else 1

                    discount_name = input("Enter discount name: ")
                    category_ID = input("Enter category ID: ")
                    discount_percent = input("Enter discount percentage: ")
                    discount_code = input("Enter discount code: ")
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")

                    # Insert into discount table
                    insert_query = "INSERT INTO discount (discount_ID, category_ID, discount_name, discount_percent, discount_code, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    insert_values = (
                        new_discount_id,
                        category_ID,
                        discount_name,
                        discount_percent,
                        discount_code,
                        start_date,
                        end_date,
                    )
                    mycursor.execute(insert_query, insert_values)
                    mydb.commit()
                    print("Discount added successfully!")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")

            else:
                print("Invalid choice. Please enter a valid option.")

    elif choice == "2":  # Entering as customer

        customer_name = input("Enter your username: ")
        customer_password = input("Enter your password: ")

        try:
            mycursor.execute(
                "SELECT customer_ID FROM customer WHERE customer_name = %s AND customer_password = %s",
                (customer_name, customer_password),
            )
            result = mycursor.fetchone()

            if result:
                customer_ID = result[0]
                print("Login successful!")

                while True:
                    print("\nOptions:")
                    print("1. View all products")
                    print("2. View cart")
                    print("3. Add product to cart")
                    print("4. Order cart items")
                    print("5. Back")
                    choice = input("Enter your choice (1/2/3/4/5/6): ")

                    if choice == "5":
                        print("Returning to main menu...")
                        break

                    elif choice == "1":  # View all products
                        mycursor.execute("SELECT * FROM product")
                        products = mycursor.fetchall()

                        print("\nProducts:")
                        print(
                            "Product ID | Product Name            | Price | Stock | Category"
                        )
                        for product in products:
                            print(
                                f"{product[0]} | {product[1]:<25} | ${product[4]:<5} | {product[5]:<5} | {product[2]:<10}"
                            )

                    elif choice == "2":  # View cart
                        mycursor.execute(
                            "SELECT p.product_ID, p.product_name, c.quantity, c.cost FROM product p JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s",
                            (customer_ID,),
                        )
                        cart_items = mycursor.fetchall()

                        if cart_items:
                            print("\nYour Cart:")
                            print(
                                "Product ID | Product Name            | Quantity | Cost"
                            )
                            for item in cart_items:
                                print(
                                    f"{item[0]} | {item[1]:<25} | {item[2]:<8} | ${item[3]:<5}"
                                )
                        else:
                            print("Your cart is empty.")

                    elif choice == "3":  # Add product to cart
                        product_ID = input("Enter the ID of the product to add: ")
                        quantity = int(input("Enter the quantity: "))

                        # Check if the product exists and is in stock
                        mycursor.execute(
                            "SELECT * FROM product WHERE product_ID = %s AND product_stock >= %s",
                            (product_ID, quantity),
                        )
                        product = mycursor.fetchone()

                        if product:
                            cost = quantity * product[4]  # product_price
                            # Add product to cart
                            mycursor.execute(
                                "INSERT INTO cart (customer_ID, product_ID, quantity, cost) VALUES (%s, %s, %s, %s)",
                                (customer_ID, product_ID, quantity, cost),
                            )
                            mydb.commit()
                            print("Product added to cart successfully!")
                        else:
                            print("Error: Product not found or insufficient stock.")

                    elif choice == "4":  # Order cart items
                        mycursor.execute(
                            "SELECT p.product_ID, p.product_name, c.quantity FROM product p JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s",
                            (customer_ID,),
                        )
                        cart_items = mycursor.fetchall()

                        if cart_items:
                            print("\nOrdering cart items...")

                            order_status = "delivered"
                            partner_ID = random.randint(1, 10)

                            # Get the last order_ID from the order_ table
                            mycursor.execute("SELECT MAX(order_ID) FROM order_")
                            last_order_id = mycursor.fetchone()[0]

                            new_order_id = last_order_id + 1 if last_order_id else 1

                            # Insert into order_ table
                            insert_order_query = "INSERT INTO order_ (order_ID, customer_ID, order_status, partner_ID) VALUES (%s, %s, %s, %s)"
                            insert_order_values = (
                                new_order_id,
                                customer_ID,
                                order_status,
                                partner_ID,
                            )

                            try:
                                # Insert order
                                mycursor.execute(
                                    insert_order_query, insert_order_values
                                )
                                mydb.commit()

                                # Insert into order_items table
                                for item in cart_items:
                                    insert_order_items_query = "INSERT INTO Order_items (order_ID, product_ID, quantity) VALUES (%s, %s, %s)"
                                    insert_order_items_values = (
                                        new_order_id,
                                        item[0],  # product_ID
                                        item[2],  # quantity
                                    )
                                    mycursor.execute(
                                        insert_order_items_query,
                                        insert_order_items_values,
                                    )

                                    # Update product stock
                                    update_product_stock_query = "UPDATE product SET product_stock = product_stock - %s WHERE product_ID = %s"
                                    update_product_stock_values = (
                                        item[2],  # quantity
                                        item[0],  # product_ID
                                    )
                                    mycursor.execute(
                                        update_product_stock_query,
                                        update_product_stock_values,
                                    )

                                    # Update store_inventory
                                    update_store_inventory_query = "UPDATE store_inventory SET quantity = quantity - %s WHERE product_ID = %s"
                                    update_store_inventory_values = (
                                        item[2],  # quantity
                                        item[0],  # product_ID
                                    )
                                    mycursor.execute(
                                        update_store_inventory_query,
                                        update_store_inventory_values,
                                    )

                                mydb.commit()
                                print("Order confirmed.")

                                # Simulate payment processing
                                print("Payment in process...")
                                time.sleep(2)

                                print("\nPayment processed.")
                                print("Options:")
                                print("1. Purchase")
                                print("2. Deny")
                                payment_choice = input("Enter your choice (1/2): ")

                                if payment_choice == "1":  # Purchase
                                    print("Purchase completed.")
                                    print("Thank you for shopping with us!")

                                    # Remove ordered items from cart
                                    mycursor.execute(
                                        "DELETE FROM cart WHERE customer_ID = %s",
                                        (customer_ID,),
                                    )
                                    mydb.commit()

                                elif payment_choice == "2":  # Deny
                                    print("Order denied.")
                                    print("Items remain in your cart.")
                                else:
                                    print("Invalid choice. Order denied.")

                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                        else:
                            print("Your cart is empty.")

                    else:
                        print("Invalid choice. Please enter a valid option.")
            else:
                print("Incorrect username or password. Access denied.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    elif choice == "3":  # Register as customer
        customer_name = input("Enter your username: ")
        customer_password = input("Enter your password: ")
        contact_number = input("Enter your contact number: ")
        customer_address = input("Enter your address: ")
        customer_email_id = input("Enter your email ID: ")
        customer_pincode = input("Enter your pincode: ")

        try:
            # Get the last customer_ID from the customer table
            mycursor.execute("SELECT MAX(customer_ID) FROM customer")
            last_customer_id = mycursor.fetchone()[0]

            new_customer_id = last_customer_id + 1 if last_customer_id else 1

            # Insert into customer table
            insert_query = "INSERT INTO customer (customer_ID, customer_name, customer_password, contact_number, customer_address, customer_email_id, customer_pincode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            insert_values = (
                new_customer_id,
                customer_name,
                customer_password,
                contact_number,
                customer_address,
                customer_email_id,
                customer_pincode,
            )
            mycursor.execute(insert_query, insert_values)
            mydb.commit()
            print("Registration successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    elif choice == "4":  # Exit
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please enter a valid option.")
