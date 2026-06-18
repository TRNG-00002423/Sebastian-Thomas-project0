from __future__ import annotations
import db.db
class Expense:
    def __init__(self, id:int, user_id:int, amount:int, description:str, date:str) -> None:
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.date = date


    # now called with just ex_expense.create()
    def create(self):
        conn = db.get_connection()
        cursor = conn.execute(
            """
            INSERT INTO expenses (user_id, amount, description, date)
            VALUES (?, ?, ?, ?)
            """,
            (self.user_id, self.amount, self.description, self.date)
        )

        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

        return self
    
    # is called like ex_expense.edit() after modifying values
    def edit(self):
        conn = db.get_connection()
        conn.execute(
            """
            UPDATE expenses
            SET amount = ?, description = ?, date = ?
            WHERE id = ?
            """,
            (self.amount, self.description, self.date, self.id)
        )

        conn.commit()
        conn.close()

    # needs check before hand to see if id exists and status is pending
    @staticmethod
    def remove(id:int):
        conn = db.get_connection()
        conn.execute(
            """
            DELETE FROM expenses WHERE id = ?
            """,
            (id,)
        )

        conn.commit()
        conn.close()

    # added @staticmethod so it can be called Expense.get_all()
    # rather than ex_expense.get_all()
    @staticmethod
    def get_all():
        conn = db.get_connection()
        cursor = conn.execute(
            """
            SELECT * FROM expenses
            """
        )

        rows = cursor.fetchall()
        expenses = []

        for row in rows:
            expenses.append(Expense(
                id=row[0],
                user_id=row[1],
                amount=row[2],
                description=row[3],
                date=row[4]
            ))

        conn.close()

        return expenses

    @staticmethod
    def get_from_id(id:int):
        conn = db.get_connection()
        cursor = conn.execute(
        """
        SELECT * FROM expenses WHERE id = ?
        """, 
        (id,)
        )
    
        row = cursor.fetchone()

        if row is None:
            return None

        return Expense(
                id=row[0],
                user_id=row[1],
                amount=row[2],
                description=row[3],
                date=row[4]
        )


