from docutils.nodes import transition
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import *



class MyApp(App):
    def build(self):
        screen_man = ScreenManager(transition=ShaderTransition())
        screen_man.add_widget(FirstScreen(name='1'))
        screen_man.add_widget(SecondScreen(name='2'))
        return screen_man

class FirstScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        b = Button(text='Текст')
        a = Button(text='Текст')
        layout.add_widget(b)
        layout.add_widget(a)
        a.on_press=self.next
        self.add_widget(layout)

    def next(self):
        self.manager.current='2'
        self.manager.transition.direction='down'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        b = Button(text='Текст')
        layout.add_widget(b)
        b.on_press=self.not_next
        self.add_widget(layout)

    def not_next(self):
        self.manager.current='1'
        self.manager.transition.direction='up'

app = MyApp()
app.run()