cart = []  # --- List to hold items to buy ---- #

def additem(item: str):  # ---- Function to add items to cart
    """
    Function to add an item to the cart.

    Parameters:
    item (str): Item to be added to the cart.
    """
    if item:
        cart.append(item)
        print(f"{item} has been added to your cart.")
    else:
        print("Item cannot be an empty string.")

def removeitem(item: str):  # --- Function to remove an item from the cart ---- #
    """
    Function to remove an item from the cart.

    Parameters:
    item (str): Item to be removed from the cart.
    """
    if item:
        try:
            cart.remove(item)
            print(f"{item} has been removed from your cart.")
        except ValueError:
            print("Sorry, we could not remove that item.")
    else:
        print("Item cannot be an empty string.")

def showcart():  # ---- Function to reveal items in cart to the user ---- #
    """
    Function to show all the items in the cart.
    """
    if cart:
        for item in cart:
            print(f"=> {item}")
    else:
        print("Sorry, your cart is empty.")

def clearcart():  # ---- Measure to clear all items in the cart ---- #
    """
    Function to clear all items from the cart.
    """
    cart.clear()
    print("Your cart has been emptied.")
