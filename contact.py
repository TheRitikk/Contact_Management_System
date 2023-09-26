import tkinter as tk
from tkinter import ttk  # Import ttk for Treeview
from tkinter import messagebox
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Contact_Management"]
mycol = mydb["Contact"]

# Function to validate number_entry to allow only numeric input
def validate_number_input(P):
    if P.isdigit() or P == "":
        return True
    else:
        return False

def save_contact():
    name = name_entry.get().lower()
    number = number_entry.get()
    
    # Check if name or number is blank
    if not name or not number:
        messagebox.showerror("Error", "Name or number cannot be blank.")
        return
    
    existing_document = mycol.find_one({"$or": [{"name": name}, {"number": number}]})
    if existing_document:
        if existing_document.get("name") == name:
            messagebox.showerror("Error", "Name already exists.")
        if existing_document.get("number") == number:
            messagebox.showerror("Error", "Number already exists.")
    else:
        mydict = {"name": name, "number": number}
        mycol.insert_one(mydict)
        messagebox.showinfo("Success", "Contact saved")
        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)

def show_contact():
    # Clear existing data in the Treeview
    for item in contact_tree.get_children():
        contact_tree.delete(item)

    # Retrieve all contacts from the database and sort them by name
    contacts = list(mycol.find({}, {"_id": 0}))
    contacts.sort(key=lambda x: x["name"].lower())  # Sort by name in a case-insensitive manner

    # Insert sorted data into the Treeview
    for contact in contacts:
        name = contact["name"]
        name = name.capitalize()
        number = contact["number"]

        # Add values to the Treeview with anchor=center to center-align them
        contact_tree.insert("", "end", values=(name, number), tags=("centered", "centered"))

    # Configure the Treeview column to center-align the values
    contact_tree.tag_configure("centered", anchor="center")

def delete_contact():
    number_to_delete = delete_entry.get()
    existing_document = mycol.find_one({"number": number_to_delete})
    if existing_document:
        mycol.delete_one({"number": number_to_delete})
        messagebox.showinfo("Success", "Number Successfully Deleted")
    else:
        messagebox.showinfo("Error", "Number not find")
    
    delete_entry.delete(0, tk.END)
    show_contact()

def update_contact():
    hide_all()
    option_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
    number_radio.grid(row=3, column=0, columnspan=4)
    name_radio.grid(row=4, column=0, columnspan=4, padx=10, pady=5)
    old_label.grid(row=5, column=1)
    old_entry.grid(row=5, column=2,columnspan=2, padx=10, pady=5)   
    new_label.grid(row=6, column=1)
    new_entry.grid(row=6, column=2,columnspan=2,  pady=5) 
    update_button.grid(row=7, column=1, columnspan=2,  pady=5)

def perform_update(option, old_value, new_value):
    if option == "name":
        existing_document = mycol.find_one({"name": old_value})
        if existing_document:
            mycol.update_one({"name": old_value}, {"$set": {"name": new_value}})
            messagebox.showinfo("Success", "Name Successfully Updated")
        else:
            messagebox.showinfo("Error", "Name not find")
    elif option == "number":
        # Check if both old_value and new_value are numeric
        if not old_value.isdigit() or not new_value.isdigit():
            messagebox.showinfo("Error", "Both old and new values must be numeric.")
            return

        existing_document = mycol.find_one({"number": old_value})
        if existing_document:
            mycol.update_one({"number": old_value}, {"$set": {"number": new_value}})
            messagebox.showinfo("Success", "Number Successfully Updated")
        else:
            messagebox.showinfo("Error", "Number not find")
    
    old_entry.delete(0, tk.END)
    new_entry.delete(0, tk.END)
    show_contact()

def show_save():
    hide_all()
    name_label.grid(row=2, column=1,  padx=10, pady=5)
    name_entry.grid(row=2, column=2,columnspan=2, padx=10, pady=5)
    number_label.grid(row=3, column=1, padx=10, pady=5)
    number_entry.grid(row=3, column=2,columnspan=2, padx=10, pady=5)
    save_button.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

def show_show():
    hide_all()
    contact_tree.grid(row=4, column=0, columnspan=4, padx=10, pady=5)
    show_contact()

def show_delete():
    hide_all()
    delete_label.grid(row=2, column=1, padx=5)
    delete_entry.grid(row=2, column=2,columnspan=2, padx=10, pady=5)
    delete_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

def hide_all():
    name_label.grid_remove()
    name_entry.grid_remove()
    number_label.grid_remove()
    number_entry.grid_remove()
    save_button.grid_remove()
    delete_label.grid_remove()
    delete_entry.grid_remove()
    delete_button.grid_remove()
    contact_tree.grid_remove()
    option_label.grid_remove()
    name_radio.grid_remove()
    number_radio.grid_remove()
    old_label.grid_remove()
    new_label.grid_remove()
    old_entry.grid_remove()
    new_entry.grid_remove()
    update_button.grid_remove()

root = tk.Tk()
root.title("Contact Management")
root.geometry("300x300")

# Create and configure the input fields and buttons
name_label = tk.Label(root, text="Name")
name_entry = tk.Entry(root)
number_label = tk.Label(root, text="Number")
number_entry = tk.Entry(root)
save_button = tk.Button(root, text="Save Contact", command=save_contact)
delete_label = tk.Label(root, text="Enter Number")
delete_entry = tk.Entry(root)
delete_button = tk.Button(root, text="Delete Contact", command=delete_contact)

# Create and configure the contact Treeview with adjusted width
contact_tree = ttk.Treeview(root, columns=("Name", "Number"), show="headings")

# Define column headings
contact_tree.heading("Name", text="Name", anchor="w")
contact_tree.heading("Number", text="Number", anchor="w")

# Set the width for each column
contact_tree.column("Name", width=100)  # Adjust the width as needed
contact_tree.column("Number", width=100)  # Adjust the width as needed

# Create buttons for different actions
save_option = tk.Button(root, text="New Contact", command=show_save)
show_option = tk.Button(root, text="Contact", command=show_show)
delete_option = tk.Button(root, text="Delete", command=show_delete)
update_option = tk.Button(root, text="Update", command=update_contact)

# Create radio buttons and input for update_contact
selected_option = tk.StringVar()
selected_option.set("number")
option_label = tk.Label(root, text="Select option to update:")
name_radio = tk.Radiobutton(root, text="Update Name", variable=selected_option, value="name")
number_radio = tk.Radiobutton(root, text="Update Number", variable=selected_option, value="number")
old_label = tk.Label(root, text="Old Value")
new_label = tk.Label(root, text="New Value")
old_entry = tk.Entry(root)
new_entry = tk.Entry(root)
update_button = tk.Button(root, text="Update", command=lambda: perform_update(selected_option.get(), old_entry.get(), new_entry.get()))

# Grid layout for widgets
show_option.grid(row=0, column=0, padx=5, pady=5)
save_option.grid(row=0, column=1, padx=5, pady=5)
delete_option.grid(row=0, column=2, padx=10, pady=10)
update_option.grid(row=0, column=3, padx=10, pady=5)

# Apply the validation function to the number_entry widget
validate_func = root.register(validate_number_input)
number_entry.config(validate="key", validatecommand=(validate_func, "%P"))
delete_entry.config(validate="key", validatecommand=(validate_func, "%P"))

# Show the initial "Show" option
show_show()

root.mainloop()
