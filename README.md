# 💰 Personal Expense Tracker

A web-based **Personal Expense Tracker** built with **Python, Streamlit, MySQL, and Plotly** to help users record, manage, analyze, and visualize their personal expenses efficiently.

## 🚀 Features

* Add and manage personal expenses
* Store expense records using MySQL
* Categorize expenses
* View expense history
* Analyze spending patterns
* Interactive data visualizations using Plotly
* Expense summaries and insights
* User-friendly interface built with Streamlit

## 🛠️ Tech Stack

| Technology    | Purpose                                    |
| ------------- | ------------------------------------------ |
| **Python**    | Application development and business logic |
| **Streamlit** | Web application interface                  |
| **MySQL**     | Database and data storage                  |
| **Plotly**    | Interactive data visualization             |

## 📊 Project Overview

The **Personal Expense Tracker** provides a simple and interactive platform for maintaining personal financial records.

Users can enter expense information such as:

* Date
* Category
* Amount
* Description

The application stores the information in a **MySQL database** and provides interactive charts using **Plotly** to help users understand their spending patterns.

## 📁 Project Structure

```text
Personal-Expense-Tracker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.sql
│
└── assets/
    └── screenshots/
```

> The project structure may vary depending on the implementation.

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/divyalakshmi09-2005/Personal-Expense-Tracker.git
cd Personal-Expense-Tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database for the application and configure the database connection according to your project setup.

Example:

```python
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "expense_tracker"
```

> **Security Note:** Never upload database passwords or other sensitive credentials to GitHub. Use environment variables or Streamlit Secrets for production applications.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📈 Data Visualization

The project uses **Plotly** to create interactive visualizations for:

* Category-wise expense analysis
* Monthly spending trends
* Total expenses
* Spending distribution
* Expense comparisons

## 🎯 Project Objectives

This project demonstrates practical experience in:

* Python programming
* Streamlit application development
* MySQL database integration
* CRUD operations
* Data analysis
* Data visualization
* Database-driven application development

## 🔮 Future Enhancements

* User authentication
* Monthly and yearly budgets
* Budget alerts
* CSV/Excel export
* Advanced financial analytics
* Expense reports
* Cloud database integration
* Online deployment

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push your branch
6. Create a Pull Request

## 📄 License

This project is developed for **educational and personal use**.

## 👩‍💻 Author

**Divyalakshmi.B**

GitHub: **@divyalakshmi09-2005**

If you found this project useful, consider giving the repository a ⭐.
