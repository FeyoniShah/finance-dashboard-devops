# 💰 FinTrack - Personal Finance Dashboard

## 📌 Problem Statement
Managing personal finances manually is difficult and error-prone. This application helps users track expenses, income, savings, and budget efficiently.

## 🎯 Features
- User Authentication (Login/Signup)
- Add/Edit/Delete Expenses
- Track Income
- Budget Monitoring with Alerts
- Savings Goals
- Visual Charts (Category-wise & Income vs Expense)

## 🛠 Tech Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, Chart.js
- Database: SQLite

## 🚀 How to Run
```bash
pip install -r requirements.txt
python app.py




Docker steps

docker build -t fintrack .
docker run -p 5000:5000 fintrack