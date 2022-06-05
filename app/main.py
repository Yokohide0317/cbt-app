#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty 
from kivy.uix.widget import Widget


class TextWidget(Widget):
    text = StringProperty()    # プロパティの追加

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = 'Question'

    def buttonClicked(self):        # ボタンをクリック時
        self.text = 'Hello World'


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'

    def build(self):
        return TextWidget()

if __name__ == '__main__':
    TestApp().run()
