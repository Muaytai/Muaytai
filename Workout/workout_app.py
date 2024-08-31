import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

# Создание и подключение к базе данных
conn = sqlite3.connect('workouts.db')
c = conn.cursor()

# Создание таблицы для хранения информации о тренировках
c.execute('''CREATE TABLE IF NOT EXISTS workouts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TEXT,
              workout_type TEXT,
              duration INTEGER,
              notes TEXT)''')
conn.commit()


# Функция для добавления новой тренировки
def add_workout():
    date = simpledialog.askstring("Дата", "Введите дату тренировки (гггг-мм-дд):")
    workout_type = simpledialog.askstring("Тип тренировки", "Введите тип тренировки:")
    duration = simpledialog.askinteger("Длительность", "Введите длительность тренировки в минутах:")
    notes = simpledialog.askstring("Заметки", "Введите заметки (если есть):")

    c.execute("INSERT INTO workouts (date, workout_type, duration, notes) VALUES (?, ?, ?, ?)",
              (date, workout_type, duration, notes))
    conn.commit()
    update_workout_list()


# Функция для редактирования выбранной тренировки
def edit_workout():
    selected_item = workout_list.curselection()
    if selected_item:
        workout_id = workout_list.get(selected_item).split()[0]
        date = simpledialog.askstring("Дата", "Введите новую дату тренировки (гггг-мм-дд):")
        workout_type = simpledialog.askstring("Тип тренировки", "Введите новый тип тренировки:")
        duration = simpledialog.askinteger("Длительность", "Введите новую длительность тренировки в минутах:")
        notes = simpledialog.askstring("Заметки", "Введите новые заметки (если есть):")

        c.execute("UPDATE workouts SET date = ?, workout_type = ?, duration = ?, notes = ? WHERE id = ?",
                  (date, workout_type, duration, notes, workout_id))
        conn.commit()
        update_workout_list()
    else:
        messagebox.showwarning("Предупреждение", "Выберите тренировку для редактирования")


# Функция для обновления списка тренировок
def update_workout_list():
    workout_list.delete(0, END)
    for row in c.execute("SELECT * FROM workouts"):
        workout_list.insert(END, f"{row[0]}: {row[1]}, {row[2]}, {row[3]} мин, {row[4]}")


# Создание основного окна приложения
root = Tk()
root.title("Трекер тренировок")

# Создание списка для отображения тренировок
workout_list = Listbox(root, width=80)
workout_list.pack()

# Создание кнопок для управления записями
add_button = Button(root, text="Добавить тренировку", command=add_workout)
add_button.pack()

edit_button = Button(root, text="Редактировать тренировку", command=edit_workout)
edit_button.pack()

# Инициализация списка тренировок
update_workout_list()

# Запуск главного цикла приложения
root.mainloop()

# Закрытие подключения к базе данных при выходе
conn.close()
