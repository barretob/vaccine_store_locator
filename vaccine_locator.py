# Imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

# states and cities dict
state_cities = {
    "NY": ["New York", "Buffalo", "Albany"],
    "CA": ["Los Angeles", "San Francisco", "San Diego"],
    "FL": ["Miami", "Orlando", "Tampa"],
    "IL": ["Chicago", "Peoria", "Rockford"],
}

# get vaccine locations for state and city
def get_locations(state, city):
    url = f"https://getmyvax.org/api/edge/locations?state={state}&city={city}"
    response = requests.get(url)
    if response.ok:
        locations = response.json()["data"]
        results = []
        for location in locations:
            name = location["name"]
            address = " ".join(location["address_lines"])
            phone = location["info_phone"]
            results.append({"name": name, "address": address, "phone": phone})
        return results
    else:
        return None

# # Test function with a sample input
# test = get_locations("NY","New York")
# print(test)

#  display vaccine locations 
def show_locations(*args):
    state = state_var.get()
    city = city_var.get()

    # clear the table
    for i in location_table.get_children():
        location_table.delete(i)

    # vaccine locations state and city
    locations = get_locations(state, city)
    if locations is not None:
        # Populate the table with the vaccine location data
        for i, location in enumerate(locations):
            name = location["name"]
            address = " ".join(location["address"].split("\n"))
            phone = location.get("phone", "-")
            # website = location.get("url", "-")
            location_table.insert("", "end", values=(i+1, name, address, phone))
    else:
        # Show an error message if no locations are found
        messagebox.showerror("Error", "No locations found.")

# window
root = tk.Tk()
root.geometry("800x600")
root.title("Vaccine Locations")

# label for the state dropdown 
state_label = tk.Label(root, text="Select a State:")
state_label.pack()

# StringVar to store the selected state
state_var = tk.StringVar()

# state dropdown
state_combobox = ttk.Combobox(root, textvariable=state_var, state="readonly")
state_combobox.pack()

# values for statedropdown 
state_list = sorted(state_cities.keys())
state_combobox.config(values=state_list)

# label city dropdown
city_label = tk.Label(root, text="Select a City:")
city_label.pack()

#StringVar to store the selected city
city_var = tk.StringVar()

# city dropdown 
city_combobox = ttk.Combobox(root, textvariable=city_var, state="readonly")
city_combobox.pack()

# main title
location_label = tk.Label(root, text="Vaccine Locations:")
location_label.pack()

# table 
location_table = ttk.Treeview(root, columns=("No.","Name","Address", "Phone"))
location_table.heading("#1", text="No.")
location_table.heading("#2", text="Name")
location_table.heading("#3", text="Address")
location_table.heading("#4", text="Phone")
location_table.column("#0", width=5)
location_table.column("#1", width=15)
location_table.column("#2", width=200)
location_table.column("#3", width=300)
location_table.column("#4", width=150)
location_table.pack()

# update cities
def update_cities(*args):
    state = state_var.get()
    if state:
        cities = state_cities.get(state)
        city_var.set("")
        city_combobox.config(values=cities)
    else:
        city_var.set("")
        city_combobox.config(values=[])

# dropdown 
state_combobox.bind("<<ComboboxSelected>>", update_cities)
city_combobox.bind("<<ComboboxSelected>>", show_locations)

root.mainloop()


