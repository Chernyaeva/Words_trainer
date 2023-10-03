from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import gspread
import random

sa = gspread.service_account(filename="service_account.json")
sh = sa.open("Deutsch")
wks = sh.worksheet("Verben")
row_cnt = wks.row_count


class MyDumbScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MyDumbScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.level = 1
        self.verb_list = []
        self.verb_num = random.randint(1, row_cnt)
        self.verb_list.append(self.verb_num)
        self.my_anch_for_russ = AnchorLayout(anchor_x='center', anchor_y='top', size_hint=(1, 0.2))
        self.russian = Label(text=wks.acell(f'D{self.verb_num}').value, font_size= self.my_anch_for_russ.width/3, bold=True)
        self.my_anch_for_russ.add_widget(self.russian)
        self.my_grid = GridLayout(cols=2)
        self.verb_1 = Label(text="Infinitiv", font_size= self.my_anch_for_russ.width/3)
        self.my_user_input = TextInput(font_size= self.width/3)
        self.verb_2 = Label(text="Präteritum", font_size=self.my_anch_for_russ.width / 3)
        self.my_user_input_praet_empty = Label(text="", font_size=self.my_anch_for_russ.width / 3)
        self.verb_3 = Label(text="Perfekt", font_size=self.my_anch_for_russ.width / 3)
        self.my_grid.add_widget(self.verb_1)
        self.my_grid.add_widget(self.my_user_input)
        self.my_grid.add_widget(self.verb_2)
        self.my_grid.add_widget(self.my_user_input_praet_empty)
        self.my_grid.add_widget(self.verb_3)
        submit = Button(text="Prüfen", font_size= self.my_anch_for_russ.width/3, size_hint=(1, 0.3), background_color=(0,1,10,0.8), on_press=self.submit)
        self.add_widget(self.my_anch_for_russ)
        self.add_widget(self.my_grid)
        self.add_widget(submit)


    def find_verb(self):
        if self.level == 1 or self.level == 2 or self.level == 3:
            verb_num = self.verb_num
            return verb_num

        else:
            while True:
                verb_num = random.randint(1, row_cnt)
                if verb_num not in self.verb_list:
                    self.verb_list.append(verb_num)
                    self.level = 1
                    return verb_num


    def submit(self, obj):
        verb_num = self.find_verb()
        if self.level == 1:
            if self.my_user_input.text.lower() == wks.acell(f'A{verb_num}').value.lower():
                self.level = 2
                self.my_grid.remove_widget(self.my_user_input)
                self.my_grid.remove_widget(self.my_user_input_praet_empty)
                self.my_grid.remove_widget(self.verb_3)
                self.my_grid.remove_widget(self.verb_2)
                self.inf_richtig = Label(text=wks.acell(f'A{verb_num}').value.lower(), font_size= self.my_anch_for_russ.width/25, color=(0,9,0,1), italic=True)
                self.my_grid.add_widget(self.inf_richtig)
                self.my_grid.add_widget(self.verb_2)
                self.my_user_input_praet = TextInput(font_size= self.my_anch_for_russ.width/25)
                self.my_grid.add_widget(self.my_user_input_praet)
                self.my_grid.add_widget(self.verb_3)
            else:
                self.my_user_input.background_color = (0.8, 0.5, 0.5, 1.0)

        elif self.level == 2:
            if self.my_user_input_praet.text.lower() == wks.acell(f'B{verb_num}').value.lower():
                self.level = 3
                self.my_grid.remove_widget(self.my_user_input_praet)
                self.my_grid.remove_widget(self.verb_3)
                self.praet_richtig = Label(text=wks.acell(f'B{verb_num}').value.lower(), font_size= self.my_anch_for_russ.width/25, color=(0,9,0,1), italic=True)
                self.my_grid.add_widget(self.praet_richtig)
                self.my_grid.add_widget(self.verb_3)
                self.my_user_input_perf = TextInput(font_size= self.my_anch_for_russ.width/25)
                self.my_grid.add_widget(self.my_user_input_perf)
            else:
                self.my_user_input_praet.background_color = (0.8, 0.5, 0.5, 1.0)
        elif self.level == 3:
            if self.my_user_input_perf.text.lower() == wks.acell(f'C{verb_num}').value.lower():
                self.level = 4
                self.my_anch_for_russ.remove_widget(self.russian)
                self.my_grid.remove_widget(self.verb_2)
                self.my_grid.remove_widget(self.verb_3)
                self.my_grid.remove_widget(self.inf_richtig)
                self.my_grid.remove_widget(self.praet_richtig)
                self.my_grid.remove_widget(self.my_user_input_perf)
                if len(self.verb_list) == row_cnt:
                    self.clear_widgets()
                    end = Label(text="Das war's!", font_size= self.my_anch_for_russ.width/10, color=(.8,0,.4,.8))
                    self.add_widget(end)
                else:
                    self.verb_num = self.find_verb()
                    self.my_user_input = TextInput(font_size=self.width / 25)
                    self.russian = Label(text=wks.acell(f'D{self.verb_num}').value, font_size=self.width / 25, bold=True)
                    self.my_anch_for_russ.add_widget(self.russian)
                    self.my_grid.add_widget(self.my_user_input)
                    self.my_grid.add_widget(self.verb_2)
                    self.my_grid.add_widget(self.my_user_input_praet_empty)
                    self.my_grid.add_widget(self.verb_3)
            else:
                self.my_user_input_perf.background_color = (0.8, 0.5, 0.5, 1.0)

class MyApp(App):

    def build(self):
        return MyDumbScreen()


if __name__ == '__main__':
    MyApp().run()