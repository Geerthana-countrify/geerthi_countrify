import logging
logging.basicConfig(filename='customer_details.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

customer_list = []
def add_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    phone = input("Enter customer phone number: ")
    customer = {
        "Name": name,
        "Email": email,
        "Phone": phone
    }
    customer_list.append(customer)
    print("Customer details added successfully!\n")
    logging.info(f"Added customer: {customer}")

def display_customers():
    if not customer_list:
        print("No customer details available.")
    else:
        print("Customer Details:")
        for idx, customer in enumerate(customer_list, start=1):
            print(f"Customer {idx}:")
            for key, value in customer.items():
                print(f"{key}: {value}")
            print()
    logging.info("Displayed customer details")

while True:
    print("Options:")
    print("1. Add Customer")
    print("2. Display Customers")
    print("3. Quit")
    
    choice = input("Select an option (1/2/3): ")
    logging.info(f"User chose option {choice}")
    
    if choice == '1':
        add_customer()
    elif choice == '2':
        display_customers()
    elif choice == '3':
        print("Goodbye!")
        logging.info("Program exited")
        break
    else:
        print("Invalid choice. Please select a valid option (1/2/3).")
        logging.warning(f"Invalid choice: {choice}")


# a1 = ServiceRegistry["CATALOG"]["uow"]
# print(a1)
# a2 = catalog_service.uow
# print(a2)
