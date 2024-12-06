from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.spinner import Spinner,SpinnerOption
import random



class MainScreen(Screen):

  def __init__(self, **kwargs):
    super(MainScreen, self).__init__(**kwargs)
    self.layout = BoxLayout(orientation="vertical")

    self.label1 = Label(text="您好！",
                        font_name="SourceHanSansSC-VF.otf",
                        font_size=40)
    self.layout.add_widget(self.label1)

    self.button1 = Button(
        text="click me",
        background_color=(1, 0, 0, 1),
        size_hint=(1, 1),
        pos_hint={
            "center_x": 0.8,
            "center_y": 0.2
        },
        background_normal="C:\KivyApps\green-button-icon-png-13.png")
    self.button1.bind(on_press=self.press_button1)
    self.layout.add_widget(self.button1)

    self.button2 = Button(text="Старт")
    self.button2.bind(on_press=self.go_to_page2)
    self.layout.add_widget(self.button2)

    self.add_widget(self.layout)

  def press_button1(self, instance):
    self.label1.text = "Button clicked!"

  def go_to_page2(self, instance):
    self.manager.current = "Second"


class SecondScreen(Screen):

  def __init__(self, **kwargs):
    super(SecondScreen, self).__init__(**kwargs)
    self.layout = BoxLayout(orientation="vertical")

    self.label1 = Label(text="That's the second page")
    self.layout.add_widget(self.label1)

    self.button1 = Button(text="Вернуться")
    self.button1.bind(on_press=self.go_to_page1)
    self.layout.add_widget(self.button1)

    self.char_list = ["爱", "八", "把"]
    self.but_list = []
    for char in self.char_list:
      self.but_list.append(
          Button(text=char, font_name="SourceHanSansSC-VF.otf", font_size=40))
    for but in self.but_list:
      but.bind(on_press=self.go_to_page3)
      self.layout.add_widget(but)

    self.add_widget(self.layout)

  def go_to_page1(self, instance):
    self.manager.current = "Main"

  def go_to_page3(self, instance):
    self.manager.get_screen("Third").update_char(instance.text)
    self.manager.get_screen("Fourth").update_char(instance.text)
    self.manager.current = "Third"


class ThirdScreen(Screen):
  #character=StringProperty("")
  def __init__(self, **kwargs):
    super(ThirdScreen, self).__init__(**kwargs)
    scroll_view = ScrollView(size_hint=(1,0.8))
    self.char_list = ["爱", "八", "把"]

    self.layout = BoxLayout(orientation="vertical",padding=10)

    self.button1 = Button(text="Вернуться",size_hint_y=0.1)
    self.button1.bind(on_press=self.go_to_page2)

    self.button2 = Button(text="Начать",size_hint_y=0.1)
    self.button2.bind(on_press=self.go_to_page4)

    self.label4 = Label(text="",
                        size_hint_y=None,
                        #height=2000,
                        text_size=(400,None),
                        valign='top',
                        halign='center',
                        font_name="SourceHanSansSC-VF.otf",
                        font_size=30)


    #self.label3 = Label(text="Слова с иероглифом:")
   # self.layout.add_widget(self.label3)

   # self.label2 = Label(text="",
   #                     font_name="SourceHanSansSC-VF.otf",
   #                     font_size=40)



    scroll_view.add_widget(self.label4)

    self.layout.add_widget(scroll_view)
    self.layout.add_widget(self.button1)
    self.layout.add_widget(self.button2)

    self.add_widget(self.layout)

  def update_char(self, character):
    self.hierog = character
    self.load_words()
    #print(self.words)
    self.label4.text = self.words
    self.label4.bind(texture_size=self.adjust_h)
    #self.label4.bind(size=self.label4.setter('text_size'))
    #self.label2.text = character

  def adjust_h(self,instance,value):
    instance.height=value[1]


  def load_words(self):
    h_num=self.char_list.index(self.hierog)
    file = open(f"texts/{str(h_num)}.txt", encoding="utf8")
    self.words = file.read()
    file.close()

  def go_to_page2(self, instance):
      self.manager.current = "Second"

  def go_to_page4(self, instance):
    self.manager.current = "Fourth"

    #self.words = words[self.char_list.index(self.hierog)]
    #print(self.words)

class FourthScreen(Screen):
  def __init__(self, **kwargs):
    super(FourthScreen, self).__init__(**kwargs)
    self.char_list = ["爱", "八", "把"]
    self.word_ind=0
    self.layout = BoxLayout(orientation="vertical",padding=10)

    self.button1 = Button(text="Вернуться",size_hint_y=0.2)
    self.button1.bind(on_press=self.go_to_page3)
    self.layout.add_widget(self.button1)

    self.button2 = Button(text="Ответить",size_hint_y=0.2)
    self.button2.bind(on_press=self.check_answer)
    self.layout.add_widget(self.button2)

    self.button3 = Button(text="Следующее",size_hint_y=0.2)
    self.button3.bind(on_press=self.next_sen)
    self.layout.add_widget(self.button3)
    


    self.label1 = Label(text="", 
            font_name="SourceHanSansSC-VF.otf",
            font_size="40sp",
            markup=True)
    self.layout.add_widget(self.label1)

    self.label2 = Label(text='',font_size="40sp",
                       markup=True)
    self.layout.add_widget(self.label2)

    self.spinner = Spinner(
      text="   ",  # Default word
      values=[],  # Menu options
      size_hint=(None, None),
      size=(150, 50),
      font_name="SourceHanSansSC-VF.otf",

      font_size="38sp",
      option_cls=CustomSpinnerOption
    )
    self.spinner.bind(text=self.update_sentence)  # Bind selection change to update function
    self.add_widget(self.spinner)

    self.add_widget(self.layout)

  def update_sentence(self, spinner, selected_word):
    self.selected_word=selected_word
    self.sentence=self.sentence.replace("___","{}") 
    self.label1.text = self.sentence.format(f"[color=ff0000]{selected_word}[/color]")

  def next_sen(self,instance):
    self.label2.text=""
    self.get_random_sent()

  def get_random_sent(self):
    self.sentence=random.choice(self.words)
    self.sentence_n=self.words.index(self.sentence)
       
    self.label1.text=self.sentence
    self.spinner.text=self.all_var[0]
    self.spinner.values=self.all_var

  def update_char(self, character):
    self.hierog = character
    self.load_sentences()
    self.load_variants()
    self.get_random_sent()
    
    #print(self.words)

  def load_sentences(self):
    h_num=self.char_list.index(self.hierog)
    file = open(f"sentence/{str(h_num)}.txt", encoding="utf8")
    self.words = file.readlines()
    #print(self.words)
    file.close()

  def load_variants(self):
    h_num=self.char_list.index(self.hierog)
    file = open(f"variants/{str(h_num)}.txt", encoding="utf8")
    self.all_var = file.readline().split()
    self.true_var=file.readlines()
    #print(self.words)
    file.close()


  def go_to_page3(self, instance):
    self.manager.current = "Third"

  def check_answer(self,instance):
    
    t_word=self.true_var[self.sentence_n].strip()
    us_answer=self.sentence.format(self.selected_word)
    t_answer=self.words[self.sentence_n].replace("___",t_word)
    # print(us_answer)
    # print(t_answer)
    if us_answer == t_answer:
      self.label2.text="[color=0FFF50]Правильно![/color]"
    else:
      self.label2.text="[color=ff0000]Неправильно![/color]"
    


class CustomSpinnerOption(SpinnerOption):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.font_name = "SourceHanSansSC-VF.otf"  
      self.font_size = "38sp"  


class MyApp(App):

  def build(self):
    sm = ScreenManager()
    sm.add_widget(MainScreen(name="Main"))
    sm.add_widget(SecondScreen(name="Second"))
    sm.add_widget(ThirdScreen(name="Third"))
    sm.add_widget(FourthScreen(name="Fourth"))
    return sm


if __name__ == "__main__":
  MyApp().run()
