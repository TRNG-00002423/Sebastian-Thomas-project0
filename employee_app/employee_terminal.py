from models.users import User

import os
import requests

BASE_URL = "http://127.0.0.1:5050"

def submit_expense(user:User):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'='*25}\nExpense Report Submission\n{'='*25}\n")
    while True:
        amount = input("Please enter the amount of the expense (or q to exit): $")
        if amount.casefold() == 'q':
            return
        try:
            amount = int(amount)
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
        
    description = input("Please enter the description of the expense: ")
    date = input("Please enter the date of the expense: ") 
    
    payload = {
        "user_id": user.id,
        "amount": amount,
        "description": description,
        "date": date
    }

    expense = (requests.post(f"{BASE_URL}/expenses", json=payload)).json()
    payload = {
        "expense_id": expense['id'],
        "status": "pending",
        "reviewer": None,
        "comment": "",
        "review_date": ""
    }

    requests.post(f"{BASE_URL}/approvals", json=payload)
    print("\n")

def get_all_non_pending_user(user:User): 
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{'='*25}\n{user.username}'s Approved or Denied Expense Reports\n{'='*25}\n")
    response = requests.get(f"{BASE_URL}/expenses/user/{user.id}/history")
    if response.status_code != 200:
        print(f"Could not retrieve history: {response.text}")
        return
    non_pending_expenses = response.json()
    for expense in non_pending_expenses:
        approval_response = requests.get(f"{BASE_URL}/approvals/expense/{expense['id']}")
        if approval_response.status_code == 200:
            status = approval_response.json().get('status', 'Unknown')
        else:
            status = "Unknown"
        print(f"ID: {expense['id']} | Amount: ${expense['amount']} | Desc: {expense['description']} | Status: {status}")
    print("\n")

    input("Press any key to go back to the main menu...")

def get_all_expenses(user:User):
    #clears the console, regardless of it is in windows or mac/linux
    os.system('cls' if os.name == 'nt' else 'clear')
    response = requests.get(f"{BASE_URL}/expenses/user/{user.id}")
    if response.status_code != 200:
        print(f"Could not retrieve history: {response.text}")
        return
    print(f"{'='*25}\n{user.username.capitalize()}'s Expense Reports\n{'='*25}\n")
    expenses = response.json()
    for expense in expenses:
        approval_response = requests.get(f"{BASE_URL}/approvals/expense/{expense['id']}")
        if approval_response.status_code == 200:
            status = approval_response.json().get('status', 'Unknown')
        else:
            status = "Unknown"
        print(f"ID: {expense['id']} | Amount: ${expense['amount']} | Desc: {expense['description']} | Status: {status}")
    print("\n")
    input("Press any key to go back to the main menu...")

def edit_expense(user:User):
    os.system('cls' if os.name == 'nt' else 'clear')
        
    print(f"{'='*25}\nEdit Expense Report\n{'='*25}\n")
    while True:
        user_input = input("Please enter the expense id you would like to edit (press q to exit): ")
        if user_input == 'q':
            return
        try:
            id = int(user_input)
            expense_response = requests.get(f"{BASE_URL}/expenses/{id}")
            if expense_response.status_code != 200:
                print("Expense does not exist. Please enter a valid expense.\n")
                continue
            expense = expense_response.json()
            approval_response = requests.get(f"{BASE_URL}/approvals/expense/{id}")
            if approval_response.status_code == 200:
                approval = approval_response.json()
                status = approval.get('status', 'pending')
            else:
                status = 'pending'

            if expense['user_id'] != user.id:
                print("Invalid operation. You can only edit your own expense reports\n")
            elif status != "pending":
                print("Invalid operation. You can only edit pending expense reports\n")
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")
    while True:
        amount = input(f"Please enter the new amount (Current: ${expense['amount']}): ")
        try:
            if amount == "":
                break
            amount = int(amount)
            expense['amount'] = amount
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

    description = input(f"Please enter the new description (Current: {expense['description']}): ").strip()
    date = input(f"Please enter the new date (Current: {expense['date']}): ").strip()
    expense['description'] = description or expense['description']
    expense['date'] = date or expense['date']
    
    payload = {
        "user_id": user.id,
        "amount": expense['amount'],
        "description": expense['description'],
        "date": expense['date']
    }

    response = requests.put(f"{BASE_URL}/expenses/{id}", json=payload)

    if response.status_code != 200:
        print("Expense could not be updated.")

def delete_expense(user:User):
    os.system('cls' if os.name == 'nt' else 'clear')
        
    print(f"{'='*25}\nRemove Expense Report\n{'='*25}\n")
    while True:
        user_input = input("Please enter the expense id you would like to remove (press q to exit): ").strip().lower()
        if user_input == 'q':
            return
        try:
            id = int(user_input)
            expense_response = requests.get(f"{BASE_URL}/expenses/{id}")
            if expense_response.status_code != 200:
                print("Expense does not exist. Please enter a valid expense.\n")
                continue
            expense = expense_response.json()
            if expense['user_id'] != user.id:
                print("Invalid operation. You can only delete your own expense reports\n")
            else:
                delete_response = requests.delete(f"{BASE_URL}/expenses/{id}")
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")



def dashboard(user:User):
    running_dash = True
    print(f"\nWelcome Employee {user.username.capitalize()}!")

    while running_dash:
        print("\n1. Submit a new expense report")
        print("2. View the status of all your submitted expense reports")
        print("3. Edit a pending expense report")
        print("4. Delete a pending expense report")
        print("5. View a history of all your approved or denied expense reports")
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
        
        if user_command == 1:#create
            submit_expense(user)

        elif user_command == 2:
            get_all_expenses(user)

        elif user_command == 3:
            edit_expense(user)

        elif user_command == 4:
            delete_expense(user)

        elif user_command == 5:
            get_all_non_pending_user(user)

        elif user_command == 6:
            running_dash = False

        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Welcome to the Employee App!")

    running_main = True

    while running_main:
        user_input = input("Please type 1 to login or 2 to exit: ")
        try:
            user_command = int(user_input)
            if user_command < 1 or user_command > 2:
                print("Invalid operation. Please enter 1 or 2.")
                continue
        except ValueError as e:
            print("Invalid input. Please enter a valid number.")
            continue
        
        if user_command == 1:
            
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            package = {
                "username": username,
                "password": password
            }
            login_request = requests.post(f"{BASE_URL}/users/login", json=package)

            if login_request.status_code == 200:
                raw_user_data = login_request.json()
                if raw_user_data['role'] == "Manager":
                    print("Only employee logins permitted")
                    continue
                logged_in_user = User(
                    id=raw_user_data['id'],
                    username=raw_user_data['username'],
                    password=raw_user_data['password'],
                    role=raw_user_data['role']
                )
                
                dashboard(logged_in_user)
                continue
            else:
                print("Username or password not valid, Please try again!")
                continue
        if user_command == 2:
            print("Goodbye!")
            running_main = False
    

if __name__ == "__main__":
    main()
