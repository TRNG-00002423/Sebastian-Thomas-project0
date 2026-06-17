from __future__ import annotations
from db import get_connection
class User:
    def __init__(self, id:int, username:str, password:str, role:str) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.role = role


    def create(self, user:User):
        conn = get_connection()
        cursor = conn.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (user.username, user.password, user.role)
        )

        user.id = cursor.lastrowid
        conn.close()

        return user
    
    def get_all(self):
        conn = get_connection()
        cursor = conn.execute(
            """
            SELECT * FROM users
            """
        )

        rows = cursor.fetchall()
        users = []

        for row in rows:
            users.append(User(
                id=row[0],
                username=row[1],
                password=row[2],
                role=row[3]
            ))

        conn.close()

        return users

    def get_from_id(self,id:int):
        conn = get_connection()
        cursor = conn.execute(
        """
        SELECT * FROM users WHERE id = ?
        """, 
        (id,)
        )
    
        row = cursor.fetchone()

        if row is None:
            return None

        return User(
            id=row[0],
            username=row[1],
            password=row[2],
            role=row[3]
        )
    
    def get_from_username_password(self, username, password):
        conn = get_connection()
        cursor = conn.execute(
        """
        SELECT * FROM users WHERE username = ? AND password = ?
        """, 
        (username,password)
        )
    
        row = cursor.fetchone()

        if row is None:
            return None

        return User(
            id=row[0],
            username=row[1],
            password=row[2],
            role=row[3]
        )

