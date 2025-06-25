import sys
import getpass
from hashlib import sha256
from db import DataBase
# Helper function to hash passwords
def hashString(input_string):
    return sha256(input_string.encode()).hexdigest()

def add_admin_user():

    while True:
        user_id = input("Enter user id (email): ")
        confirm_user_id = input("Re-Enter user id (email): ")

        if user_id.strip().lower() == confirm_user_id.strip().lower():

            while True:
                password = getpass.getpass("Enter your password: ")
                confirm_password = getpass.getpass("Re-Enter your passsword: ")

                if password == confirm_password:
                    db = DataBase()
                    result = db.add_admin(
                        user_id,
                        hashString(password),
                        1
                    )
                    if result:
                        print("Account Creation Successfull")
                        break
                else:
                    print("Passwords do not match please try again")
            break
        else:
            print("User IDs are not emails or do not match please try again ")

def help():
    print("""
List of available commands:

--help : toggles the help menu
--add-admin : add a new admin user to the server
          
""")
    
mappings = {
    "--add-admin":add_admin_user,
    "--help":help
}

if len(sys.argv) == 2:
    for i in mappings:
        if i == sys.argv[1]:
            mappings[i]()
else:
    print("Usage: python3 interact.py <COMMAND>")