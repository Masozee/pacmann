import sqlite3

class Transaction:
    def __init__(self):

        '''initiate database'''

        self.connection = sqlite3.connect('shop.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL
        )
        """)
        self.connection.commit()
        self.transaction_id = self.get_latest_id() + 1

    def get_latest_id(self):
        '''melakukan check transaksi terakhir berdasarkan Id sehingga menghidari data double'''
        self.cursor.execute("SELECT MAX(id) FROM transactions")
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0

    def add_item(self, name, quantity, price):

        '''Menambahkan Item pada transaksi'''

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            print("Hanya bisa diisi dengan angka.")
            return

        self.cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?)", 
                            (self.transaction_id, name, quantity, price))
        self.connection.commit()
        self.transaction_id += 1

    def show_items(self):

        '''memunculkan daftar item pada transaksi'''

        self.cursor.execute("SELECT * FROM transactions")
        print("ID | Name | Quantity | Price")
        for item in self.cursor.fetchall():
            print(f'{item[0]} | {item[1]} | {item[2]} | {item[3]}')

    def delete_item(self, id):

        '''menghapus item pada transaksi'''

        self.cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
        self.connection.commit()

    def update_item_name(self, id, new_name):

        '''mengupdate nama item pada transaksi'''

        self.cursor.execute("UPDATE transactions SET name=? WHERE id=?", (new_name, id))
        self.connection.commit()

    def update_item_qty(self, id, new_qty):

        '''mengupdate jumlah item pada transaksi'''

        self.cursor.execute("UPDATE transactions SET quantity=? WHERE id=?", (new_qty, id))
        self.connection.commit()

    def update_item_price(self, id, new_price):

        '''mengupdate harga item pada transaksi'''

        self.cursor.execute("UPDATE transactions SET price=? WHERE id=?", (new_price, id))
        self.connection.commit()

    def reset_transaction(self):

        '''memulai ulang transaksi dengan menghapus semua data transaksi berjalan'''

        self.cursor.execute("DELETE FROM transactions")
        self.connection.commit()

    def check_order(self):

        '''mengecek daftar pesanan pada transaksi'''

        self.cursor.execute("SELECT * FROM transactions")
        for transaction in self.cursor.fetchall():
            if not all(transaction[1:]):
                return "There's an error in the transaction data."
        return "The order is correct."

    def total_price(self):

        '''menjumlahkan transaksi dengan diskon'''

        self.cursor.execute("SELECT * FROM transactions")
        total = sum(transaction[2] * transaction[3] for transaction in self.cursor.fetchall())
        discount = 0
        if total > 500000:
            discount = 0.1
        elif total > 300000:
            discount = 0.08
        elif total > 200000:
            discount = 0.05
        total -= total * discount
        return total, discount

    def pay(self, payment):

        '''melakukan pembayaran transaksi serta menampilkan kembalian dari transaksi'''

        total, discount = self.total_price()
        if payment < total:
            return "The payment is not enough."
        change = payment - total
        self.reset_transaction()  # Reset the transaction
        return f'Change: {change}, Discount: {discount * 100}%'

    def __del__(self):
        self.connection.close()

#fungsi yang dugunakan untuk menjalankan aplikasi utama dan mengatur alur eksekusi program
def main():
    trnsct_l23 = Transaction()
    while True:
        print("\n1. Add item")
        print("2. Show items")
        print("3. Delete item")
        print("4. Update item")
        print("5. Reset transaction")
        print("6. Check order")
        print("7. Calculate total price")
        print("8. Pay")
        print("9. Quit")
        option = int(input("Select an option: "))
        if option == 1:
            name = input("Enter item name: ")
            quantity = int(input("Enter item quantity: "))
            price = float(input("Enter item price: "))
            trnsct_l23.add_item(name, quantity, price)
        elif option == 2:
            trnsct_l23.show_items()
        elif option == 3:
            trnsct_l23.show_items()
            id = int(input("Enter ID of the item to delete: "))
            trnsct_l23.delete_item(id)
        elif option == 4:
            trnsct_l23.show_items()
            id = int(input("Enter ID of the item to update: "))
            print("\n1. Update name")
            print("2. Update quantity")
            print("3. Update price")
            option = int(input("Select an option: "))
            if option == 1:
                new_name = input("Enter new name: ")
                trnsct_l23.update_item_name(id, new_name)
            elif option == 2:
                new_qty = int(input("Enter new quantity: "))
                trnsct_l23.update_item_qty(id, new_qty)
            elif option == 3:
                new_price = float(input("Enter new price: "))
                trnsct_l23.update_item_price(id, new_price)
        elif option == 5:
            trnsct_l23.reset_transaction()
            print("Transaction has been reset.")
        elif option == 6:
            print(trnsct_l23.check_order())
        elif option == 7:
            total, discount = trnsct_l23.total_price()
            print(f"Total price: {total}, Discount: {discount * 100}%")
        elif option == 8:
            payment = float(input("Enter the amount of money given: "))
            print(trnsct_l23.pay(payment))
        elif option == 9:
            break


if __name__ == "__main__":
    main()
