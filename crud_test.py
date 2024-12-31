import mysql.connector
import datetime

# Konfigurasi koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Piang09@Secure!",
    database="Kelompok_CC"
)

cursor = db.cursor()

def create_user(username, password, account):
    created_at = datetime.datetime.now()
    cursor.execute("INSERT INTO users (username, password, account, created_at) VALUES (%s, %s, %s, %s)",
                   (username, password, account, created_at))
    db.commit()
    print(f"User {username} created successfully!")

def display_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    print("\nUsers in database:")
    print(f"{'ID':<5} {'Username':<15} {'Password':<20} {'Account':<25} {'Created At'}")
    print("-" * 80)
    
    for (id, username, password, account, created_at) in users:
        print(f"{id:<5} {username:<15} {password:<20} {account:<25} {created_at}")
    print("-" * 80)

def update_user(user_id, new_username, new_password, new_account):
    cursor.execute("UPDATE users SET username = %s, password = %s, account = %s WHERE id = %s",
                   (new_username, new_password, new_account, user_id))
    db.commit()
    print(f"User {user_id} updated successfully!")

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    print(f"User {user_id} deleted successfully!")

def menu():
    while True:
        print("\n--- CRUD Menu ---")
        print("1. Create User")
        print("2. Read Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            account = input("Enter account email: ")
            create_user(username, password, account)
        elif choice == '2':
            display_users()
        elif choice == '3':
            user_id = int(input("Enter the user ID to update: "))
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_account = input("Enter new account email: ")
            update_user(user_id, new_username, new_password, new_account)
        elif choice == '4':
            user_id = int(input("Enter the user ID to delete: "))
            delete_user(user_id)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

menu()

cursor.close()
db.close()
