import os
import pymongo
if os.path.exists("env.py"): # Checks for sensitive info stored in env.py
    import env

MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"

# Function to grab db data from MongoDB

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Couldn't connect to MongoDB: %s") % e

# Menu options that show in the terminal

def show_menu():
    print("")
    print("1. Add a record") # CRUD
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ") # ask user to choos an option
    return option

# Input prompts to a user when searching a record

def get_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found.")

    return doc

# Add a record

def add_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_color = input("Enter hair color > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_color": hair_color,
        "occupation": occupation,
        "nationality": nationality
      }

    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")

# Find a record

def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():  # for key value pairs in doc
            if k != "_id":  # if key isn't = to the id (we want to keep that hidden)
                print(k.capitalize() + ": " + v.capitalize())  # print the key val pairs in capitalized

# Edit a record

def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ") # keys's value will be changed to input after the > 

                if update_doc[k] == "": # if no changes are made to key
                    update_doc[k] = v   # value stays the same

        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")

# Delete a record

def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document deleted!")
            except:
                print("Error accessing the database")
        else:
            print("Document not deleted")

# Main loop to show in terminal

def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")

# Variables that get url, db and db's content + runs the loop function

conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()