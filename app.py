import mysql.connector
import csv



conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*****",
    database="expense_tracker"
)

print("Database connected successfully! ✅")




monthly_budget = 0




def add_expense():

    print("\n========== ADD EXPENSE ==========")

    expense_date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))
    payment_method = input("Enter payment method: ")

    query = """
    INSERT INTO expenses
    (expense_date, category, description, amount, payment_method)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        expense_date,
        category,
        description,
        amount,
        payment_method
    )

    cursor = conn.cursor()

    cursor.execute(query, values)

    conn.commit()

    cursor.close()

    print("\nExpense added successfully! ✅")




def view_expenses():

    print("\n========== ALL EXPENSES ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    ORDER BY expense_id
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if not records:

        print("No expenses found.")

    else:

        for record in records:

            print(
                "ID:", record[0],
                "| Date:", record[1],
                "| Category:", record[2],
                "| Description:", record[3],
                "| Amount:", record[4],
                "| Payment:", record[5]
            )

    cursor.close()



def update_expense():

    print("\n========== UPDATE EXPENSE ==========")

    expense_id = int(input("Enter Expense ID to update: "))

    print("\nWhat do you want to update?")
    print("1. Category")
    print("2. Description")
    print("3. Amount")
    print("4. Payment Method")

    choice = input("Enter your choice: ")

    cursor = conn.cursor()

    if choice == "1":

        new_value = input("Enter new category: ")

        query = """
        UPDATE expenses
        SET category = %s
        WHERE expense_id = %s
        """

    elif choice == "2":

        new_value = input("Enter new description: ")

        query = """
        UPDATE expenses
        SET description = %s
        WHERE expense_id = %s
        """

    elif choice == "3":

        new_value = float(input("Enter new amount: "))

        query = """
        UPDATE expenses
        SET amount = %s
        WHERE expense_id = %s
        """

    elif choice == "4":

        new_value = input("Enter new payment method: ")

        query = """
        UPDATE expenses
        SET payment_method = %s
        WHERE expense_id = %s
        """

    else:

        print("\nInvalid choice! ❌")

        cursor.close()

        return

    cursor.execute(query, (new_value, expense_id))

    conn.commit()

    if cursor.rowcount > 0:

        print("\nExpense updated successfully! ✅")

    else:

        print("\nExpense ID not found! ❌")

    cursor.close()


=====

def delete_expense():

    print("\n========== DELETE EXPENSE ==========")

    expense_id = int(input("Enter Expense ID to delete: "))

    confirm = input(
        "Are you sure you want to delete this expense? (yes/no): "
    )

    if confirm.lower() != "yes":

        print("\nDelete cancelled.")

        return

    cursor = conn.cursor()

    query = """
    DELETE FROM expenses
    WHERE expense_id = %s
    """

    cursor.execute(query, (expense_id,))

    conn.commit()

    if cursor.rowcount > 0:

        print("\nExpense deleted successfully! ✅")

    else:

        print("\nExpense ID not found! ❌")

    cursor.close()




def total_expense():

    print("\n========== TOTAL EXPENSE ==========")

    cursor = conn.cursor()

    query = """
    SELECT SUM(amount)
    FROM expenses
    """

    cursor.execute(query)

    result = cursor.fetchone()

    total = result[0]

    if total is None:

        total = 0

    print("Total Expense: ₹", total)

    cursor.close()




def category_summary():

    print("\n========== CATEGORY-WISE SUMMARY ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        category,
        SUM(amount) AS total_amount
    FROM expenses
    GROUP BY category
    ORDER BY total_amount DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if not records:

        print("No expenses found.")

    else:

        for record in records:

            print(
                "Category:", record[0],
                "| Total: ₹", record[1]
            )

    cursor.close()




def payment_summary():

    print("\n========== PAYMENT METHOD SUMMARY ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        payment_method,
        SUM(amount) AS total_amount
    FROM expenses
    GROUP BY payment_method
    ORDER BY total_amount DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if not records:

        print("No expenses found.")

    else:

        for record in records:

            print(
                "Payment Method:", record[0],
                "| Total: ₹", record[1]
            )

    cursor.close()




def monthly_summary():

    print("\n========== MONTHLY EXPENSE SUMMARY ==========")

    year = int(input("Enter year: "))

    month = int(input("Enter month (1-12): "))

    cursor = conn.cursor()

    query = """
    SELECT SUM(amount)
    FROM expenses
    WHERE YEAR(expense_date) = %s
    AND MONTH(expense_date) = %s
    """

    cursor.execute(query, (year, month))

    result = cursor.fetchone()

    total = result[0]

    if total is None:

        total = 0

    print("\nYear:", year)
    print("Month:", month)
    print("Total Expense: ₹", total)

    cursor.close()




def search_by_id():

    print("\n========== SEARCH EXPENSE ==========")

    expense_id = int(input("Enter Expense ID: "))

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    WHERE expense_id = %s
    """

    cursor.execute(query, (expense_id,))

    record = cursor.fetchone()

    if record:

        print("\nExpense Found! ✅")

        print("ID:", record[0])
        print("Date:", record[1])
        print("Category:", record[2])
        print("Description:", record[3])
        print("Amount: ₹", record[4])
        print("Payment Method:", record[5])

    else:

        print("\nExpense ID not found! ❌")

    cursor.close()




def search_by_category():

    print("\n========== SEARCH BY CATEGORY ==========")

    category = input("Enter category: ")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    WHERE category = %s
    ORDER BY expense_date
    """

    cursor.execute(query, (category,))

    records = cursor.fetchall()

    if not records:

        print("\nNo expenses found for this category.")

    else:

        for record in records:

            print(
                "ID:", record[0],
                "| Date:", record[1],
                "| Category:", record[2],
                "| Description:", record[3],
                "| Amount:", record[4],
                "| Payment:", record[5]
            )

    cursor.close()




def filter_by_date():

    print("\n========== FILTER BY DATE ==========")

    start_date = input("Enter start date (YYYY-MM-DD): ")

    end_date = input("Enter end date (YYYY-MM-DD): ")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    WHERE expense_date BETWEEN %s AND %s
    ORDER BY expense_date
    """

    cursor.execute(query, (start_date, end_date))

    records = cursor.fetchall()

    if not records:

        print("\nNo expenses found for this date range.")

    else:

        for record in records:

            print(
                "ID:", record[0],
                "| Date:", record[1],
                "| Category:", record[2],
                "| Description:", record[3],
                "| Amount:", record[4],
                "| Payment:", record[5]
            )

    cursor.close()




def highest_expense():

    print("\n========== HIGHEST EXPENSE ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    ORDER BY amount DESC
    LIMIT 1
    """

    cursor.execute(query)

    record = cursor.fetchone()

    if record:

        print("ID:", record[0])
        print("Date:", record[1])
        print("Category:", record[2])
        print("Description:", record[3])
        print("Amount: ₹", record[4])
        print("Payment:", record[5])

    else:

        print("No expenses found.")

    cursor.close()




def lowest_expense():

    print("\n========== LOWEST EXPENSE ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    ORDER BY amount ASC
    LIMIT 1
    """

    cursor.execute(query)

    record = cursor.fetchone()

    if record:

        print("ID:", record[0])
        print("Date:", record[1])
        print("Category:", record[2])
        print("Description:", record[3])
        print("Amount: ₹", record[4])
        print("Payment:", record[5])

    else:

        print("No expenses found.")

    cursor.close()




def average_expense():

    print("\n========== AVERAGE EXPENSE ==========")

    cursor = conn.cursor()

    query = """
    SELECT AVG(amount)
    FROM expenses
    """

    cursor.execute(query)

    result = cursor.fetchone()

    average = result[0]

    if average is None:

        average = 0

    print("Average Expense: ₹", round(float(average), 2))

    cursor.close()




def expense_count():

    print("\n========== EXPENSE COUNT ==========")

    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM expenses
    """

    cursor.execute(query)

    result = cursor.fetchone()

    count = result[0]

    print("Total Number of Expenses:", count)

    cursor.close()




def set_budget():

    global monthly_budget

    print("\n========== SET MONTHLY BUDGET ==========")

    monthly_budget = float(
        input("Enter your monthly budget: ₹ ")
    )

    print(
        "\nMonthly budget set to ₹",
        monthly_budget
    )



def budget_status():

    print("\n========== BUDGET STATUS ==========")

    if monthly_budget == 0:

        print("Please set your monthly budget first.")

        return

    cursor = conn.cursor()

    query = """
    SELECT SUM(amount)
    FROM expenses
    """

    cursor.execute(query)

    result = cursor.fetchone()

    total = result[0]

    if total is None:

        total = 0

    print("Monthly Budget: ₹", monthly_budget)
    print("Total Spent: ₹", total)

    remaining = monthly_budget - float(total)

    if remaining > 0:

        print("Remaining Budget: ₹", remaining)
        print("Budget Status: Within Budget ✅")

    elif remaining == 0:

        print("Budget Status: Budget Fully Used ⚠️")

    else:

        print("Exceeded Amount: ₹", abs(remaining))
        print("Budget Status: Budget Exceeded! ❌")

    cursor.close()




def export_csv():

    print("\n========== EXPORT EXPENSES ==========")

    cursor = conn.cursor()

    query = """
    SELECT
        expense_id,
        expense_date,
        category,
        description,
        amount,
        payment_method
    FROM expenses
    ORDER BY expense_id
    """

    cursor.execute(query)

    records = cursor.fetchall()

    if not records:

        print("No expenses available to export.")

        cursor.close()

        return

    filename = "expense_report.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Expense ID",
            "Date",
            "Category",
            "Description",
            "Amount",
            "Payment Method"
        ])

        writer.writerows(records)

    cursor.close()

    print("\nCSV report created successfully! ✅")
    print("File name:", filename)



while True:

    print("\n")
    print("================================================")
    print("           PERSONAL EXPENSE TRACKER")
    print("================================================")

    print("1.  Add Expense")
    print("2.  View Expenses")
    print("3.  Update Expense")
    print("4.  Delete Expense")
    print("5.  Total Expense")
    print("6.  Category-wise Summary")
    print("7.  Payment Method Summary")
    print("8.  Monthly Expense Summary")
    print("9.  Search by Expense ID")
    print("10. Search by Category")
    print("11. Filter by Date")
    print("12. Highest Expense")
    print("13. Lowest Expense")
    print("14. Average Expense")
    print("15. Expense Count")
    print("16. Set Monthly Budget")
    print("17. Budget Status")
    print("18. Export to CSV")
    print("19. Exit")

    print("================================================")

    choice = input("Enter your choice: ")




    if choice == "1":

        add_expense()

    elif choice == "2":

        view_expenses()

    elif choice == "3":

        update_expense()

    elif choice == "4":

        delete_expense()

    elif choice == "5":

        total_expense()

    elif choice == "6":

        category_summary()

    elif choice == "7":

        payment_summary()

    elif choice == "8":

        monthly_summary()

    elif choice == "9":

        search_by_id()

    elif choice == "10":

        search_by_category()

    elif choice == "11":

        filter_by_date()

    elif choice == "12":

        highest_expense()

    elif choice == "13":

        lowest_expense()

    elif choice == "14":

        average_expense()

    elif choice == "15":

        expense_count()

    elif choice == "16":

        set_budget()

    elif choice == "17":

        budget_status()

    elif choice == "18":

        export_csv()

    elif choice == "19":

        print("\nThank you for using Personal Expense Tracker! 👋")

        break

    else:

        print("\nInvalid choice! Please enter 1-19.")




conn.close()

print("Database connection closed. ✅")
