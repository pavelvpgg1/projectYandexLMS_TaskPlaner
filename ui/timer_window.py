import pygame
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpinBox, QMessageBox
)
from PyQt6.QtCore import QTimer, QTime


class TimerWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таймер")
        self.setGeometry(300, 300, 300, 200)

        # Инициализация Pygame для воспроизведения звука
        pygame.mixer.init()

        # Таймер и время
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 25, 0)

        # Сохраняем начальное значение времени
        self.initial_time = self.remaining_time  # Изначально сохраняем дефолтное время

        # Интерфейс
        self.layout = QVBoxLayout()

        # Метка для отображения оставшегося времени
        self.time_label = QLabel(self.remaining_time.toString("hh:mm:ss"))
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        self.layout.addWidget(self.time_label)

        # Поля ввода для установки времени
        self.input_layout = QHBoxLayout()
        self.hours_spinbox = QSpinBox()
        self.hours_spinbox.setRange(0, 23)
        self.hours_spinbox.setSuffix(" ч")
        self.minutes_spinbox = QSpinBox()
        self.minutes_spinbox.setRange(0, 59)
        self.minutes_spinbox.setSuffix(" мин")
        self.seconds_spinbox = QSpinBox()
        self.seconds_spinbox.setRange(0, 59)
        self.seconds_spinbox.setSuffix(" сек")
        self.input_layout.addWidget(self.hours_spinbox)
        self.input_layout.addWidget(self.minutes_spinbox)
        self.input_layout.addWidget(self.seconds_spinbox)
        self.layout.addLayout(self.input_layout)

        # Кнопки управления таймером
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton()
        self.start_button.setObjectName("startButton")
        self.update_button_style(is_running=False)

        self.reset_button = QPushButton("Сброс")
        self.reset_button.setObjectName("resetButton")

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.reset_button)
        self.layout.addLayout(self.button_layout)

        # Установка макета
        self.setLayout(self.layout)

        # Подключение сигналов
        self.start_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset_timer)

        self.hours_spinbox.valueChanged.connect(self.update_remaining_time)
        self.minutes_spinbox.valueChanged.connect(self.update_remaining_time)
        self.seconds_spinbox.valueChanged.connect(self.update_remaining_time)

        # Путь к звуковому файлу
        self.sound_file = "assets/sounds/end_timer.mp3"  # Замените на путь к вашему звуковому файлу

    def update_button_style(self, is_running: bool):
        """Обновляет стиль кнопки в зависимости от состояния таймера."""
        if is_running:
            self.start_button.setStyleSheet(
                "background-color: red; color: white; font-size: 14px; border-radius: 8px;"
            )
            self.start_button.setText("Пауза")  # Меняем текст на кнопке
        else:
            self.start_button.setStyleSheet(
                "background-color: green; color: white; font-size: 14px; border-radius: 8px;"
            )
            self.start_button.setText("Старт")  # Меняем текст на кнопке

    def toggle_timer(self):
        """Запуск или остановка таймера с изменением состояния кнопки"""
        if self.timer.isActive():
            self.timer.stop()
            self.update_button_style(is_running=False)
        else:
            self.timer.start(1000)
            self.update_button_style(is_running=True)

    def reset_timer(self):
        """Сброс таймера к значению, установленному пользователем"""
        self.timer.stop()
        self.time_label.setText(self.initial_time.toString("hh:mm:ss"))
        self.update_button_style(is_running=False)
        self.remaining_time = self.initial_time

    def set_timer(self):
        """Установка времени таймера на основе ввода пользователя"""
        hours = self.hours_spinbox.value()
        minutes = self.minutes_spinbox.value()
        seconds = self.seconds_spinbox.value()
        self.remaining_time = QTime(hours, minutes, seconds)
        self.time_label.setText(self.remaining_time.toString("hh:mm:ss"))
        self.update_remaining_time()

    def update_remaining_time(self):
        """Обновляет оставшееся время на основе значений SpinBox в реальном времени"""
        hours = self.hours_spinbox.value()
        minutes = self.minutes_spinbox.value()
        seconds = self.seconds_spinbox.value()
        self.remaining_time = QTime(hours, minutes, seconds)
        self.time_label.setText(self.remaining_time.toString("hh:mm:ss"))
        self.initial_time = self.remaining_time

    def update_timer(self):
        """Обновление оставшегося времени"""
        if self.remaining_time == QTime(0, 0, 0):
            self.timer.stop()
            self.play_sound()  # Воспроизводим звук
            QMessageBox.information(self, "Время вышло", "Таймер завершился!")
            return

        self.remaining_time = self.remaining_time.addSecs(-1)
        self.time_label.setText(self.remaining_time.toString("hh:mm:ss"))

    def play_sound(self):
        """Воспроизведение звука при завершении таймера"""
        pygame.mixer.music.load(self.sound_file)  # Загружаем звук
        pygame.mixer.music.play()  # Воспроизводим звук
