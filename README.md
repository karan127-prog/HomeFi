# 🏠 HomeFi — Household Finance Analyzer

> A powerful, modular CLI-based personal finance analyzer built with Python.  
> Track income, expenses, savings goals, forecast future spending, and generate professional PDF & Excel reports — all from your terminal.

---

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║        HomeFi — Household Finance Analyzer           ║
║           Your Personal Money Dashboard              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

  ┌──────────────────────────────────────────────────┐
  │                   MAIN MENU                      │
  ├──────────────────────────────────────────────────┤
  │  ANALYSIS                                        │
  │   1.  Overall Financial Summary                  │
  │   2.  Month-wise Summary                         │
  │   3.  Category-wise Breakdown + Charts           │
  │   4.  Monthly Trend Analysis + Charts            │
  │   5.  Budget vs Actual Report + Chart            │
  │   6.  Next Month Expense Forecast                │
  │   7.  Savings Goals Tracker                      │
  │   8.  Smart Recommendations                      │
  │   15. Filter by Specific Month                   │
  │  ──────────────────────────────────────────────  │
  │  MANAGE DATA                                     │
  │   9.  Set / Update Monthly Budgets               │
  │   10. Add New Savings Goal                       │
  │   11. Update Goal Savings Amount                 │
  │   14. Add New Expense / Income Entry             │
  │  ──────────────────────────────────────────────  │
  │  REPORTS & EXPORT                                │
  │   12. Full Report (Run Everything + PDF)         │
  │   13. Data Summary (what's loaded)               │
  │   16. Export to Excel (.xlsx)                    │
  │   17. Year-end Tax Summary                       │
  └──────────────────────────────────────────────────┘
```

---

## ✨ Features

### 📊 Analysis
| Feature | Description |
|--------|-------------|
| Overall Summary | Total income, expenses, net savings, savings rate |
| Month-wise Summary | Month-by-month breakdown with ↑↓ trend indicators |
| Category Breakdown | Pie chart + bar chart of spending by category |
| Monthly Trends | Line chart — income vs expenses vs savings over time |
| Budget vs Actual | Set budgets per category, get 🔴🟡🟢 alerts |
| Expense Forecast | **Pure NumPy linear regression** — predicts next month's spend |
| Savings Goals | Set goals (e.g. laptop, vacation), track progress + ETA |
| Smart Recommendations | Rule-based tips using **50-30-20 financial rule** |
| Month Filter | Drill into any single month — full analysis + chart |

### 🗂️ Data Management
| Feature | Description |
|--------|-------------|
| Add Entry via CLI | Add income/expense directly from terminal — no manual CSV editing |
| Manage Budgets | Set/update category-wise monthly budgets (saved as JSON) |
| Manage Goals | Add savings goals, update progress, track ETA |

### 📄 Reports & Export
| Feature | Description |
|--------|-------------|
| PDF Report | Multi-page professional PDF with all charts, summary tables, and recommendations |
| Excel Export | 4-sheet formatted `.xlsx` — Dashboard, Monthly Summary, Category Summary, Raw Data |
| Tax Summary | Year-end Indian IT filing helper — 80C, 80D, HRA deductions + Old vs New regime comparison |

---

## 🗂️ Project Structure

```
HomeFi/
│
├── Data/
│   ├── expenses.csv          # Your financial data (edit this)
│   ├── budgets.json          # Auto-generated budget limits
│   └── goals.json            # Auto-generated savings goals
│
├── Modules/
│   ├── loader.py             # Load & validate CSV data
│   ├── analyzer.py           # Core stats: income, expense, savings
│   ├── categorizer.py        # Category-wise breakdown + charts
│   ├── trends.py             # Monthly trend analysis + charts
│   ├── budget.py             # Budget alerts + comparison chart
│   ├── forecaster.py         # NumPy linear regression forecast
│   ├── goals.py              # Savings goal tracker + ETA
│   ├── recommender.py        # Smart saving recommendations
│   ├── report_generator.py   # PDF report (ReportLab)
│   ├── expense_adder.py      # Add entries via CLI
│   ├── month_filter.py       # Single-month analysis
│   ├── excel_exporter.py     # Excel export (openpyxl)
│   └── tax_summary.py        # Year-end tax summary
│
├── Charts/                   # Auto-saved chart images (.png)
├── Reports/                  # Auto-generated PDF & Excel reports
├── main.py                   # CLI entry point (menu-driven)
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/homefi.git
cd homefi
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Data

Edit `Data/expenses.csv` with your own transactions, or use the sample data provided.

**CSV Format:**
```
date,category,type,amount,description
2025-01-05,Food,expense,1500,Groceries
2025-01-10,Salary,income,45000,Monthly salary
2025-01-15,Rent,expense,8000,House rent
```

**Valid Categories:**  
`Food` · `Rent` · `EMI` · `Entertainment` · `Shopping` · `Travel` · `Utilities` · `Healthcare` · `Education` · `Salary` · `Freelance` · `Other`

### 4. Run the App

```bash
python main.py
```

---

## 📦 Requirements

```
pandas
numpy
matplotlib
seaborn
reportlab
openpyxl
```

Install all at once:
```bash
pip install pandas numpy matplotlib seaborn reportlab openpyxl
```

---

## 📊 Sample Output

### Financial Summary
```
💰 OVERALL FINANCIAL SUMMARY
  Total Income   : Rs.  2,95,000
  Total Expenses : Rs.  1,77,400
  Net Savings    : Rs.  1,17,600
  Savings Rate   :        39.86% 🟢 Excellent!
```

### Forecast (NumPy Linear Regression)
```
🔮 NEXT MONTH FORECAST
  Predicted Expense : Rs. 33,138
  Trend             : ↑ INCREASING
  Monthly Change    : +Rs. 1,021/month
```

### Tax Summary
```
  Old Regime Tax (with deductions) : Rs. 12,400
  New Regime Tax (default)         : Rs. 18,200
  💡 OLD REGIME saves you Rs. 5,800 — consider it!
```

---

## 🧠 Technical Highlights

- **Pure NumPy Linear Regression** — no sklearn; built from scratch using `np.polyfit()`
- **Modular Architecture** — each module works independently and is importable
- **JSON Persistence** — budgets and goals saved across sessions
- **7 Auto-generated Charts** — dark-themed matplotlib visualizations
- **Professional PDF** — multi-page ReportLab report with cover page, tables, and charts
- **Excel Export** — formatted openpyxl workbook with 4 sheets and built-in charts
- **Indian Tax Helper** — Old vs New regime comparison with 80C/80D/HRA deductions

---

## 🔮 Future Scope

- [ ] Flask web dashboard — same analysis in the browser
- [ ] Login system — multi-user support
- [ ] Bank SMS parser — auto-import transactions
- [ ] Investment tracker — mutual funds, FD, stocks
- [ ] WhatsApp/Telegram bot integration

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Linear%20Regression-013243?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=flat)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Generation-red?style=flat)
![openpyxl](https://img.shields.io/badge/openpyxl-Excel%20Export-green?style=flat)

---

## 👤 Author

**Karan**  
B.Tech CSE | Passionate about Data Analytics & Python Development  
📧 karank55509@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/karan-kumar-28898338a/) · [GitHub](https://github.com/karan127-prog)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> *"A budget is telling your money where to go instead of wondering where it went."*  
> — Dave Ramsey