from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QDialog, QLabel
)

from db.database import Database
from ui.task_editor import TaskEditor
from ui.timer_window import TimerWindow
from utils import format_datetime_for_display, calculate_remaining_time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик задач")
        self.setGeometry(100, 100, 1000, 600)

        # Инициализация базы данных
        self.db = Database("tasks.db")

        # Главное окно
        self.layout = QVBoxLayout()

        # Таблица задач
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(7)
        self.task_table.setHorizontalHeaderLabels(
            ["Название", "Описание", "Приоритет", "Дедлайн", "До конца", "Время начала", "Статус"])
        self.layout.addWidget(self.task_table)

        # Кнопки управления
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить задачу")
        self.add_button.setObjectName("addButton")
        self.edit_button = QPushButton("Редактировать задачу")
        self.delete_button = QPushButton("Удалить задачу")
        self.delete_button.setObjectName("deleteButton")
        self.timer_button = QPushButton("Запустить таймер")
        self.button_layout.addWidget(self.timer_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.add_button)
        self.layout.addLayout(self.button_layout)

        # Основной виджет
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Подключение сигналов
        self.add_button.clicked.connect(self.open_task_editor)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.timer_button.clicked.connect(self.open_timer)

        # Загрузка задач
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач в таблицу из базы данных"""
        tasks = self.db.get_tasks()
        self.task_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            self.task_table.setItem(row, 0, QTableWidgetItem(task['title']))
            self.task_table.setItem(row, 2, QTableWidgetItem(task['priority']))
            self.task_table.setItem(row, 3, QTableWidgetItem(format_datetime_for_display(task['deadline'])))
            remaining_time = calculate_remaining_time(QDateTime.fromString(task['deadline'], "yyyy-MM-dd HH:mm:ss"))
            self.task_table.setItem(row, 4, QTableWidgetItem(remaining_time))
            self.task_table.setItem(row, 5, QTableWidgetItem(task['created_at']))
            self.task_table.setItem(row, 6, QTableWidgetItem(task['status']))

            description_button = QPushButton("Подробнее...")
            description_button.clicked.connect(lambda _, t=task['description']: self.show_description(t))
            self.task_table.setCellWidget(row, 1, description_button)

        self.task_table.setColumnWidth(0, 180)
        self.task_table.setColumnWidth(1, 150)
        self.task_table.setColumnWidth(2, 70)
        self.task_table.setColumnWidth(3, 130)
        self.task_table.setColumnWidth(4, 130)
        self.task_table.setColumnWidth(5, 130)
        self.task_table.horizontalHeader().setStretchLastSection(True)

    def show_description(self, description):
        """Показ полного описания задачи"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Описание задачи")
        layout = QVBoxLayout()
        label = QLabel(description)
        label.setWordWrap(True)  # Разрешаем перенос строк
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()

    def open_task_editor(self):
        """Открытие окна добавления задачи"""
        editor = TaskEditor(self)
        editor.exec()
        self.load_tasks()

    def edit_task(self):
        """Редактирование выбранной задачи"""
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для редактирования.")
            return
        task = self.db.get_tasks()[selected_row]
        editor = TaskEditor(self, **task)
        editor.exec()
        self.load_tasks()

    def delete_task(self):
        """Удаление выбранной задачи"""
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления.")
            return
        task_id = self.db.get_tasks()[selected_row]['id']
        self.db.delete_task(task_id)
        QMessageBox.information(self, "Успех", "Задача удалена.")
        self.load_tasks()

    @staticmethod
    def open_timer():
        """Открытие окна таймера"""
        TimerWindow().exec()
