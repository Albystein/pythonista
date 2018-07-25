# from kivy.config import Config
# Config.set('graphics','width','300')
# Config.set('graphics','height','500')
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from functools import partial

from kivymd.button import MDRaisedButton
from passlib.apps import custom_app_context as pwd_context
import matplotlib.pyplot as plt
import assessment
import os

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'signupscreen'
        self.app = AssessmentApp()
        self.user_data =  self.ids.name.text+':'+self.ids.username.text+':'+self.ids.email.text
    def register_user(self,password1,password2,user_data = None):
        if password1 == password2:
            password_hash = pwd_context.encrypt(password1)
            with open('C:\\Users\\albystein\\gisutech\\EASS\\password.txt','w') as password_file:
                password_file.write(user_data+':'+ password_hash)
                self.app.sm.current = 'mainscreen'
        else:
            pass

class LoginFailPopup(Popup):
    pass

class StudentPopup():
    pass

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'loginscreen'

    def authenticate_user(self, username,password):
        self._popup = LoginFailPopup()
        self.app = AssessmentApp()
        with open('C:\\Users\\albystein\\gisutech\\EASS\\password.txt') as password_file:
                credentials = password_file.read().split(':')
                if credentials[1] == username and pwd_context.verify(password,credentials[-1]):
                    self.app.sm.current = 'mainscreen'
                else:
                    self._popup.open()
                    self.app.sm.switch_to (LoginScreen())

class AssessmentScreenManager(ScreenManager):
    pass

class DatabaseInfo(FloatLayout):
    pass

class AssessmentFileChooser(FloatLayout):
    import_file = ObjectProperty()

class StylingLabel(Label):
    def __init__(self,label_color, **kwargs):
        self.label_color = label_color
        super().__init__()

class StudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'studentscreen'


class MainScreen(Screen,BoxLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'mainscreen'

class StudentGridLayout(GridLayout):
    records = ''
    show = False
    def __init__(self, **kwargs):
        super().__init__()
        self.cols = 2
        self.app = AssessmentApp()

    def load_student_data(self,dt, records):
        num = 0
        for record in records:
            for data in record:
                    self.add_widget(Label(text=str(dt[num])))
                    self.add_widget(Button(text=str(data),size_hint=(.2,.2)))
                    num+=1
                    print(num)
        self.add_widget(TextInput())
        self.add_widget(Button(text='edit'))
        self._popup = ModalView(size_hint=(.5,.5))
        self._popup.add_widget(self)#Popup(content=self,title='Student data',size_hint=(.7,.7))
        self._popup.open()
        self._popup.bind(on_dismiss=lambda *x: self._popup.remove_widget(self))#self._popup.bind(on_dismiss=self._popup.remove_widget(self.children)

class MainGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.cols =2
        db_name = 'F:\\students_database.db'
        self.layout = StudentGridLayout()
        self.app = AssessmentApp()

        if os.path.exists(db_name):
            records = assessment.retrieve_data_from_db(db_name, 'gisu')
            for record in records:
                self.btn = Button(text=str(record[0]), size_hint_y=None, height=40,background_color=get_color_from_hex('#6ae2d3'))
                self.btn.bind(on_press=partial(self.show_student_results,self.btn))
                color = assessment.determine_performance(list(record[1:]))
                label = StylingLabel(label_color = get_color_from_hex(color) )
                self.add_widget(self.btn)
                self.add_widget(label)
        else:
            pass

    def show_student_results(self,btn,*args):
        records = assessment.retrieve_student_data(btn.text,'gisu','F:\\students_database.db')
        self.layout.load_student_data(['Name', 'HOLIDAYWORK','BOT','MOT','EOT'], records)

class StudentScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__()
        layout = StudentGridLayout()
        layout.bind(minimum_height=layout.setter('height'))
        self.add_widget(layout)
        self.size=(Window.width, Window.height)

class MainScrollView(ScrollView):
    def __init__(self,**kwargs):
        super().__init__()
        layout = MainGridLayout()
        layout.bind(minimum_height=layout.setter('height'))
        self.add_widget(layout)
        self.size=(Window.width, Window.height)

class AssessmentApp(App):
    sm = AssessmentScreenManager()

    def build(self):
        self.filechooser = AssessmentFileChooser()
        self._signupscreen = SignUpScreen()
        self._loginupscreen = LoginScreen()
        self._mainscreen = MainScreen()
        self._studentscreen = StudentScreen()
        self.sm.add_widget(SignUpScreen())
        self.sm.add_widget(self._loginupscreen)
        self.sm.add_widget(self._mainscreen)
        self.sm.add_widget(self._studentscreen)
        self.sm.current = 'signupscreen'

        return self.sm

    def change_to_student_screen(self):
        self.sm.switch_to(StudentScreen())
        print(self)

    def draw_line_graph(self):
        labels = ['EXCELLENT','VERY GOOD', 'GOOD','TRAIL','FAIL']
        sizes = [32.4, 40.6, 20.7, 10.3,2.0]
        colors = ['#5cf500','#e5ea0b','#0be8ea','#ff8300' ,'#ff00ba']
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def open_popup(self):
        content = AssessmentFileChooser()
        self._popup = Popup(content = content, title = 'Import File')
        self._popup.open()

    def dismiss_filechooser(self):
        self._popup.dismiss()
        self.sm.switch_to(MainScreen())

    def create_db(self,filename):
        self.path = filename
        self.db_filename = os.path.splitext(os.path.split(self.path)[1])[0]
        self.DB_NAME = 'students_database'
        self.T_NAME = self.db_filename
        assessment.retrieve_excel_file(filename=self.path, db_name = self.DB_NAME,db_table = self.T_NAME)

    def on_start(self):
        with open('C:\\Users\\albystein\\gisutech\\EASS\\password.txt') as password_file:
            if password_file.read() == '':
                self.sm.current = 'signupscreen'
            else:
                self.sm.current = 'loginscreen'

if __name__ == '__main__':
    AssessmentApp().run()
