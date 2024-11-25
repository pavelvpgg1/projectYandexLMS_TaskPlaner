import sys
import traceback

from PyQt6.QtWidgets import QApplication

from db.database import Database
from ui.main_window import MainWindow


def main():
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)

    # Создаем или подключаем базу данных
    db = Database("db/tasks.db")

    # Создаем главное окно приложения
    main_window = MainWindow()

    try:
        with open("assets/styles.css", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("CSS файл не найден. Проверьте путь: assets/styles.css")

    # Показываем главное окно
    main_window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())


def excepthook(exc_type, exc_value, exc_tb):
    if exc_type == SystemExit:
        # Если ошибка SystemExit, то просто выходим
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    else:
        # Выводим ошибку в консоль
        traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == "__main__":
    sys.excepthook = excepthook
    main()
