contacts=[]

def add_contact(name, phone, email):
    contact = {
        'name': name,
        'phone': phone,
        'email': email
    }
    contacts.append(contact)
    print(f"Contact {name} added successfully.\n")

def view_contacts():
    if not contacts:
        print("No contacts found.\n")
        return
    print("\n======Contact List======\n")

    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")
    print("\n========================\n")

def search_contact(search_name):
    for contact in contacts:
        if contact['name'].lower() == search_name.lower():
            print(f"Contact found: Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}\n")
            return
    print(f"No contact found with the name: {search_name}\n")

def delete_contact(delete_name):
    for contact in contacts:
        if contact['name'].lower() == delete_name.lower():
            contacts.remove(contact)
            print(f"Contact {delete_name} deleted successfully.\n")
            return
    print(f"No contact found with the name: {delete_name}\n")

def main():
    while True:
        print("Contact List Application")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email address: ")
            add_contact(name, phone, email)
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            search_name = input("Enter the name to search: ")
            search_contact(search_name)
        elif choice == '4':
            delete_name = input("Enter the name to delete: ")
            delete_contact(delete_name)
        elif choice == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()