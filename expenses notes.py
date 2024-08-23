import json
from datetime import datetime

# Expense Tracker class
class ExpenseTracker:
    def __init__(self, data_file='expenses.json'):
        self.data_file = data_file
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_expenses(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description):
        date = datetime.now().strftime("%Y-%m-%d")
        self.expenses.setdefault(date, []).append({
            "amount": amount,
            "category": category,
            "description": description
        })
        self.save_expenses()
        print("Expense added successfully.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        for date, expenses in self.expenses.items():
            print(f"Date: {date}")
            for i, expense in enumerate(expenses, 1):
                print(f"  {i}. Amount: ${expense['amount']}, Category: {expense['category']}, Description: {expense['description']}")

    def view_summary(self):
        if not self.expenses:
            print("No expenses to summarize.")
            return

        monthly_summary = {}
        for date, expenses in self.expenses.items():
            month = date[:7]
            monthly_summary.setdefault(month, {"total": 0, "categories": {}})
            for expense in expenses:
                monthly_summary[month]["total"] += expense["amount"]
                category = expense["category"]
                monthly_summary[month]["categories"].setdefault(category, 0)
                monthly_summary[month]["categories"][category] += expense["amount"]

        for month, summary in monthly_summary.items():
            print(f"Month: {month}")
            print(f"  Total Expenses: ${summary['total']}")
            for category, total in summary["categories"].items():
                print(f"  {category}: ${total}")

    def delete_expense(self, date, index):
        try:
            if date in self.expenses and 0 <= index < len(self.expenses[date]):
                del self.expenses[date][index]
                if not self.expenses[date]:  # Remove date if no expenses left
                    del self.expenses[date]
                self.save_expenses()
                print("Expense deleted successfully.")
            else:
                print("Invalid date or index.")
        except ValueError:
            print("Invalid input for date or index.")

    def edit_expense(self, date, index, amount, category, description):
        try:
            if date in self.expenses and 0 <= index < len(self.expenses[date]):
                self.expenses[date][index] = {"amount": amount, "category": category, "description": description}
                self.save_expenses()
                print("Expense edited successfully.")
            else:
                print("Invalid date or index.")
        except ValueError:
            print("Invalid input for date or index.")

    def search_expenses_by_category(self, category):
        found = False
        for date, expenses in self.expenses.items():
            for expense in expenses:
                if expense['category'].lower() == category.lower():
                    print(f"Date: {date}, Amount: ${expense['amount']}, Description: {expense['description']}")
                    found = True
        if not found:
            print(f"No expenses found under category '{category}'.")

def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary")
        print("4. Delete Expense")
        print("5. Edit Expense")
        print("6. Search Expenses by Category")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category (e.g., food, transportation): ")
                description = input("Enter description: ")
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Invalid input. Please enter a valid number for the amount.")

        elif choice == '2':
            tracker.view_expenses()

        elif choice == '3':
            tracker.view_summary()

        elif choice == '4':
            date = input("Enter the date of the expense to delete (YYYY-MM-DD): ")
            index = int(input("Enter the index of the expense to delete: ")) - 1
            tracker.delete_expense(date, index)

        elif choice == '5':
            date = input("Enter the date of the expense to edit (YYYY-MM-DD): ")
            index = int(input("Enter the index of the expense to edit: ")) - 1
            try:
                amount = float(input("Enter new amount: "))
                category = input("Enter new category (e.g., food, transportation): ")
                description = input("Enter new description: ")
                tracker.edit_expense(date, index, amount, category, description)
            except ValueError:
                print("Invalid input. Please enter a valid number for the amount.")

        elif choice == '6':
            category = input("Enter category to search: ")
            tracker.search_expenses_by_category(category)

        elif choice == '7':
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
