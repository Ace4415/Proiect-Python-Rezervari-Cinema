from auth import hashing as hash
from auth import userdb as user

user.init_db()
DEFAULT_ADMIN_PASS = "admin123"
admin_hash = hash.hash_passwd(DEFAULT_ADMIN_PASS)
user.create_default_admin(admin_hash)


case = input("Enter case: 1 to login, 2 to create user: ")
if case == "1":
    username = input("Enter username: ")
    password = input("Enter password: ")
    auth_data = user.get_user_auth_data(username)

    if auth_data:
        stored_hash, is_admin, must_change_password = auth_data
        if hash.check_passwd(password, stored_hash):
            print(f"Login successful! Welcome {username}.")

            if is_admin:
                if must_change_password:
                    new_passwd = input("Admin password is default, enter a new password: ")
                    user.update_password(username, hash.hash_passwd(new_passwd))
            else:
                print("Logged in as client")
        else:
            print("Invalid username or password")
    else:
        print("Invalid username or password")
elif case == "2":
    username = input("Enter username: ")
    password = input("Enter password: ")
    if user.create_user(username, hash.hash_passwd(password)):
        print("User created successfully")
    else:
        print("User already exists")