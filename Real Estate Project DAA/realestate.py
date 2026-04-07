import tkinter as tk
from tkinter import ttk, messagebox
import csv

FILE = "properties.csv"

def load_properties():
    properties = []
    try:
        with open(FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['price'] = float(row['price'])
                row['id'] = int(row['id'])
                properties.append(row)
    except FileNotFoundError:
        pass
    return properties

def save_properties(properties):
    with open(FILE, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'location', 'type', 'price', 'owner', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for prop in properties:
            writer.writerow(prop)

def next_id(properties):
    return max([p['id'] for p in properties], default=0) + 1

# ------------------- GUI FUNCTIONS -------------------
class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Management System")
        self.root.geometry("900x500")
        self.properties = load_properties()
        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # Input Frame
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Location").grid(row=0, column=2)
        tk.Label(frame, text="Type").grid(row=0, column=4)
        tk.Label(frame, text="Price").grid(row=1, column=0)
        tk.Label(frame, text="Owner").grid(row=1, column=2)
        tk.Label(frame, text="Status").grid(row=1, column=4)

        self.name_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.owner_var = tk.StringVar()
        self.status_var = tk.StringVar()

        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(frame, textvariable=self.location_var).grid(row=0, column=3)
        tk.Entry(frame, textvariable=self.type_var).grid(row=0, column=5)
        tk.Entry(frame, textvariable=self.price_var).grid(row=1, column=1)
        tk.Entry(frame, textvariable=self.owner_var).grid(row=1, column=3)
        tk.Entry(frame, textvariable=self.status_var).grid(row=1, column=5)

        # Buttons
        tk.Button(frame, text="Add Property", command=self.add_property).grid(row=2, column=0, pady=10)
        tk.Button(frame, text="Update Property", command=self.update_property).grid(row=2, column=1)
        tk.Button(frame, text="Delete Property", command=self.delete_property).grid(row=2, column=2)
        tk.Button(frame, text="Search Property", command=self.search_property).grid(row=2, column=3)
        tk.Button(frame, text="Show All", command=self.populate_treeview).grid(row=2, column=4)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Location", "Type", "Price", "Owner", "Status"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def populate_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for prop in self.properties:
            self.tree.insert("", "end", values=(prop['id'], prop['name'], prop['location'], prop['type'], prop['price'], prop['owner'], prop['status']))

    def add_property(self):
        prop = {
            'id': next_id(self.properties),
            'name': self.name_var.get(),
            'location': self.location_var.get(),
            'type': self.type_var.get(),
            'price': float(self.price_var.get()),
            'owner': self.owner_var.get(),
            'status': self.status_var.get()
        }
        self.properties.append(prop)
        save_properties(self.properties)
        self.populate_treeview()
        messagebox.showinfo("Success", "Property added successfully!")

    def update_property(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a property to update")
            return
        values = self.tree.item(selected, 'values')
        pid = int(values[0])
        for prop in self.properties:
            if prop['id'] == pid:
                prop.update({
                    'name': self.name_var.get(),
                    'location': self.location_var.get(),
                    'type': self.type_var.get(),
                    'price': float(self.price_var.get()),
                    'owner': self.owner_var.get(),
                    'status': self.status_var.get()
                })
                break
        save_properties(self.properties)
        self.populate_treeview()
        messagebox.showinfo("Success", "Property updated successfully!")

    def delete_property(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a property to delete")
            return
        values = self.tree.item(selected, 'values')
        pid = int(values[0])
        self.properties = [p for p in self.properties if p['id'] != pid]
        save_properties(self.properties)
        self.populate_treeview()
        messagebox.showinfo("Success", "Property deleted successfully!")

    def search_property(self):
        query = self.name_var.get().lower()
        filtered = [p for p in self.properties if query in p['name'].lower() or query in p['location'].lower() or query in p['type'].lower()]
        for row in self.tree.get_children():
            self.tree.delete(row)
        for prop in filtered:
            self.tree.insert("", "end", values=(prop['id'], prop['name'], prop['location'], prop['type'], prop['price'], prop['owner'], prop['status']))

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.name_var.set(values[1])
            self.location_var.set(values[2])
            self.type_var.set(values[3])
            self.price_var.set(values[4])
            self.owner_var.set(values[5])
            self.status_var.set(values[6])

# ------------------- MAIN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()