"""
main.py
-------
HomeFi — Household Finance Analyzer
Main entry point. Menu-driven CLI connecting all modules.

Run this file to start the app:
    python main.py
"""

import sys
import os
import json
import numpy as np

# Add Modules folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "Modules"))

from loader         import load_data, get_summary
from analyzer       import print_overall_summary, print_monthly_summary
from categorizer    import run_categorizer
from trends         import run_trends
from budget         import run_budget, set_budget_interactive
from forecaster     import run_forecaster
from goals          import run_goals, add_goal_interactive, update_savings_interactive
from recommender    import run_recommender
from report_generator import generate_report
from expense_adder  import add_multiple_entries
from month_filter   import run_month_filter
from excel_exporter import run_excel_export
from tax_summary    import run_tax_summary


# ─────────────────────────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║        HomeFi — Household Finance Analyzer           ║
║           Your Personal Money Dashboard              ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
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
  │  ──────────────────────────────────────────────  │
  │   0.  Exit                                       │
  └──────────────────────────────────────────────────┘
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\n  Press Enter to return to menu...")


def _collect_report_data(df):
    """Collect summary, forecast, goals, tips for PDF report."""
    inc_df = df[df["type"] == "income"]
    exp_df = df[df["type"] == "expense"]

    total_income  = inc_df["amount"].sum()
    total_expense = exp_df["amount"].sum()
    net_savings   = total_income - total_expense
    savings_rate  = (net_savings / total_income * 100) if total_income > 0 else 0

    df2 = df.copy()
    df2["month"]   = df2["date"].dt.to_period("M")
    monthly_exp    = exp_df.copy()
    monthly_exp    = monthly_exp.copy()
    monthly_exp["month"] = monthly_exp["date"].dt.to_period("M")
    monthly_exp_g  = monthly_exp.groupby("month")["amount"].sum()

    monthly_inc    = inc_df.copy()
    monthly_inc["month"] = monthly_inc["date"].dt.to_period("M")
    monthly_inc_g  = monthly_inc.groupby("month")["amount"].sum()
    monthly_sav    = monthly_inc_g.subtract(monthly_exp_g, fill_value=0)

    best_month  = str(monthly_sav.idxmax())  if not monthly_sav.empty  else "N/A"
    worst_month = str(monthly_exp_g.idxmax()) if not monthly_exp_g.empty else "N/A"

    summary = {
        "total_income":  float(total_income),
        "total_expense": float(total_expense),
        "net_savings":   float(net_savings),
        "savings_rate":  float(savings_rate),
        "months":        int(monthly_exp_g.shape[0]),
        "best_month":    best_month,
        "worst_month":   worst_month,
    }

    # Forecast
    if len(monthly_exp_g) >= 2:
        x = np.arange(len(monthly_exp_g))
        y = monthly_exp_g.values
        m, b = np.polyfit(x, y, 1)
        predicted = float(m * len(monthly_exp_g) + b)
        trend = "increasing" if m > 50 else ("decreasing" if m < -50 else "stable")
    else:
        predicted, m, trend = float(total_expense), 0, "stable"

    forecast_data = {
        "predicted_expense": predicted,
        "trend":             trend,
        "monthly_change":    float(m),
    }

    # Goals
    goals = []
    goals_path = os.path.join("Data", "goals.json")
    if os.path.exists(goals_path):
        with open(goals_path, "r") as f:
            raw_goals = json.load(f)
        avg_sav = float(monthly_sav.mean()) if not monthly_sav.empty else 0
        for g in raw_goals:
            target    = g.get("target", 0)
            saved     = g.get("current_savings", 0)
            remaining = max(0, target - saved)
            eta = f"{int(remaining / avg_sav)} months" if avg_sav > 0 else "N/A"
            goals.append({"name": g.get("name","Goal"), "target": target,
                          "saved": saved, "eta": eta})

    # Tips
    tips = []
    cat_totals = exp_df.groupby("category")["amount"].sum()
    thresholds = {"Food": 25, "Entertainment": 10, "Shopping": 15,
                  "Travel": 10, "Utilities": 10}
    for cat, amt in cat_totals.items():
        pct   = (amt / total_expense * 100) if total_expense > 0 else 0
        limit = thresholds.get(cat, 30)
        if pct > limit:
            tips.append(f"{cat} is {pct:.1f}% of expenses — aim below {limit}%.")
    if savings_rate < 20:
        tips.append(f"Savings rate {savings_rate:.1f}% — target at least 20%.")
    if m > 500:
        tips.append(f"Expenses growing Rs.{m:,.0f}/month — review spending.")
    if not tips:
        tips.append("Excellent discipline! Consider investing the surplus.")

    return summary, forecast_data, goals, tips


def run_full_report(df):
    """Run all modules + generate PDF report."""
    print("\n  Running full report... this may take a moment.\n")
    print_overall_summary(df)
    print_monthly_summary(df)
    run_categorizer(df)
    run_trends(df)
    run_budget(df)
    run_forecaster(df)
    run_goals(df)
    run_recommender(df)

    print("\n" + "=" * 55)
    print("  All modules done! Generating PDF report...")
    print("=" * 55)

    summary, forecast_data, goals, tips = _collect_report_data(df)
    path = generate_report(
        summary=summary, forecast_data=forecast_data,
        goals=goals, tips=tips,
        charts_dir="Charts", reports_dir="Reports",
    )

    print("\n" + "=" * 55)
    print("  Full report complete!")
    print(f"  Charts : Charts/")
    print(f"  PDF    : {path}")
    print("=" * 55)


def main():
    clear()
    print(BANNER)

    print("  Loading your financial data...\n")
    try:
        df = load_data("Data/expenses.csv")
    except (FileNotFoundError, ValueError) as e:
        print(e)
        print("\n  Please fix the issue and restart the app.")
        sys.exit(1)

    print("\n  Data loaded! Welcome to HomeFi.\n")
    pause()

    while True:
        clear()
        print(BANNER)
        print(MENU)

        choice = input("  Enter your choice (0-17): ").strip()
        clear()
        print(BANNER)

        if choice == "1":
            print_overall_summary(df)
            print_monthly_summary(df)
            pause()

        elif choice == "2":
            print_monthly_summary(df)
            pause()

        elif choice == "3":
            run_categorizer(df)
            pause()

        elif choice == "4":
            run_trends(df)
            pause()

        elif choice == "5":
            run_budget(df)
            pause()

        elif choice == "6":
            run_forecaster(df)
            pause()

        elif choice == "7":
            run_goals(df)
            pause()

        elif choice == "8":
            run_recommender(df)
            pause()

        elif choice == "9":
            set_budget_interactive()
            pause()

        elif choice == "10":
            add_goal_interactive()
            pause()

        elif choice == "11":
            update_savings_interactive()
            pause()

        elif choice == "12":
            run_full_report(df)
            pause()

        elif choice == "13":
            get_summary(df)
            pause()

        elif choice == "14":
            add_multiple_entries()
            # Reload data after adding entries
            print("\n  Reloading data...")
            try:
                df = load_data("Data/expenses.csv")
                print("  Data reloaded successfully!")
            except Exception as e:
                print(f"  [!] Could not reload: {e}")
            pause()

        elif choice == "15":
            run_month_filter(df)
            pause()

        elif choice == "16":
            run_excel_export(df)
            pause()

        elif choice == "17":
            run_tax_summary(df)
            pause()

        elif choice == "0":
            clear()
            print(BANNER)
            print("  Thank you for using HomeFi!")
            print("  Keep saving, keep growing. Goodbye!\n")
            sys.exit(0)

        else:
            print("  Invalid choice. Please enter a number between 0-17.")
            pause()


if __name__ == "__main__":
    main()