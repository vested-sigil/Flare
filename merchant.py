from collections import namedtuple

class Order:
    """A class representing a single order.

    Attributes:
        items (list): The items in the order.
        customer (str): The customer who placed the order.
        status (str): The status of the order.
    """
    def __init__(self, items, customer, status):
        """Initializes an Order object.

        Args:
            items (list): The items in the order.
            customer (str): The customer who placed the order.
            status (str): The status of the order.
        """
        self.items = items
        self.customer = customer
        self.status = status

    def mark_completed(self):
        """Marks the order as completed."""
        self.status = "completed"

    def display(self):
        """Displays the details of the order."""
        print(f"Items: {self.items}")
        print(f"Customer: {self.customer}")
        print(f"Status: {self.status}")

def take_order(menu, customer_name):
    """Takes an order from a customer.

    Args:
        menu (namedtuple): The menu items and their categories.
        customer_name (str): The name of the customer placing the order.

    Returns:
        Order: The order placed by the customer.
    """
    def display_menu(menu):
        """Displays the menu options.

        Args:
            menu (namedtuple): The menu items and their categories.
        """
        print("Menu:")
        for i, category in enumerate(menu):
            print(f"{i+1}. {category.name}")

    def prompt_for_order(menu):
        """Prompts the user to select items from the menu.

        Args:
            menu (namedtuple): The menu items and their categories.

        Returns:
            list: The selected menu items.
        """
        order = []
        while True:
            # Display the menu
            display_menu(menu)

            # Prompt the user to select a category
            try:
                selection = int(input("Enter the number of the category you would like to order from (or 0 to finish): "))
            except ValueError:
                print("Invalid input. Please try again.")
                continue

            # Exit the loop if the user entered 0
            if selection == 0:
                break

            # Get the selected category
            try:
                category = menu[selection-1]
            except IndexError:
                print("Invalid selection. Please try again.")
                continue

            # Display the items in the selected category
            print(f"{category.name}:")
            for i, item in enumerate(category):
                print(f"{i+1}. {item}")

            # Prompt the user to select an item
            try:
                item_selection = int(input("Enter the number of the item you would like to order (or 0 to return to the main menu): "))
            except ValueError:
                print("Invalid input. Please try again.")
                continue

            # Return to the main menu if the

