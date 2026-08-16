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
        self.geometry("750x550")

        self.build_tab_menu()
        self.build_add_tab()
        self.build_history_tab()
        self.build_summary_tab()

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
        # Configure rows
        self.tab_history.grid_rowconfigure(0, weight=0)
        self.tab_history.grid_rowconfigure(1, weight=1)
        self.tab_history.grid_columnconfigure(0, weight=1)

        # Build the filter bar in Row 0
        filter_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
        filter_frame.grid(row=0, column=0, pady=(10, 0), sticky="ew")

        # Create the entry box
        self.history_month_entry = ctk.CTkEntry(filter_frame, width=200, placeholder_text="YYYY-MM (or blank for all)")
        self.history_month_entry.pack(side="left", padx=10)

        filter_btn = ctk.CTkButton(filter_frame, text="Search", command=self.load_history)
        filter_btn.pack(side="left")

        # Build the scrollable list and push it down to row 1
        self.history_list = ctk.CTkScrollableFrame(
            self.tab_history,
            label_text="Saved Transactions"
        )
        self.history_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.history_list.grid_columnconfigure(4, weight=1)
        
        # Load the history
        self.load_history()

    def load_history(self):
        # Clear out the old rows so they don't stack up infinitely
        for widget in self.history_list.winfo_children():
            widget.destroy()

        # Rebuild the header row
        headers = ["Date", "Type", "Amount", "Category", "Description", "Action"]
        for col_idx, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.history_list, 
                text=header_text, 
                font=ctk.CTkFont(weight="bold")
            )
            header_label.grid(row=0, column=col_idx, padx=10, pady=(5, 10), sticky="w")

        # Read the filter input and decide which database method to call
        month_text = self.history_month_entry.get().strip()

        if month_text == "":
            transactions = self.database.get_all_transactions()
        else:
            try:
                date.fromisoformat(f"{month_text}-01")
            except ValueError:
                print(f"Error: '{month_text}' is an invalid month format. Use YYYY-MM.")
                return
            else:
                transactions = self.database.get_monthly_transactions(month_text)

        # Loop through the returned transactions and build the table rows
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
                cell_label = ctk.CTkLabel(self.history_list, text=str(text_value), anchor="w")
                cell_label.grid(row=index + 1, column=col_idx, padx=10, pady=5, sticky="w")

            delete_btn = ctk.CTkButton(
                self.history_list, 
                text="Delete", 
                width=60,
                fg_color="red",
                command=lambda id_to_delete=tx_id: self.on_delete_clicked(id_to_delete)
            )
            delete_btn.grid(row=index + 1, column=5, padx=10, pady=5)

    # Builds a UI card and returns the value label so it can be updated later.
    def create_summary_card(self, parent, row, column, title_text, color, padding_y):
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=column, padx=10, pady=padding_y, sticky="nsew")

        title = ctk.CTkLabel(card, text=title_text, font=ctk.CTkFont(size=14, weight="bold"))
        title.pack(pady=(15, 5))

        val_label = ctk.CTkLabel(card, text="$0.00", font=ctk.CTkFont(size=24, weight="bold"), text_color=color)
        val_label.pack(pady=(0, 15))
        
        return val_label

    def build_summary_tab(self):
        # Row 0: all-time stats cards
        self.all_income_val_label = self.create_summary_card(self.tab_summary, 0, 0, "ALL-TIME INCOME", "green", (20, 10))
        self.all_expense_val_label = self.create_summary_card(self.tab_summary, 0, 1, "ALL-TIME EXPENSES", "red", (20, 10))
        self.all_balance_val_label = self.create_summary_card(self.tab_summary, 0, 2, "ALL-TIME BALANCE", "white", (20, 10))

        # Row 1: the month filter bar
        filter_frame = ctk.CTkFrame(self.tab_summary, fg_color="transparent")
        filter_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.month_entry = ctk.CTkEntry(filter_frame, width=150)
        self.month_entry.insert(0, date.today().isoformat()[:7])
        self.month_entry.pack(side="left", padx=10)

        filter_btn = ctk.CTkButton(filter_frame, text="Filter Month", command=self.load_summary)
        filter_btn.pack(side="left")

        # Row 2: monthly stats cards
        self.month_income_val_label = self.create_summary_card(self.tab_summary, 2, 0, "MONTHLY INCOME", "green", (10, 20))
        self.month_expense_val_label = self.create_summary_card(self.tab_summary, 2, 1, "MONTHLY EXPENSES", "red", (10, 20))
        self.month_balance_val_label = self.create_summary_card(self.tab_summary, 2, 2, "MONTHLY BALANCE", "white", (10, 20))

        # Final setup
        self.tab_summary.grid_columnconfigure((0, 1, 2), weight=1)

        self.load_summary()

    def load_summary(self):
        # Update all-time stats
        all_transactions = self.database.get_all_transactions()
        all_inc, all_exp, all_bal = self.database.calculate_summary(all_transactions)
        
        self.all_income_val_label.configure(text=f"${all_inc:,.2f}")
        self.all_expense_val_label.configure(text=f"${all_exp:,.2f}")
        self.all_balance_val_label.configure(text=f"${all_bal:,.2f}")

        # Extract and validate the month
        month_text = self.month_entry.get()
        try:
            date.fromisoformat(f"{month_text}-01")
        except ValueError:
            print(f"Error: '{month_text}' is not a valid month format. Use YYYY-MM.")
            self.month_income_val_label.configure(text="Error")
            self.month_expense_val_label.configure(text="Error")
            self.month_balance_val_label.configure(text="Error")
            return

        # Update monthly stats
        month_transactions = self.database.get_monthly_transactions(month_text)
        mon_inc, mon_exp, mon_bal = self.database.calculate_summary(month_transactions)

        self.month_income_val_label.configure(text=f"${mon_inc:,.2f}")
        self.month_expense_val_label.configure(text=f"${mon_exp:,.2f}")
        self.month_balance_val_label.configure(text=f"${mon_bal:,.2f}")

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
            self.load_summary()

    def on_delete_clicked(self, tx_id):
        self.database.delete_transaction(tx_id)
        self.load_history()
        self.load_summary()

if __name__ == "__main__":
    app = Interface(Database())
    app.mainloop()