from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime


def show_message(parent, title, text, message_type="info"):
    """
    Удобный способ показывать всплывающие сообщения.

    Args:
        parent: Родительское окно, в котором показывается сообщение.
        title (str): Заголовок сообщения.
        text (str): Текст сообщения.
        message_type (str): Тип сообщения: 'info', 'warning', 'error'.
    """
    msg_box = QMessageBox(parent)
    if message_type == "info":
        msg_box.setIcon(QMessageBox.Icon.Information)
    elif message_type == "warning":
        msg_box.setIcon(QMessageBox.Icon.Warning)
    elif message_type == "error":
        msg_box.setIcon(QMessageBox.Icon.Critical)

    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.exec()


def format_datetime_for_display(datetime_str):
    """
    Форматирует строку с датой-временем для отображения.

    Args:
        datetime_str (str): Дата-время в формате ISO (YYYY-MM-DD HH:MM:SS).

    Returns:
        str: Форматированная строка для пользователя (например, "24.11.2024 18:30").
    """
    dt = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss")
    return dt.toString("dd.MM.yyyy HH:mm")


def validate_task_fields(title, description, deadline):
    """
    Проверяет, что поля задачи заполнены корректно.

    Args:
        title (str): Название задачи.
        description (str): Описание задачи.
        deadline (QDateTime): Дата-время дедлайна.

    Returns:
        tuple: (bool, str) - True и пустая строка, если все поля валидны, иначе False и сообщение об ошибке.
    """
    if not title.strip():
        return False, "Название задачи не может быть пустым."
    if not description.strip():
        return False, "Описание задачи не может быть пустым."
    if deadline < QDateTime.currentDateTime():
        return False, "Дедлайн не может быть в прошлом."
    return True, ""


def calculate_remaining_time(deadline):
    """
    Вычисляет оставшееся время до дедлайна.

    Args:
        deadline (QDateTime): Дата-время дедлайна.

    Returns:
        str: Форматированная строка (например, "2 дня 5 часов").
    """
    current_time = QDateTime.currentDateTime()
    if deadline < current_time:
        return "Дедлайн уже прошёл"

    diff = current_time.secsTo(deadline)
    days = diff // (24 * 3600)
    hours = (diff % (24 * 3600)) // 3600
    minutes = (diff % 3600) // 60

    result = []
    if days > 0:
        result.append(f"{days} дн.")
    if hours > 0:
        result.append(f"{hours} ч.")
    if minutes > 0:
        result.append(f"{minutes} мин.")

    return " ".join(result)
