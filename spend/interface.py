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
        self.geometry("750x450")

        self.build_tab_menu()
        self.build_add_tab()
        self.build_history_tab()

    def build_tab_menu(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_add = self.tabview.add("Add")
        self.tab_history = self.tabview.add("History")
        self.tab_summary = self.tabview.add("Summary")

    def build_add_tab(self):
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

    def build_history_tab(self):
        self.tab_history.grid_rowconfigure(0, weight=1)
        self.tab_history.grid_columnconfigure(0, weight=1)

        self.history_list = ctk.CTkScrollableFrame(
            self.tab_history,
            label_text="Saved Transactions"
        )
        self.history_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.history_list.grid_columnconfigure(4, weight=1)
        
        self.load_history()

    def load_history(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()

        headers = ["Date", "Type", "Amount", "Category", "Description", "Action"]
        for col_idx, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.history_list, 
                text=header_text, 
                font=ctk.CTkFont(weight="bold")
            )
            header_label.grid(row=0, column=col_idx, padx=10, pady=(5, 10), sticky="w")

        transactions = self.database.get_all_transactions()

        for index, tx in enumerate(transactions):
            tx_id = tx[0]
            row_data = [
                tx[5], # Date
                tx[2], # Type
                f"${tx[1]:.2f}", # Amount
                tx[3], # Category
                tx[4] # Description
            ]

            for col_idx, text_value in enumerate(row_data):
                cell_label = ctk.CTkLabel(self.history_list, text=text_value, anchor="w")
                cell_label.grid(
                    row=index + 1, 
                    column=col_idx, 
                    padx=10, 
                    pady=5, 
                    sticky="w"
                )

            delete_btn = ctk.CTkButton(
                self.history_list, 
                text="Delete", 
                width=60,
                fg_color="red",
                command=lambda id_to_delete=tx_id: self.on_delete_clicked(id_to_delete)
            )
            delete_btn.grid(row=index + 1, column=5, padx=10, pady=5)

    def on_save_clicked(self):
        try:
            float(self.amount_entry.get())
            date.fromisoformat(self.date_entry.get())
        except ValueError:
            print("Error: Check your amount (e.g. 12.50) and date format (YYYY-MM-DD).")
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

            self.load_history()

    def on_delete_clicked(self, tx_id):
        self.database.delete_transaction(tx_id)
        self.load_history()

if __name__ == "__main__":
    app = Interface(Database())
    app.mainloop()