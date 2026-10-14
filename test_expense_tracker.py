import unittest

from expense_tracker import (add_expense, delete_expense,
                             totals_by_category, totals_by_month)


class ExpenseTests(unittest.TestCase):
    def setUp(self):
        self.expenses = []
        add_expense(self.expenses, 10, "food", "lunch", "2026-09-01")
        add_expense(self.expenses, 5.5, "Food", "coffee", "2026-09-15")
        add_expense(self.expenses, 40, "Books", "textbook", "2026-10-02")

    def test_ids_increase(self):
        self.assertEqual([e["id"] for e in self.expenses], [1, 2, 3])

    def test_category_is_normalized(self):
        self.assertEqual(self.expenses[0]["category"], "Food")

    def test_totals_by_category(self):
        self.assertEqual(totals_by_category(self.expenses), {"Books": 40.0, "Food": 15.5})

    def test_totals_by_month(self):
        self.assertEqual(totals_by_month(self.expenses), {"2026-09": 15.5, "2026-10": 40.0})

    def test_delete(self):
        self.assertTrue(delete_expense(self.expenses, 2))
        self.assertFalse(delete_expense(self.expenses, 99))
        self.assertEqual(len(self.expenses), 2)

    def test_bad_input_is_rejected(self):
        with self.assertRaises(ValueError):
            add_expense(self.expenses, -5, "Food")
        with self.assertRaises(ValueError):
            add_expense(self.expenses, 5, "  ")
        with self.assertRaises(ValueError):
            add_expense(self.expenses, 5, "Food", "", "09/01/2026")


if __name__ == "__main__":
    unittest.main()
