import wmi
import tkinter as tk
from tkinter import font, messagebox
import requests
import socket
import platform
import io


def submit():
    user_input = entry.get()
    if user_input != '' and user_input:
        c = wmi.WMI()

        pc_name = socket.gethostname()

        info = f'Номер кабинета: {user_input}\nКомп: {socket.gethostname()}\n'
        info += f'Ось: {platform.system()} - {platform.version()}\n'

        for board in c.Win32_BaseBoard():
            info += f'Материнская плата: {board.Product}\n'

        for processor in c.Win32_Processor():
            info += f'Процессор: {processor.Name}\n'

        video_cards = c.Win32_VideoController()
        if video_cards:
            for card in video_cards:
                info += f"Название видеокарты: {card.Name}\n"
        else:
            info += "Видеокарты не найдены.\n"

        for i, memory in enumerate(c.Win32_PhysicalMemory()):
            info += f'Плашка {i}: {int(memory.Capacity) / 1048576:.0f} мб\n'

        for disk in c.Win32_DiskDrive():
            info += f'Имя жесткого диска: {disk.Caption}\n'
            info += f'Объем: {int(disk.Size) / 1073741824:.0f} гб\n'

            info += f'Тип носителя: {disk.MediaType}\n'

        file = io.BytesIO(info.encode('utf-8'))
        file.name = f'cab-{user_input}_pc-{pc_name}.txt'

        response = requests.post(
            f'https://api.telegram.org/bot7219279963:AAHBLOWQuPPygCM0NjVPYdAyG1Q4BqAqoAk/sendDocument',
            data={'chat_id': '1912263952'},
            files={'document': file}
        )

        if response.status_code == 200:
            messagebox.showinfo(
                title='<з',
                message='Большое спасибо!'
            )
            root.destroy()
        else:
            messagebox.showinfo(
                title='Ошибка!',
                message='Ошибка при отправке файла - нажмите готово ещё раз через несколько секунд.'
            )
    else:
        messagebox.showinfo(
            title='Ошибка!',
            message='Введите номер кабинета!'
        )


root = tk.Tk()
root.title("(o_o)")
x = (root.winfo_screenwidth() // 2) - 150
y = (root.winfo_screenheight() // 2) - 155
root.geometry(f"{300}x{150}+{x}+{y}")

app_font = font.Font(size=14)

label = tk.Label(root, text="Введите номер кабинета:", font=app_font)
label.pack(pady=10)

entry = tk.Entry(root, font=app_font)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Готово", command=submit, font=app_font)
submit_button.pack(pady=10)

root.mainloop()
