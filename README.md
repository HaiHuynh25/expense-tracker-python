# Expense Tracker (Python)

A small command-line program for recording spending and seeing where the money goes.
Data is saved in a CSV file, so it can also be opened in Excel.

**Built with:** Python 3 (standard library only: `argparse`, `csv`, `datetime`, `collections`, `unittest`)

## Features
- Add expenses with an amount, category, note, and optional date
- List all expenses
- Summary of spending by category (with percentages)
- Totals by month
- Delete an expense by id
- Input checks (no negative amounts, empty categories, or badly formatted dates)
- Unit tests for the core logic

## How to run
Requires Python 3.8 or newer. No packages to install.

```
python expense_tracker.py add 12.50 Food "Lunch with classmates"
python expense_tracker.py add 48 Books "Textbook" --date 2026-09-05
python expense_tracker.py list
python expense_tracker.py summary
python expense_tracker.py monthly
python expense_tracker.py delete 3
```

Try it with the included sample data:

```
python expense_tracker.py --file sample_expenses.csv summary
```

## Example output
```
Total spent: $147.64 across 7 expenses

By category:
  Transport      $   55.00   37.3%  #######
  Books          $   48.00   32.5%  ######
  Food           $   28.65   19.4%  ###
  Entertainment  $   15.99   10.8%  ##
```

## Run the tests
```
python test_expense_tracker.py
```

## What I learned
- Organizing a program into small functions that each do one job
- Reading and writing CSV files
- Grouping and summarizing data with dictionaries
- Validating user input
- Writing unit tests

## Ideas for next steps
- Monthly budgets with warnings
- Charts with matplotlib
- A simple web or GUI version

*The sample data in `sample_expenses.csv` is made up for demonstration.*
