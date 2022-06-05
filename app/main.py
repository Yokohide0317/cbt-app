#-*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.lang import Builder
import japanize_kivy

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty 
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput


class ReadFile():
    def __init__(self, csv_file):
        with open(csv_file) as f:
            lines = f.readlines()
        self.lineArr = [l.split(",") for l in lines]

    def getQuestion(self, n: int):
        q = self.lineArr[n][1]
        res = f"Q. {q}"
        return res

    def getAnswer(self, n: int):
        a = self.lineArr[n][2]
        res = f"A. {a}"
        return res

class TextWidget(Widget):
    text = StringProperty()
    question = StringProperty()
    answer = StringProperty()
    question = StringProperty()
    readFile = ReadFile("./question.csv")

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)

        # 問題の表示
        self.question = self.readFile.getQuestion(0)

        ti = TextInput(text='Hello world', multiline=False)
        ti.bind(on_text_validate=self.on_enter)

    # ボタンクリックで
    def buttonClicked(self):
        self.answer = self.readFile.getAnswer(0) 


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()

if __name__ == '__main__':
    TestApp().run()
