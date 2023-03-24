import tkinter
import reactionometer_classes as react_cl


# Создаём окно и экземпляры классов
master = tkinter.Tk()
master.title('Reaction-O-Meter')
canvas = tkinter.Canvas(master, bg='dark cyan', height=700, width=800)
game_info = react_cl.GameInfo(canvas)
aim = react_cl.Target(canvas, master)
time = react_cl.Timer(aim, canvas, master)
btn = react_cl.Buttons(time, canvas, master)

# Располагаем начальные кнопки на экране
game_info.create_start_screen()
btn.place_start_buttons()

# Закрываем (пакуем) программу
canvas.pack()
master.mainloop()
