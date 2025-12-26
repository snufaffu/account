import hashlib
import sqlite3
import secrets

account_data = sqlite3.connect('main.db') 
cursor = account_data.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        password TEXT,
        salt INTEGER
    )
''')

def input_username():
    username = input("Hello user! What would you like your username to be? ")      
    confirmation = input(f"Is {username} the name you would like to choose? (Y/N) ")
    flag = confirm_username(confirmation)
    flag2 = check_duplicate_username(username)
    if flag2 == True: #dupe check
        print("Sorry, this username is taken.")
        return input_username()
    if flag == True:
        return username
    else:
       return input_username()

def confirm_username(confirm_text):
    if confirm_text in ["yes", "y", 'Y']:
        return True
    elif confirm_text in ["no", "n", 'N']:
        return False

def check_duplicate_username(username):
    cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
    result = cursor.fetchone()
    return result is not None
    
def input_password():
    password = input("Please use at least 8 characters. ")
    if len(password) < 8:
        print("Please use at least 8 characters!")
        return input_password()
    confirmation = input("Please type your password in again. ")
    flag = confirm_password(password, confirmation)
    if flag == True:
        return password
    else:
        return input_password()

def confirm_password(password, confirmation):
    if password == confirmation:
        return True
    else:
        print("Passwords didn't match!")
        return False

    
username = input_username()
print("The next step is to create a password!")
password = input_password()
print(f"Success! Welcome to the platform, {username}")

salt = secrets.randbelow(999999)
salted_password = str(salt) + password
hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()

userdata = (username, hashed_password, salt)
cursor.execute('INSERT INTO users (name, password, salt) VALUES (?, ?, ?)', userdata)
account_data.commit()
account_data.close()