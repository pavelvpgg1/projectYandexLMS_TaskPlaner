import os
import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Создание таблиц в базе данных"""
        with open("db/schema.sql", "r") as f:
            self.conn.executescript(f.read())

    def get_tasks(self):
        """Получение всех задач из базы данных"""
        cursor = self.conn.execute("SELECT * FROM tasks")
        return [dict(row) for row in cursor]

    def get_edit_task(self, task_id):
        """Получение отредактированной задачи"""
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return [dict(row) for row in cursor]

    def add_task(self, title, description, priority, deadline, status):
        """Добавление задачи в базу данных"""
        self.conn.execute(
            "INSERT INTO tasks (title, description, priority, deadline, status) VALUES (?, ?, ?, ?, ?)",
            (title, description, priority, deadline, status),
        )
        self.conn.commit()

    def update_task(self, task_id, title, description, priority, deadline, status):
        """Обновление данных о задаче"""
        self.conn.execute(
            "UPDATE tasks SET title = ?, description = ?, priority = ?, deadline = ?, status = ? WHERE id = ?",
            (title, description, priority, deadline, status, task_id),
        )
        self.conn.commit()

    def delete_task(self, task_id):
        """Удаление данных о задаче"""
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
