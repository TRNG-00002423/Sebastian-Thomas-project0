def validate_login(username, password):
    # TODO: finish this logic
    return True

def dashboard(username):
    running_dash = True
    print(f"\nWelcome Employee {username}!")

    while running_dash:
        print("\n1. Submit a new expense report")
        print("2. View the status of your submitted expense reports")
        print("3. Edit a pending expense report")
        print("4. Delete a pending expense report")
        print("5. View a history of all approved and denied expense reports")
        print("6. Logout")

        user_input = input("Please select an option: ")
        try:
            user_command = int(user_input)
            if user_command < 1 or user_command > 6:
                print("Invalid operation. Please enter a valid option.")
                continue
        except ValueError as e:
            print("\nInvalid input. Please enter a valid number.")
            continue
        
        if user_command == 1:
            # TODO: implement logic to submit a new expense report
            pass
        if user_command == 2:
            # TODO: implement logic to view the status of your submitted expense reports
            pass
        if user_command == 3:
            # TODO: implement logic to edit a pending expense report
            pass
        if user_command == 4:
            # TODO: implement logic to delete a pending expense report
            pass
        if user_command == 5:
            # TODO: implement logic to view a history of all approved and denied expense reports
            pass
        if user_command == 6:
            running_dash = False

def main():
    print("Welcome to the Employee App!")

    running_main = True

    while running_main:
        user_input = input("Please type 1 to login or 2 to exit: ")
        try:
            user_command = int(user_input)
            if user_command < 1 or user_command > 2:
                print("Invalid operation. Please enter 1 or 2.")
        except ValueError as e:
            print("Invalid input. Please enter a valid number.")
        
        if user_command == 1:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if validate_login(username,password):
                dashboard(username)
        if user_command == 2:
            print("Goodbye!")
            running_main = False
    

if __name__ == "__main__":
    main()