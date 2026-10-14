"""Expense Tracker - a small command-line program for recording and summarizing spending.

Usage examples:
    python expense_tracker.py add 12.50 Food "Lunch with classmates"
    python expense_tracker.py list
    python expense_tracker.py summary
    python expense_tracker.py monthly
    python expense_tracker.py delete 3

Data is stored in a CSV file (expenses.csv by default) so it can also be opened in Excel.
"""
import argparse
import csv
import os
from collections import defaultdict
from datetime import date, datetime

FIELDS = ["id", "date", "amount", "category", "note"]
DEFAULT_FILE = "expenses.csv"


def load_expenses(path):
    """Read all expenses from the CSV file. Returns an empty list if it does not exist yet."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["id"] = int(row["id"])
        row["amount"] = float(row["amount"])
    return rows


def save_expenses(path, expenses):
    """Write all expenses back to the CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense(expenses, amount, category, note="", when=None):
    """Add one expense and return it. Raises ValueError for bad input."""
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category.strip():
        raise ValueError("Category cannot be empty.")
    when = when or date.today().isoformat()
    datetime.strptime(when, "%Y-%m-%d")  # raises ValueError if the format is wrong
    new_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {"id": new_id, "date": when, "amount": round(amount, 2),
               "category": category.strip().title(), "note": note}
    expenses.append(expense)
    return expense


def delete_expense(expenses, expense_id):
    """Remove an expense by id. Returns True if something was deleted."""
    before = len(expenses)
    expenses[:] = [e for e in expenses if e["id"] != expense_id]
    return len(expenses) < before


def totals_by_category(expenses):
    """Return {category: total_amount}, sorted from largest to smallest."""
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def totals_by_month(expenses):
    """Return {'YYYY-MM': total_amount}, sorted by month."""
    totals = defaultdict(float)
    for e in expenses:
        totals[e["date"][:7]] += e["amount"]
    return dict(sorted(totals.items()))


def print_list(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"{'ID':<4} {'Date':<11} {'Amount':>9}  {'Category':<14} Note")
    for e in sorted(expenses, key=lambda x: x["date"]):
        print(f"{e['id']:<4} {e['date']:<11} ${e['amount']:>8.2f}  {e['category']:<14} {e['note']}")


def print_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    total = sum(e["amount"] for e in expenses)
    print(f"Total spent: ${total:,.2f} across {len(expenses)} expenses\n")
    print("By category:")
    for category, amount in totals_by_category(expenses).items():
        share = amount / total * 100
        bar = "#" * int(share // 5)
        print(f"  {category:<14} ${amount:>8.2f}  {share:5.1f}%  {bar}")


def print_monthly(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("By month:")
    for month, amount in totals_by_month(expenses).items():
        print(f"  {month}  ${amount:>9.2f}")


def build_parser():
    parser = argparse.ArgumentParser(description="Track and summarize your spending.")
    parser.add_argument("--file", default=DEFAULT_FILE, help="CSV file to use (default: expenses.csv)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add an expense")
    add.add_argument("amount", type=float)
    add.add_argument("category")
    add.add_argument("note", nargs="?", default="")
    add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    sub.add_parser("list", help="list all expenses")
    sub.add_parser("summary", help="totals by category")
    sub.add_parser("monthly", help="totals by month")

    delete = sub.add_parser("delete", help="delete an expense by id")
    delete.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = load_expenses(args.file)

    if args.command == "add":
        try:
            e = add_expense(expenses, args.amount, args.category, args.note, args.date)
        except ValueError as err:
            print(f"Error: {err}")
            return 1
        save_expenses(args.file, expenses)
        print(f"Added #{e['id']}: ${e['amount']:.2f} for {e['category']} on {e['date']}")
    elif args.command == "delete":
        if delete_expense(expenses, args.id):
            save_expenses(args.file, expenses)
            print(f"Deleted expense #{args.id}")
        else:
            print(f"No expense with id {args.id}")
            return 1
    elif args.command == "list":
        print_list(expenses)
    elif args.command == "summary":
        print_summary(expenses)
    elif args.command == "monthly":
        print_monthly(expenses)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
