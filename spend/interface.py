import customtkinter as ctk
from database import Database
from datetime import date

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Interface(ctk.CTk):
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.title("Money Tracker")
        self.geometry("700x450")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_add = self.tabview.add("Add")
        self.tab_history = self.tabview.add("History")
        self.tab_summary = self.tabview.add("Summary")

        self.amount_entry = ctk.CTkEntry(self.tab_add, placeholder_text="0.00")

        self.type_dropdown = ctk.CTkComboBox(
            self.tab_add, 
            values=["INCOME", "EXPENSE"]
        )
        
        self.category_entry = ctk.CTkEntry(self.tab_add, placeholder_text="General")

        self.description_entry = ctk.CTkEntry(self.tab_add, placeholder_text="No description")

        self.date_entry = ctk.CTkEntry(self.tab_add, placeholder_text=date.today().isoformat())
        self.date_entry.insert(0, date.today().isoformat())
        
        self.save_btn = ctk.CTkButton(
            self.tab_add, 
            text="Save Transaction", 
            command=self.on_save_clicked
        )
        
        self.tab_add.grid_columnconfigure(0, weight=1)
        self.amount_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.type_dropdown.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.category_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.description_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.date_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.save_btn.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")

    def on_save_clicked(self):
        try:
            float(self.amount_entry.get())
            date.fromisoformat(self.date_entry.get())
        except ValueError:
            print("There was an error while inserting your data! Did you format your amount and date correctly?")
            print("For amount, make sure to use 'XXXX.XX' (with a '.', not a ',')")
            print("For the date, make sure to use the 'YYYY-MM-DD' format")
        else:
            amount_text = self.amount_entry.get()
            selected_type = self.type_dropdown.get()
            category = self.category_entry.get()
            description = self.description_entry.get()
            selected_date = self.date_entry.get()
            self.database.insert_transaction(amount_text, selected_type, category, description, selected_date)
            print(f"Saved! Amount: '{amount_text}', Type: '{selected_type}'")

            self.amount_entry.delete(0, "end")
            self.category_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, date.today().isoformat())

if __name__ == "__main__":
    app = Interface(Database())
    app.mainloop()