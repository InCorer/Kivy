from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.uix.textinput import TextInput
from win32.lib.win32con import FALSE

from instructions import *
from kivy.properties import BooleanProperty



class MyApp(App):
    def build(self):
        screen_man = ScreenManager()
        screen_man.add_widget(FirstScreen(name='1'))
        screen_man.add_widget(SecondScreen(name='2'))
        screen_man.add_widget(ThirdScreen(name='3'))
        screen_man.add_widget(FourthScreen(name='4'))
        return screen_man

class FirstScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=8, padding=8)
        a = Button(text='Начать', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        text = Label(text=txt_instruction)
        line_name = TextInput(height='30px', size_hint=(1, None), pos_hint={'center_y': 0.5}, multiline=False)
        self.line_age = TextInput(height='30px', size_hint=(1, None), pos_hint={'center_y': 0.5}, multiline=False)
        name_layout = BoxLayout()
        age_layout = BoxLayout()
        name_label = Label(text='Введите имя:', halign='right')
        age_label = Label(text='Введите возраст:', halign='right')
        layout.add_widget(text)
        layout.add_widget(name_layout)
        name_layout.add_widget(name_label)
        name_layout.add_widget(line_name)
        age_layout.add_widget(age_label)
        age_layout.add_widget(self.line_age)
        layout.add_widget(age_layout)
        layout.add_widget(a)
        a.on_press=self.next
        self.add_widget(layout)



    def next(self):
        global age
        try:
            age = int(self.line_age.text)
            self.manager.current='2'
            self.manager.transition.direction='down'
        except ValueError:
            pass

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        pulse_layout = BoxLayout()
        self.b = Button(text='Продолжить', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        text = Label(text=txt_test1)
        pulse_label = Label(text='Введите результат:')
        self.pulse_line = TextInput(height='30px', size_hint=(1, None), pos_hint={'center_y': 0.5}, multiline=False)
        self.pulse_line.set_disabled(True)
        self.timer = Timer(1)
        self.timer.bind(done=self.unblock)
        layout.add_widget(text)
        layout.add_widget(self.timer)
        layout.add_widget(pulse_layout)
        pulse_layout.add_widget(pulse_label)
        pulse_layout.add_widget(self.pulse_line)
        layout.add_widget(self.b)
        self.add_widget(layout)
        self.b.on_press = self.next

    def unblock(self, *args):
        self.pulse_line.set_disabled(False)
        self.b.set_disabled(False)

    def next(self):
        global pulse
        try:
            pulse = int(self.pulse_line.text)
            self.manager.current = '3'
            self.manager.transition.direction = 'down'
        except ValueError:
            self.timer.start()
            self.b.set_disabled(True)

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        text = Label(text=txt_sits)
        self.c = Button(text='Продолжить', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        self.timer = Timer(1)
        self.timer.bind(done=self.unblock)
        self.done = False
        layout.add_widget(text)
        layout.add_widget(self.timer)
        layout.add_widget(self.c)
        self.add_widget(layout)
        self.c.on_press = self.next

    def unblock(self, *args):
        self.c.set_disabled(False)
        self.done = True
        self.next()

    def next(self):
        if self.done:
            self.manager.current = '4'
            self.manager.transition.direction = 'down'
        else:
            self.timer.start()
            self.c.set_disabled(True)


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        res_layout = BoxLayout()
        res2_layout = BoxLayout()
        text = Label(text=txt_test3)
        self.d = Button(text='Завершить', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        res_label = Label(text='Результат:')
        self.res_line = TextInput(height='30px', size_hint=(1, None), pos_hint={'center_y': 0.5}, multiline=False)
        res2_label = Label(text='Результат после отдыха:')
        self.res2_line = TextInput(height='30px', size_hint=(1, None), pos_hint={'center_y': 0.5}, multiline=False)
        self.timer = Timer(3)
        self.timer.bind(done=self.unblock)
        self.res_line.set_disabled(True)
        self.res2_line.set_disabled(True)
        layout.add_widget(text)
        layout.add_widget(self.timer)
        layout.add_widget(res_layout)
        layout.add_widget(res2_layout)
        layout.add_widget(self.d)
        res_layout.add_widget(res_label)
        res_layout.add_widget(self.res_line)
        res2_layout.add_widget(res2_label)
        res2_layout.add_widget(self.res2_line)
        self.add_widget(layout)
        self.d.on_press = self.next

    def unblock(self, *args):
        self.res_line.set_disabled(False)
        self.timer.total = 5
        self.timer.start()
        self.timer.done = False
        self.timer.bind(done=self.unblock2)

    def unblock2(self, *args):
        self.res2_line.set_disabled(False)


    def next(self):
        global res, res2
        try:
            res = int(self.res_line.text)
            res2 = int(self.res2_line.text)
            self.manager.current='1'
            self.manager.transition.direction='down'
        except ValueError:
            self.timer.start()
            self.d.set_disabled(True)


class Timer(Label):
    done = BooleanProperty(False)
    def __init__(self, total,**kwargs):
        self.current = 0
        self.total = total
        text = 'Прошло секунд:' + str(self.current)
        self.done = False
        super().__init__(text=text ,**kwargs)

    def start(self):
        Clock.schedule_interval(self.change,1)

    def change(self, dt):
        if self.current < self.total:
            self.current += 1
            self.text = 'Прошло секунд: ' + str(self.current)
        else:
            self.done = True
            return False

app = MyApp()
app.run()