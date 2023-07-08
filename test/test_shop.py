import unittest
from src.shop import Transaction

class TestTransaction(unittest.TestCase):
    
    def setUp(self):
        self.transaction = Transaction()
        self.transaction.add_item('TestItem', 5, 1000)

    def test_add_item(self):
        self.transaction.add_item('NewItem', 2, 2000)
        self.transaction.cursor.execute("SELECT * FROM transactions WHERE name=?", ('NewItem',))
        result = self.transaction.cursor.fetchone()
        self.assertEqual(result, (2, 'NewItem', 2, 2000))

    def test_show_items(self):
        self.transaction.cursor.execute("SELECT * FROM transactions")
        items = self.transaction.cursor.fetchall()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], (1, 'TestItem', 5, 1000))

    def test_delete_item(self):
        self.transaction.delete_item(1)
        self.transaction.cursor.execute("SELECT * FROM transactions WHERE id=?", (1,))
        result = self.transaction.cursor.fetchone()
        self.assertIsNone(result)

    def test_update_item_name(self):
        self.transaction.update_item_name(1, 'UpdatedName')
        self.transaction.cursor.execute("SELECT name FROM transactions WHERE id=?", (1,))
        result = self.transaction.cursor.fetchone()[0]
        self.assertEqual(result, 'UpdatedName')

    def test_update_item_qty(self):
        self.transaction.update_item_qty(1, 10)
        self.transaction.cursor.execute("SELECT quantity FROM transactions WHERE id=?", (1,))
        result = self.transaction.cursor.fetchone()[0]
        self.assertEqual(result, 10)

    def test_update_item_price(self):
        self.transaction.update_item_price(1, 500)
        self.transaction.cursor.execute("SELECT price FROM transactions WHERE id=?", (1,))
        result = self.transaction.cursor.fetchone()[0]
        self.assertEqual(result, 500)

    def test_reset_transaction(self):
        self.transaction.reset_transaction()
        self.transaction.cursor.execute("SELECT * FROM transactions")
        result = self.transaction.cursor.fetchall()
        self.assertEqual(result, [])

    def test_check_order(self):
        result = self.transaction.check_order()
        self.assertEqual(result, "The order is correct.")
        self.transaction.add_item('BadItem', None, None)
        result = self.transaction.check_order()
        self.assertEqual(result, "There'san error in the transaction data.")

    def test_total_price(self):
        total, discount = self.transaction.total_price()
        self.assertEqual(total, 5000)
        self.assertEqual(discount, 0)
        self.transaction.add_item('NewItem', 10, 50000)
        total, discount = self.transaction.total_price()
        self.assertEqual(total, 500000 * 0.9)
        self.assertEqual(discount, 0.10)

    def test_pay(self):
        change = self.transaction.pay(6000)
        self.assertEqual(change, "Change: 1000.0, Discount: 0.0%")
        change = self.transaction.pay(4000)
        self.assertEqual(change, "The payment is not enough.")

    def tearDown(self):
        self.transaction.reset_transaction()

if __name__ == "__main__":
    unittest.main()
