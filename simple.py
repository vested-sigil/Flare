import requests
import os
import json
import midcrud  # Importing midcrud module

# Load environment variables
BACK4APP_APP_ID = os.getenv('BACK4APP_APP_ID')
BACK4APP_REST_API_KEY = os.getenv('BACK4APP_REST_API_KEY')
BACK4APP_SERVER_URL = "https://parseapi.back4app.com"  # Update if different

# Headers for Back4App API
HEADERS = {
    "X-Parse-Application-Id": BACK4APP_APP_ID,
    "X-Parse-REST-API-Key": BACK4APP_REST_API_KEY,
    "Content-Type": "application/json"
}

# Function to get classes from Back4App
def get_classes():
    response = requests.get(f"{BACK4APP_SERVER_URL}/schemas", headers=HEADERS)
    return response.json().get('results', [])



def wake_server():
    response = requests.get(f"{BACK4APP_SERVER_URL}/functions/index", headers=HEADERS)
    return response.json()


# Interactive menu functions
def choose_class():
    classes = get_classes()
    print("Choose a class:")
    for i, cls in enumerate(classes, 1):
        print(f"{i}. {cls['className']}")
    choice = int(input("Enter your choice: "))
    return classes[choice - 1]['className']

def main_menu():
    print("Select an action:")
    print("1. New (Create)")
    print("2. View (Read)")
    print("3. Edit (Update)")
    print("4. Junk (Delete)")
    print("5. Wake Server")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    return choice

def get_params():
    params = {}
    while True:
        key = input("Enter parameter key (or 'done' to finish): ")
        if key == 'done':
            break
        value = input(f"Enter value for {key}: ")
        params[key] = value
    return params

def wake_server():
    # Implement the logic to wake the server
    print("Waking up the server...")
    # Add any necessary logic here
    return "Server is awake."

def main():
    # Auto wake server
    wake_server()

    while True:
        choice = main_menu()
        if choice == '1':
            className = choose_class()
            params = get_params()
            response = midcrud.create(className, params)
        elif choice == '2':
            className = choose_class()
            query = input("Enter query: ")
            response = midcrud.read(className, query)
        elif choice == '3':
            className = choose_class()
            objectId = input("Enter object ID: ")
            updates = get_params()
            response = midcrud.update(className, objectId, updates)
        elif choice == '4':
            className = choose_class()
            objectId = input("Enter object ID: ")
            response = midcrud.delete(className, objectId)
        elif choice == '5':
            response = wake_server()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        print("Response:", response)

if __name__ == "__main__":
    main()

