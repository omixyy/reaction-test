import random as rd
import tkinter
import sys
import json
from datetime import datetime


class GameInfo:
    def __init__(self, canvas):
        self.show = ''
        self.canvas = canvas

    # Создание текста на экране
    def create_start_screen(self):
        self.show = 'Welcome!'
        self.canvas.create_text(410, 250, text=self.show, fill='cornsilk', font=('Helvetica', 60))


class Buttons:
    def __init__(self, class_timer, canvas, master):
        self.class_timer = class_timer
        self.master = master
        self.canvas = canvas
        self.size_var = None
        self.button_start = None
        self.label = None
        self.diff = 90
        self.btn1, self.btn2, self.btn3 = None, None, None

        # Создание кнопок Get in и Exit
        self.button_get_in = tkinter.Button(
            self.master, text='Get in', height=1, width=5, font=('Helvetica', 20),
            command=self.choose_target_size, bg='SeaGreen', fg='cornsilk'
        )
        self.button_exit = tkinter.Button(
            self.master, text='Exit', height=1, width=5, font=('Helvetica', 20),
            command=sys.exit, bg='rosy brown', fg='cornsilk'
        )

    # Если была нажата кнопка Get in
    def button_start_pressed(self):

        # Удаление всех начальных кнопок с экрана и запуск обратного отсчёта
        self.canvas.delete('all')
        self.button_start.destroy()
        self.label.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.class_timer.timer(self.diff)

    # Расположение стартовых кнопок на экране
    def place_start_buttons(self):
        self.button_get_in.place(x=250, y=400)
        self.button_exit.place(x=450, y=400)

    # Метод выбора размера мишени
    def choose_target_size(self):
        self.canvas.delete('all')
        self.button_exit.destroy()
        self.button_get_in.destroy()
        self.size_var = tkinter.IntVar()
        self.label = tkinter.Label(text='Choose target size:')
        self.label.place(x=0, y=0, width=810)

        # Создание меню выбора размера мишени
        self.btn3 = tkinter.Radiobutton(
            self.master, text='Big', variable=self.size_var, value=3,
            command=self.draw_big_target_example
        )
        self.btn2 = tkinter.Radiobutton(
            self.master, text='Medium', variable=self.size_var, value=2,
            command=self.draw_medium_target_example
        )
        self.btn1 = tkinter.Radiobutton(
            self.master, text='Small', variable=self.size_var, value=1,
            command=self.draw_small_target_example
        )
        self.btn3.place(x=0, y=20, width=810, height=20)
        self.btn2.place(x=0, y=40, width=810, height=20)
        self.btn1.place(x=0, y=60, width=810, height=20)

        # Создание кнопки Start!, нажав которую начнётся обратный отсчёт, после чего появится первая мишень
        self.button_start = tkinter.Button(self.master, text='Start!', height=1, width=10, font=('Helvetica', 20),
                                           command=self.button_start_pressed, bg='green3', fg='snow')
        self.button_start.place(x=318, y=600)
        self.canvas.create_text(410, 150, text='Default size:', fill='cornsilk', font=('Helvetica', 60))
        self.canvas.create_oval((355, 265), (445, 355), fill='coral')

    # Отрисовка примера маленькой мишени
    def draw_small_target_example(self):
        self.canvas.delete('all')
        self.canvas.create_oval((375, 290), (425, 340), fill='coral')
        self.diff = 50

    # Отрисовка примера средней мишени
    def draw_medium_target_example(self):
        self.canvas.delete('all')
        self.canvas.create_oval((363, 275), (438, 350), fill='coral')
        self.diff = 75

    # Отрисовка примера большой мишени
    def draw_big_target_example(self):
        self.canvas.delete('all')
        self.canvas.create_oval((350, 260), (450, 360), fill='coral')
        self.diff = 100


class Target:
    def __init__(self, canvas, master):
        self.oval = None
        self.target_clicks = 0
        self.old_clicks = 0
        self.button_exit = None
        self.button_retry = None
        self.show = ''
        self.canvas = canvas
        self.master = master
        self.diff = 0
        self.moment_start, self.moment_end = None, None

    #
    def create_new_target(self, x, y, diff):
        self.diff = diff
        self.oval = self.canvas.create_oval(
            (x, y), (x + self.diff, y + self.diff), fill='coral'
        )
        self.canvas.tag_bind(self.oval, '<Button-1>', self.target_clicked)

    # Рекурсивная функция, обрабатывающая нажатия на мишень и создающая новую
    def target_clicked(self, event):
        if self.target_clicks == 0:
            self.moment_start = datetime.now()
        self.old_clicks = self.target_clicks
        self.target_clicks += 1

        # Если нажатий на мишени было меньше, чем самих мишеней, то продолжить выполнение функции
        if self.old_clicks < self.target_clicks:
            self.canvas.delete('all')

            # Пока количество нажатий на мишень не достигло 30 создавать новую
            if self.target_clicks != 30:
                self.create_new_target(rd.randint(1, 700), rd.randint(1, 600), self.diff)
                self.canvas.create_text(20, 20, text=f'{self.target_clicks}/30', fill='white', font=('Helvetica', 10))

            # Иначе показать скорость реакции и создать кнопку выхода
            else:
                if self.diff == 50:
                    size = 'Small'
                elif self.diff == 75:
                    size = 'Medium'
                elif self.diff == 100:
                    size = 'Big'
                else:
                    size = 'Default'
                self.moment_end = datetime.now()
                time_spent = round((self.moment_end - self.moment_start).seconds / 30, 3)
                show_text = f'    Your reaction is:\nOne target - ~' \
                            f'{time_spent} sec'
                self.canvas.create_text(410, 150, text=show_text, fill='cornsilk', font=('Helvetica', 30))
                self.button_exit = tkinter.Button(
                    self.master, text='Exit', height=1, width=9, font=('Helvetica', 20),
                    command=sys.exit, bg='rosy brown', fg='cornsilk'
                )
                with open('best_result.json', 'r') as jsonf:
                    reader = json.load(jsonf)
                    with open('best_result.json', 'w') as jsfile:
                        if time_spent < reader[size] or reader[size] == 0:
                            reader[size] = time_spent
                            self.canvas.create_text(410, 250, text=f'Congratulations! Your new best result is: '
                                                                   f'{time_spent}',
                                                    fill='SeaGreen1', font=('Helvetica', 20))
                        json.dump(reader, jsfile, indent=4)
                self.button_exit.place(x=318, y=600)


class Timer:
    def __init__(self, class_target, canvas, master):
        self.timer_num = 3
        self.colors = ['red', 'orange', 'yellow', 'SpringGreen2']
        self.class_target = class_target
        self.canvas = canvas
        self.master = master

    # Метод, реализующий обратный отсчёт перед началом испытания
    def timer(self, diff):
        for i in range(4):
            self.canvas.delete('all')
            self.master.after(1000, self.show_text())
            self.timer_num -= 1
            self.master.update()
        self.master.after(1000, self.canvas.delete('all'))
        self.class_target.create_new_target(rd.randint(1, 700), rd.randint(1, 600), diff)

    # Метод, показывающий цифру обратного отсчёта ф определённом цвете
    def show_text(self):
        self.canvas.create_text(
            410, 250, text=self.timer_num, fill=self.colors[self.timer_num], font=('Helvetica', 60)
        )
