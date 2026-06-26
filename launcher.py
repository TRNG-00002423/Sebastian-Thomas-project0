import subprocess
import os
programs = {
    1: ["python", "employee_app/employee_terminal.py"],
    2: ["mvn", "-q", "-f", "manager_app/pom.xml", "exec:java"],
}

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    choice = input("1. Employee App\n""2. Manager App\n""Choice: ")
    try:
        choice = int(choice)
        if choice == 1 or choice == 2:
            subprocess.run(["python", "employee_app/db/seed.py"])
            os.system('cls' if os.name == 'nt' else 'clear')
            subprocess.run(programs[choice])
        else:
            print("\nInvalid input. Please enter a valid number.")

    except ValueError:
            print("\nInvalid input. Please enter a valid number.")
