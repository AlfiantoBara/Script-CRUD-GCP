import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.Certificate('/home/alfiantoteofilusbara/serviceAccountKey.json') 
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_last_user_id():
    doc_ref = db.collection('user_ids').document('last_id')
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()['last_id']
    else:
        return 0

def update_last_user_id(new_id):
    doc_ref = db.collection('user_ids').document('last_id')
    doc_ref.set({
        'last_id': new_id
    })

def get_available_id():
    users_ref = db.collection('users')
    docs = users_ref.stream()

    existing_ids = []
    for doc in docs:
        existing_ids.append(int(doc.id))

    max_id = max(existing_ids) if existing_ids else 0
    for i in range(1, max_id + 1):
        if i not in existing_ids:
            return i
    return max_id + 1  

def create_user(username, password, account):
    new_user_id = get_available_id()  

    created_at = datetime.datetime.now()
    user_ref = db.collection('users').document(str(new_user_id))
    user_ref.set({
        'username': username,
        'password': password,
        'account': account,
        'created_at': created_at
    })

    print(f"User {username} created successfully with ID: {new_user_id}")

def read_users():
    users_ref = db.collection('users')
    docs = users_ref.stream()

    print("\nUsers in Firestore:")
    print(f"{'ID'.ljust(20)} {'Username'.ljust(20)} {'Password'.ljust(20)} {'Account'.ljust(30)} {'Created At'}")
    print("-" * 90)
    for doc in docs:
        user = doc.to_dict()
        print(f"{doc.id.ljust(20)} {user['username'].ljust(20)} {user['password'].ljust(20)} {user['account'].ljust(30)} {user['created_at']}")
    print("-" * 90)

def update_user(user_id, new_username, new_password, new_account):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'username': new_username,
        'password': new_password,
        'account': new_account
    })
    print(f"User {user_id} updated successfully!")

def delete_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()
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
            read_users()
        elif choice == '3':
            user_id = input("Enter the user ID to update: ")
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_account = input("Enter new account email: ")
            update_user(user_id, new_username, new_password, new_account)
        elif choice == '4':
            user_id = input("Enter the user ID to delete: ")
            delete_user(user_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
