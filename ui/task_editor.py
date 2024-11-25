from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDateTimeEdit, QPushButton

from db.database import Database
from utils import validate_task_fields, show_message


class TaskEditor(QDialog):
    def __init__(self, parent=None, **task_fields):
        super().__init__(parent)
        self.task_id = task_fields.get("id")
        self.task_title = task_fields.get("title")
        self.task_description = task_fields.get("description")
        self.task_priority = task_fields.get("priority")
        self.task_deadline = QDateTime.fromString(task_fields.get("deadline"), "yyyy-MM-dd HH:mm:ss")
        self.setWindowTitle("Редактирование задачи" if self.task_id else "Добавление задачи")
        self.setGeometry(200, 200, 400, 300)

        # Инициализация базы данных
        self.db = Database("tasks.db")

        # Интерфейс
        self.layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название задачи")
        self.title_input.setText(self.task_title)
        self.layout.addWidget(QLabel("Название:"))
        self.layout.addWidget(self.title_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Описание задачи")
        self.description_input.setText(self.task_description)
        self.layout.addWidget(QLabel("Описание:"))
        self.layout.addWidget(self.description_input)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Низкий", "Средний", "Высокий"])
        self.priority_input.setCurrentText(self.task_priority)
        self.layout.addWidget(QLabel("Приоритет:"))
        self.layout.addWidget(self.priority_input)

        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setDateTime(self.task_deadline if self.task_id else QDateTime.currentDateTime())
        self.deadline_input.setCalendarPopup(True)
        self.layout.addWidget(QLabel("Дедлайн:"))
        self.layout.addWidget(self.deadline_input)

        self.status_input = QComboBox()
        self.status_input.addItems(["0%", "25%", "50%", "75%", "100%"])
        self.layout.addWidget(QLabel("Статус:"))
        self.layout.addWidget(self.status_input)

        self.save_button = QPushButton("Сохранить")
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        # Сигналы
        self.save_button.clicked.connect(self.save_task)

        # Если редактирование, загружаем данные
        if self.task_id:
            self.load_task()

    def load_task(self):
        """Загрузка данных задачи"""
        task = self.db.get_edit_task(self.task_id)[0]
        self.title_input.setText(task['title'])
        self.description_input.setText(task['description'])
        self.priority_input.setCurrentText(task['priority'])
        self.deadline_input.setDateTime(QDateTime.fromString(task['deadline'], "yyyy-MM-dd HH:mm:ss"))
        self.status_input.setCurrentText(task['status'])

    def save_task(self):
        """Сохранение данных задачи"""
        title = self.title_input.text()
        description = self.description_input.text()
        priority = self.priority_input.currentText()
        deadline = self.deadline_input.dateTime()
        status = self.status_input.currentText()

        # Валидация
        is_valid, error_message = validate_task_fields(title, description, deadline)
        if not is_valid:
            show_message(self, "Ошибка", error_message, message_type="error")
            return

        # Сохранение задачи
        if self.task_id:
            self.db.update_task(self.task_id, title, description, priority, deadline.toString("yyyy-MM-dd HH:mm:ss"),
                                status)
        else:
            self.db.add_task(title, description, priority, deadline.toString("yyyy-MM-dd HH:mm:ss"), status)

        self.accept()
