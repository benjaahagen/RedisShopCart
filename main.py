def main():
    done = False  # --- Loop switch ---- #
    print("Welcome to our store!")

    while not done:
        print("What action would you like to perform?")
        ans = input("\n** Quit\n** Add\n** Remove\n** Show\n** Clear:\n ").title()

        if ans == "Quit":
            print("Thanks for shopping with us.")
            if cart:
                print("\nHere are the items in your cart.")
                showcart()
            done = True
        elif ans == "Add":
            item = input("What item would you like to add? ").title()
            additem(item)
        elif ans == "Remove":
            showcart()
            item = input("What would you like to remove? ").title()
            removeitem(item)
        elif ans == "Show":
            print("Here is your cart:")
            showcart()
        elif ans == "Clear":
            clearcart()
        else:
            print("I'm sorry, I didn't understand that.")

if __name__ == '__main__':
    main()
