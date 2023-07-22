# -*- coding: utf-8 -*-

import hashlib
import json
from datetime import datetime

def read_json_file():
    """Reads a JSON file.
    Returns: A data list of dictionaries."""
    filename = "contacts.json"
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def save_json_file(data:list):
    """Saves a JSON file."""
    filename = "contacts.json"
    with open(filename, "w") as f:
        json.dump(data, f)

def view_all_contacts(contacts) -> list:
    """Displays all contacts list order by lastname."""
    # Print the contacts.
    if len(contacts) <= 0:
        print("No results found.")
    elif len(contacts) == 1:
        print("1 result found.")
        print("---") 
        show_contact_detail(contacts[0])
    else:
        print(f"{len(contacts)} results found.")
        print("---")        
        print(f"# --  Name  --{' '*41}--  Phone  --")
        for i in range(len(contacts)):
            print(f"{i+1}. {show_contact(contacts[i])}")
        
def show_contact(contact):
    name = contact['name'] + " " + contact['lastname']
    phone = contact['phone']
    show_format = name + " "*(50-len(name)) + "| " + phone + " |"
    return show_format

def show_contact_detail(contact:dict):
    print(f"{contact['name']} {contact['lastname']}")
    print(contact["phone"])
    print(contact["email"])
    print(contact["occupation"])
    print(contact["birth"])
    print(f"{contact['city']}, {contact['country']}")
    print(f"ID: {contact['id']}")
    
def search_contact() -> tuple:
    """Displays filtered contacts list.
    Returns:
        A tuple with filtered list of contacts and how many are.
    """
    go_back = False
    matching_values = list()
    while True:
        contacts = read_json_file()
        search_option = search_menu()
        if search_option == "":
            go_back = True
            break
        criteria = {search_option: input(f"Input {search_option} value: ")}
        # Create a set of all the values that match the criteria.
        for key, value in criteria.items():
            for contact in contacts:
                if value.lower() in contact[key].lower():
                    matching_values.append(contact)
        # Return the list of contacts that match the criteria.
        break
    return matching_values,go_back

def search_contact_by_id(contact_id):
    contacts = read_json_file()
    matching_values = list()
    for contact in contacts:
        if contact_id.lower() == contact["id"].lower():
            matching_values.append(contact)
    return matching_values

def hash(contact):
    """Hashes a contact's name and phone number.
    Args:
        contact: A dictionary containing the contact's name and phone number.
    Returns:
        A hash of the contact's name and phone number.
    """
    # Convert the contact's name and phone number to a string.
    contact_string = str(f"{contact['lastname']} {contact['name']} {contact['phone']}")
    # Use a hash function to convert the contact's information into a hash.
    contact_hash = hashlib.sha256(contact_string.encode()).hexdigest()
    # Return the contact hash.
    return contact_hash[:8]

def generate_contact_id(contact):
    """Generates a unique ID for a contact.
    Args:
        contact: A dictionary containing the contact's information.
    Returns:
        A unique ID for the contact.
    """
    # Use a hash function to convert the contact's information into a unique ID.
    contact_id = hash(contact)
    # Return the contact ID.
    return contact_id

        
def add_contact():
    """Creates a new contact and adds it to the data list."""
    contacts = read_json_file()
    new_data = {
        "name": input("Enter name: "),
        "lastname": input("Enter lastname: "),
        "birth": input("Enter the birth date: "),
        "email": input("Enter the email: "),
        "phone": input("Enter the phone number: "),
        "occupation": input("Enter the occupation: "),
        "city": input("Enter current city location: "),
        "country": input("Enter current country location: "),
    }
    new_data["id"] = generate_contact_id(new_data)
    contacts.append(new_data)
    save_json_file(contacts)
    print("Contact added.")
    
def edit_contact():
    """Edits a contact from the JSON file."""
    while True:
        print("---")
        print("To edit a contact, you need the id.")
        print("1. Enter the contact id.")
        print("2. Search contact.")
        print("0. Back to main menu.")
        print("---")
        choice = input("Enter your choice: ")
        # Validate the user's choice.
        while choice not in ["1", "2", "0"]:
            print("Invalid choice.")
            choice = input("Enter your choice: ")
        # Perform the selected action.
        if choice == "1":
            contact_id = input("Enter contact id: ")
            while validate_id(contact_id) == False:
                print("Invalid format id.")
                choice = input("Enter contact id: ")
            contact_list = search_contact_by_id(contact_id)
            if len(contact_list) == 1:
                new_contact_data = edit_menu(contact_list[0])
                update_contact(read_json_file(),contact_id,new_contact_data)
                break
            else:
                print("Contact not found.")
        
        elif choice == "2":
            print("Search contact...")
            pass
        
        elif choice == "0":
            return
        
        input("Press enter to continue...")
        
def validate_id(contact_id:str) -> bool:
    if len(contact_id) != 8:
        return False
    return True
        
def delete_contact(data, id):
    """Deletes a person from the data list."""
    for index, row in enumerate(data):
        if row["id"] == id:
            del data[index]
            break

def edit_menu(contact:dict) -> dict:
    """Displays one by one the fields to edit the contact.
       Build a new data dictionary.
    Returns:
        A dictionary with the new contact data.
    """
    # Display the menu.
    print("Fill in only the fields to update.")
    name = input("Enter name: ")
    if name == "":
        name = contact["name"]
    lastname = input("Enter lastname: ")
    if lastname == "":
        lastname = contact["lastname"]
    birth = input("Enter the birth date: ")
    if birth == "":
        birth = contact["birth"]
    email = input("Enter the email: ")
    if email == "":
        email = contact["email"]
    phone = input("Enter the phone number: ")
    if phone == "":
        phone = contact["phone"]
    occupation = input("Enter the occupation: ")
    if occupation == "":
        occupation = contact["occupation"]
    city = input("Enter current city location: ")
    if city == "":
        city = contact["city"]
    country = input("Enter current country location: ")
    if country == "":
        country = contact["country"]
        
    new_data = {
        "name" : name,
        "lastname": lastname,
        "birth": birth,
        "email": email,
        "phone": phone,
        "occupation": occupation,
        "city": city,
        "country": country,
        "id": contact["id"]
    }
    
    return new_data
        
def update_contact(contact_list,contact_id,new_contact_data):
    for contact in contact_list:
        if contact["id"] == contact_id:
        # Update the contact's data.
            for key, value in new_contact_data.items():
                contact[key] = value
    # Return the updated list of contacts.
    save_json_file(contact_list)
    print("Contact updated.")

def search_menu():
    """Displays a menu of fields options."""
    # Display the search menu.
    print("---")
    print("Wich field would you like to filter?")
    print("1. Name")
    print("2. Lastname")
    print("3. Email address")
    print("4. Phone number")
    print("0. Back to main menu")
    print("---")
    # Get the user's choice.
    choice = input("Enter your choice: ")
    # Validate the user's choice.
    while choice not in ["1", "2", "3", "4", "0"]:
        print("Invalid choice.")
        choice = input("Enter your choice: ")
    # Perform the selected action.
    if choice == "1":
        print("Filtering by name...")
        return "name"
    elif choice == "2":
        print("Filtering by lastname...")
        return "lastname"
    elif choice == "3":
        print("Filtering by email address...")
        return "email"
    elif choice == "4":
        print("Filtering by phone number...")
        return "phone"
    elif choice == "0":
        return ""
    input("Press enter to continue...")

def main_menu():
    print("Welcome to the contact app.")
    while True:
        # Display the main menu.
        print("---")
        print("What would you like to do?")
        print("1. View all contacts")
        print("2. Search a contact")
        print("3. Add a contact")
        print("4. Edit a contact")
        print("5. Delete a contact")
        print("0. Exit")
        print("---")
        # Get the user's choice.
        choice = input("Enter your choice: ")
        print("---")
        # Validate the user's choice.
        while choice not in ["1", "2", "3", "4", "5", "0"]:
            print("Invalid choice.")
            choice = input("Enter your choice: ")
            print("---")
            
        # Perform the selected action.
        if choice == "1":
            print("Contact List...")
            view_all_contacts(read_json_file())
            
        elif choice == "2":
            print("Searching contacts...")
            contacts_list,go_back = search_contact()
            if go_back == False:
                view_all_contacts(contacts_list)
                
        elif choice == "3":
            print("Creating new contact...")
            add_contact()
            
        elif choice == "4":
            print("Editing contact...")
            edit_contact()
            
        elif choice == "5":
            print("Deleting contact...")
            delete_contact()
            
        elif choice == "0":
            exit()
            
        input("Press enter to continue...")
        
main_menu()